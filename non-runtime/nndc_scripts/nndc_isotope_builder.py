"""Scrapes decay data from NNDC for selected isotopes and generates static/models/unstable_isotopes.json.

Not needed at runtime."""

import os 
import re 
import json
import time
import requests
import periodictable
import unicodedata

from bs4 import BeautifulSoup

from target_isotopes import TARGET_ISOTOPES

OUTPUT_FILE = "app/static/models/unstable_isotopes.json"

DECAY_TRANSLATIONS = {
    "β -": "beta minus",
    "β +": "beta plus",
    "α": "alpha",
    "γ": "gamma",
    "EC": "electron capture",
    "ε": "electron capture",
    "n": "neutron emission",
    "p": "proton emission",
    "SF": "spontaneous fission"
}

GREEK_TRANSLATIONS = {
    "β": "beta",
    "α": "alpha",
    "γ": "gamma",
    "ε": "epsilon"
}

if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w") as f:
        json.dump({}, f)
        
try:
    with open(OUTPUT_FILE, "r") as f:
        ISOTOPES_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    ISOTOPES_DATA = {}

def get_response(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error at {url}: {e}")
        return None


def get_table(response=None, element=None, iso_num=None):
    soup = BeautifulSoup(response.text, "html.parser")
    
    tables = soup.find_all("table")

    for idx, table in enumerate(tables):
        headers = table.find_all("td", class_="shead")
        if headers and any("Parent" in header.text for header in headers):
            return table

    return None


def extract_half_life(raw_value):
    """
    Extracts and properly formats the half-life value, unit, and uncertainty.
    
    Handles:
    - Scientific notation (e.g., "1.51×10 7 s" → "1.51e7 s")
    - Uncertainty values (e.g., "12.32 y ± 2" → value: 12.32, uncertainty: 2)
    - Unitless or malformed entries will be marked as "unknown"
    """
    if not raw_value:
        return "unknown", "unknown", "unknown"

    raw_value = raw_value.replace("\u00d7", "e").replace("×", "e")
    raw_value = re.sub(r"\s*±\s*", " ", raw_value)

    parts = raw_value.strip().split()

    value = parts[0] if parts else "unknown"
    unit = parts[1] if len(parts) > 1 else "unknown"
    uncertainty = parts[2] if len(parts) > 2 else "unknown"

    try:
        value = float(value)
    except ValueError:
        value = "unknown"

    return value, unit, uncertainty


def extract_text(td):
    nested_table = td.find("table")
    return " ".join(nested_table.get_text(" ", strip=True).split()) if nested_table else td.get_text(" ", strip=True)


def extract_decay_mode(decay_mode):
    parts = decay_mode.split(":")
    decay_symbol = parts[0].strip()
    probability = parts[1].strip() if len(parts) > 1 else "unknown"

    decay_type = DECAY_TRANSLATIONS.get(decay_symbol)

    if decay_type is None:
        normalized_symbol = unicodedata.normalize("NFKC", decay_symbol)

        for greek_char, replacement in GREEK_TRANSLATIONS.items():
            normalized_symbol = normalized_symbol.replace(greek_char, replacement)

        decay_type = DECAY_TRANSLATIONS.get(normalized_symbol, normalized_symbol)

    return {
        "symbol": decay_symbol,
        "type": decay_type,
        "probability": probability
    }


def extract_from_rows(table=None, element=None, iso_num=None):
    """
    Extracts isotope decay data from an HTML table while handling nested structures and redundant columns.

    !TODO: revisit this function to optimize and improve readability 

    Scraping was complex due to different formats between isotopes.
    Function is lengthy due to the challenges encountered:
    - "Parent Nucleus" includes a nested table, splitting content into multiple `<td>` elements
        - Similarly, "Daughter Nucleus" has extra columns that need to be filtered out
    - "Decay Mode" may contain both a type (e.g., "β -") and a probability (e.g., "100%")
    - Scientific notation and uncertainties in half-life need proper parsing
    - Symbols like "β -" should be translated into readable names ("beta minus")

    Solution:
    - Extract "Parent Nucleus" separately and ignore redundant columns
        - Extract only the first occurrence of "Daughter Nucleus"
    - Parse "Decay Mode" into a dictionary with `"type"` and `"probability"`
    - Normalize `Jπ` (spin/parity) into `"parent_spin_parity"`
    - Translate common decay types into readable names
    """

    if not table:
        return None

    rows = table.find_all("tr")
    if not rows:
        return None

    expected_headers = [
        "Parent Nucleus", "Parent E", "Parent Jπ", "Parent Half-Life",
        "Decay Mode", "GS-GS Q-value (keV)", "Daughter Nucleus"
    ]

    header_row = rows[0]
    header_cols = [col for col in header_row.find_all("td") if not col.has_attr("rowspan")]

    header_texts = [col.get_text(strip=True) for col in header_cols]
    if not all(any(expected in text for text in header_texts) for expected in ["Parent", "Decay Mode"]):
        return None

    column_map = {idx: header for idx, header in enumerate(expected_headers)}

    extracted_data = []
    for row in rows[1:]:
        all_td = row.find_all("td")

        if len(all_td) < 10:
            continue

        parent_nucleus = extract_text(all_td[0])
        remaining_cols = [extract_text(td) for td in all_td[3:-3]]
        daughter_nucleus = extract_text(all_td[-3])

        if len(remaining_cols) != 5:
            continue

        row_data = {column_map[0]: parent_nucleus}
        for i in range(5):
            row_data[column_map[i + 1]] = remaining_cols[i]
        row_data["Daughter Nucleus"] = daughter_nucleus

        half_life_value, half_life_unit, half_life_uncertainty = extract_half_life(row_data.get("Parent Half-Life", ""))
        decay_mode_dict = extract_decay_mode(row_data.get("Decay Mode", ""))

        print(dir(element))
        structured_entry = {
            "name": f"{element.name}-{iso_num}",
            "short_name": f"{element.symbol}-{iso_num}",
            "atomic_number": element.number, 
            "mass": element.mass, 
            "density": element.density,
            "half_life": half_life_value,
            "half_life_unit": half_life_unit,
            "half_life_uncertainty": half_life_uncertainty,
            "parent_nucleus": row_data["Parent Nucleus"],
            "parent_energy": row_data["Parent E"],
            "parent_spin_parity": row_data["Parent Jπ"],
            "decay_mode": decay_mode_dict,
            "gs_gs_q_value": row_data["GS-GS Q-value (keV)"],
            "daughter_nucleus": row_data["Daughter Nucleus"]
        }

        extracted_data.append(structured_entry)

    return extracted_data[0] if len(extracted_data) == 1 else None


def check_stability(response):
    soup = BeautifulSoup(response.text, "html.parser")
    if "No datasets were found since nucleus is stable" in soup.get_text():
        return 'stable'


def parse_response(response=None, element=None, iso_num=None):
    if check_stability(response) == 'stable':
        return False
    
    table = get_table(response=response, element=element, iso_num=iso_num)
    element_data = extract_from_rows(table=table, element=element, iso_num=iso_num)
    return element_data


def get_half_life_data(element, isotope_number):
    url = f"https://www.nndc.bnl.gov/nudat3/decaysearchdirect.jsp?nuc={element.symbol}{isotope_number}&unc=NDS"
    response = get_response(url)

    element_data = parse_response(response=response, element=element, iso_num=isotope_number)
    
    if element_data is False:
        print(f"{element}-{isotope_number} is stable. Continuing...")
        return None 
    
    return element_data


def scrape_isotopes():
    for element in periodictable.elements:

        for isotope_number in element.isotopes:
            print(f"Checking isotope: {element.symbol}-{isotope_number}")
            short_name = f"{element.symbol}-{isotope_number}"
            if short_name in TARGET_ISOTOPES:
                isotope_data = get_half_life_data(element, isotope_number)
                print(isotope_data)
                if isotope_data:
                    ISOTOPES_DATA[isotope_data["short_name"]] = isotope_data
                    print(f"Saved {isotope_data['short_name']}: {isotope_data['half_life']} {isotope_data['half_life_unit']}")
                    
                    with open(OUTPUT_FILE, "w") as f:
                        json.dump(ISOTOPES_DATA, f, indent=4)
                    
                    time.sleep(1)


if __name__ == "__main__":
    scrape_isotopes()

    # print(unicodedata.normalize("NFKC", "𝛽"))