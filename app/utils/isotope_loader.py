"""Loads and parses isotope data from a JSON dataset into Isotope objects."""

import json
from ..static.models.isotopes import Isotope

def extract_gamma(probability_str):
    try:
        return float(probability_str.split()[0])
    except:
        return 0

def load_unstable_isotopes(filepath="app/static/models/unstable_isotopes.json"):
    with open(filepath) as f:
        raw_data = json.load(f)

    return {
        key.lower(): Isotope(
            name=val["name"],
            half_life=float(val["half_life"]),
            half_life_unit=val["half_life_unit"],
            gamma_emission_probability=extract_gamma(val.get("decay_mode", {}).get("probability", "0"))
        )
        for key, val in raw_data.items()
    }
