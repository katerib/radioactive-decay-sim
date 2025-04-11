document.addEventListener("DOMContentLoaded", () => {
  const simulationForm = document.getElementById("simulationForm");
  const isotopeSelect = document.getElementById("isotope");
  const dataPointsButton = document.getElementById("dataPointsButton");
  const dataPointsContainer = document.getElementById("dataPointsContainer");
  const customIsotopeFields = document.getElementById("customIsotopeFields");
  const saveImageButton = document.getElementById("saveImageButton");
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

  // Initialize Selectize on the isotope dropdown
  if (isotopeSelect) {
    const selectizeInstance = $(isotopeSelect).selectize({
      create: false,
      sortField: "text",
      onChange: (value) => {
        if (customIsotopeFields) {
          customIsotopeFields.style.display =
            value === "custom" ? "block" : "none";
        }
      },
    })[0].selectize;

    // Trigger onChange for the initial selection
    selectizeInstance.onChange(selectizeInstance.getValue());
  }

  if (simulationForm) {
    initializeSimulationForm(simulationForm);
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

  if (saveImageButton) {
    saveImageButton.addEventListener("click", handleSaveImage);
  }

  const checkboxes = document.querySelectorAll("input[type=checkbox]");
  checkboxes.forEach((checkbox) =>
    checkbox.addEventListener("change", checkCheckboxes)
  );
  checkCheckboxes();
});

function checkCheckboxes() {
  const submitButton = document.querySelector("#runSimulationButton");
  const checkboxes = document.querySelectorAll("input[type=checkbox]");
  const anyChecked = Array.from(checkboxes).some((c) => c.checked);
  submitButton.disabled = !anyChecked;
}

function initializeSimulationForm(form) {
  form.addEventListener("submit", handleSimulationSubmit);
}

function handleSaveImage() {
  const plotImg = document.getElementById("decayPlot").src;
  const a = document.createElement("a");
  a.href = plotImg;
  a.download = "decay_plot.png";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);

  const saveImageButton = document.getElementById("saveImageButton");
  saveImageButton.disabled = true;
  saveImageButton.innerHTML = '<span class="spinner">↻</span> Saving...';

  setTimeout(() => {
    saveImageButton.disabled = false;
    saveImageButton.innerHTML = "Save as Image";
  }, 400);
}

async function handleSimulationSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const submitButton = e.submitter;

  submitButton.disabled = true;
  submitButton.innerHTML = '<span class="spinner">↻</span> Running...';

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

  if (!form.isotope.value) {
    showError("Please select an isotope or enter a custom one.");
    submitButton.disabled = false;
    submitButton.innerHTML = "Run Simulation";

    document.getElementById("decayPlot").src = "";
    document.getElementById("selectedIsotopeDisplay").textContent = "";
    document.getElementById("results").style.display = "none";

    return;
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

  if (data.isotope === "custom") {
    data.custom_name = form.custom_name.value;
    data.custom_half_life = form.custom_half_life.value;
    data.custom_half_life_unit = form.custom_half_life_unit.value;
    data.custom_gamma = form.custom_gamma.value;
  }

  try {
    const response = await fetch("/simulate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    updateSimulationResults(result);
  } catch (error) {
    console.error("Error:", error);
    showError("An error occurred while processing the request.");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "Run Simulation";
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

  dataPointsContainer.style.display = "none";
  const dataPointsButton = document.getElementById("dataPointsButton");
  dataPointsButton.textContent = "Show Data Points";

  // Display isotope name above the plot
  const isotopeSelect = document.getElementById("isotope");
  const selectedText = isotopeSelect.options[isotopeSelect.selectedIndex].text;
  document.getElementById("selectedIsotopeDisplay").textContent = selectedText;

// Create a download link for the simulation data
const simulationData =
  "data:text/json;charset=utf-8," +
  encodeURIComponent(JSON.stringify(result.data, null, 2));

// Remove any existing download link to avoid duplicates
const existingDownloadLink = document.getElementById("saveSimulationData");
if (existingDownloadLink) {
  existingDownloadLink.remove();
}

// Create a new download link
const downloadLink = document.createElement("a");
downloadLink.id = "saveSimulationData";
downloadLink.href = simulationData;
downloadLink.download = `${selectedText.split(" ")[0]}_data.json`;
downloadLink.textContent = "Save as JSON";
downloadLink.style.marginTop = "10px";
downloadLink.style.display = "block";

// Append the download link to the container
document.getElementById("dataPointsContainer").appendChild(downloadLink);

  // Reset Selectize dropdown to placeholder
  if ($("#isotope")[0].selectize) {
    $("#isotope")[0].selectize.clear();
  }
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
