const isotopeSelect = document.getElementById("isotope");
const datasetSelect = document.getElementById("datasets");
let selectedOption;

document.addEventListener("DOMContentLoaded", () => {
  const simulationForm = document.getElementById("simulationForm");
  const dataPointsButton = document.getElementById("dataPointsButton");
  const dataPointsContainer = document.getElementById("dataPointsContainer");
  const submitButton = simulationForm.querySelector('button[type="submit"]');
  const customIsotopeFields = document.getElementById("customIsotopeFields");

  if (simulationForm) {
    initializeSimulationForm(simulationForm);
  }

  if (isotopeSelect) {
    isotopeSelect.addEventListener("change", () => {
      if (customIsotopeFields) {
        customIsotopeFields.style.display =
          isotopeSelect.value === "custom" ? "block" : "none";
      }
    });
  }

  if (dataPointsButton && dataPointsContainer) {
    dataPointsContainer.style.display = "none";

    dataPointsButton.addEventListener("click", () => {
      const isHidden = dataPointsContainer.style.display === "none";
      dataPointsContainer.style.display = isHidden ? "block" : "none";
      dataPointsButton.textContent = isHidden
        ? "Hide Data Points"
        : "Show Data Points";
    });
  }

  const checkboxes = document.querySelectorAll("input[type=checkbox]");

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      checkCheckboxes();
    });
  });

  function checkCheckboxes() {
    const anyChecked = Array.from(checkboxes).some(
      (checkbox) => checkbox.checked
    );
    submitButton.disabled = !anyChecked;
  }

  checkCheckboxes(); // Initial check to disable the button if no checkboxes are checked
});

document.addEventListener("DOMContentLoaded", () => {
  const settingsToggle = document.getElementById("settingsToggle");
  const settingsContent = document.getElementById("settingsContent");

  if (settingsToggle && settingsContent) {
    settingsToggle.addEventListener("click", () => {
      const isHidden = settingsContent.style.display === "none";
      settingsContent.style.display = isHidden ? "block" : "none";
      settingsToggle.querySelector(".settings-text").textContent = isHidden
        ? "Hide Advanced Settings"
        : "Show Advanced Settings";
    });
  }

  // Other existing code...
});

datasetSelect.addEventListener("change", (event) => {
  if (!event.target.value) {
    isotopeSelect.disabled = false;
    isotopeSelect.style.opacity = 1;
  } else {
    isotopeSelect.disabled = true;
    isotopeSelect.style.opacity = 0.5;
    selectedOption = event.target.selectedOptions[0]; // Get the selected <option> element
    console.log();
  }
});

function initializeSimulationForm(form) {
  form.addEventListener("submit", handleSimulationSubmit);
}

const saveImageButton = document.getElementById("saveImageButton");

saveImageButton.addEventListener("click", () => {
  const plotImg = document.getElementById("decayPlot").src;
  const a = document.createElement("a");
  a.href = plotImg;
  a.download = "decay_plot.png";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  saveImageButton.disabled = true;
  saveImageButton.innerHTML = '<span class="spinner">↻</span> Saving...';

  setTimeout(() => {
    saveImageButton.disabled = false;
    saveImageButton.innerHTML = "Save as Image";
  }, 400);
});

