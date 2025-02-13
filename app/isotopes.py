from dataclasses import dataclass

@dataclass
class Isotope:
    name: str
    half_life: float
    gamma_emission_probability: float
    half_life_unit: str                     # s, d, or y

CARBON_14 = Isotope(name="Carbon-14", half_life=5730, gamma_emission_probability=0, half_life_unit='y')
COBALT_60 = Isotope(name="Cobalt-60", half_life=5.27, gamma_emission_probability=99.85, half_life_unit='y')  # 99.85% at 1173.23 keV, 99.98% at 1332.49 keV
IODINE_131 = Isotope(name="Iodine-131", half_life=8.02, gamma_emission_probability=81.2, half_life_unit='d')
URANIUM_238 = Isotope(name="Uranium-238", half_life=4.468e9, gamma_emission_probability=0.06, half_life_unit='y')  # Estimated weak gamma emission (~0.06-0.2%)
CESIUM_137 = Isotope(name="Cesium-137", half_life=30.08, gamma_emission_probability=85.1, half_life_unit='y')  # Not widely available, verify source