async function handleSimulationSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const submitButton = e.submitter;

  submitButton.disabled = true;
  submitButton.innerHTML = '<span class="spinner">↻</span> Running...';

  // custom isotope validation
  if (form.isotope.value === "custom") {
    const requiredFields = ["custom_name", "custom_half_life", "custom_gamma"];
    for (const field of requiredFields) {
      if (!form[field].value) {
        showError(`Please fill in all custom isotope fields`);
        submitButton.disabled = false;
        submitButton.innerHTML = "Run Simulation";
        return;
      }
    }
  }

  const data = {
    isotope: form.isotope.value,
    initial_amount: form.initial_amount.value,
    time_points: form.time_points.value,
    noise: form.noise.value,
    checkedBoxes: Array.from(form.elements)
      .filter((el) => el.type === "checkbox" && el.checked)
      .map((el) => el.name),
  };

  const isotope_search = form.isotope_search.value;

  // logic for custom isotope
  if (data.isotope === "custom") {
    data.custom_name = form.custom_name.value;
    data.custom_half_life = form.custom_half_life.value;
    data.custom_half_life_unit = form.custom_half_life_unit.value;
    data.custom_gamma = form.custom_gamma.value;
  }

  // logic for selected dataset isotope 
  if (selectedOption) {
    data.isotope = "custom"
    data.custom_name = `${isotope_search} - ${selectedOption.value.split(":")[0].trim()}`;
    data.custom_gamma = selectedOption.dataset.intensity;
    data.custom_half_life = selectedOption.dataset.halfLife;
    data.custom_half_life_unit = selectedOption.dataset.halfLifeUnit;
  }

  try {
    let response;
    if (submitButton.id === "runSimulationButton") {
      response = await fetch("/simulate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    } else if (submitButton.id === "searchButton") {
      response = await fetch("/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(isotope_search),
      });
      isotopeSelect.disabled = true;
      isotopeSelect.style.opacity = 0.5;
      datasetSelect.disabled = false;
      datasetSelect.style.opacity = 1;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    if (submitButton.id === "runSimulationButton") {
      updateSimulationResults(result);
    } else if (submitButton.id === "searchButton") {
      updateDatasetSelection(result);
    }
  } catch (error) {
    console.error("Error:", error);
    showError("An error occurred while processing the request.");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML =
      submitButton.id === "runSimulationButton" ? "Run Simulation" : "Search";
  }
}

function updateSimulationResults(result) {
  const plotImg = document.getElementById("decayPlot");
  plotImg.src = `data:image/png;base64,${result.plot}`;

  const tableBody = document.getElementById("dataTable");
  tableBody.innerHTML = result.data
    .map(
      (point) => `
        <tr>
            <td>${point.time}</td>
            <td>${point.remaining}</td>
            <td>${point.decayed}</td>
            <td>${point.rate}</td>
            <td>${point.gamma}</td>
        </tr>
    `
    )
    .join("");

  const results = document.getElementById("results");
  results.style.display = "block";

  const dataPointsContainer = document.getElementById("dataPointsContainer");
  dataPointsContainer.style.display = "none";
  const dataPointsButton = document.getElementById("dataPointsButton");
  dataPointsButton.textContent = "Show Data Points";
}

function updateDatasetSelection(datasets) {
  // Clear existing options
  datasetSelect.innerHTML = "";

  // Check if datasets is empty
  if (Object.keys(datasets).length === 0) {
    option.disabled = true;
    option.selected = true;
    return;
  }

  for (const entire of Object.values(datasets)) {
    for (const [id, dataset] of Object.entries(entire)) {
      const isotopeData = dataset.isotope_data[0];
      for (const emission of dataset.gamma_emissions) {
        if (emission.type === "gamma") {
          const option = document.createElement("option");
          option.textContent = `Dataset ${id}: γ: ${emission.intensity}% - Energy: ${emission.energy} keV - T₁/₂: ${isotopeData.half_life} ${isotopeData.unit}`;
          option.dataset.energy = emission.energy;
          option.dataset.intensity = emission.intensity;
          option.dataset.halfLife = isotopeData.half_life;
          option.dataset.halfLifeUnit = isotopeData.unit;
          datasetSelect.appendChild(option);
        }
      }
    }
  }

  const option = document.createElement("option");
  option.value = "";
  option.textContent = "None";
  datasetSelect.appendChild(option);
}

function showError(message) {
  const errorDiv = document.createElement("div");
  errorDiv.className = "alert alert-error";
  errorDiv.textContent = message;

  const mainContent = document.querySelector("main");
  mainContent.insertBefore(errorDiv, mainContent.firstChild);

  setTimeout(() => {
    errorDiv.remove();
  }, 5000);
}
