from dataclasses import dataclass

@dataclass
class Isotope:
    name: str
    half_life: float
    gamma_emission_probability: float
    half_life_unit: str                     # s, d, or y

CARBON_14 = Isotope(name="Carbon-14", half_life=5730, gamma_emission_probability=0, half_life_unit='y')
RADIUM_226 = Isotope(name="Radium-226", half_life=1600, gamma_emission_probability=3.6, half_life_unit='y')
COBALT_60 = Isotope(name="Cobalt-60", half_life=5.27, gamma_emission_probability=99.85, half_life_unit='y')
IODINE_131 = Isotope(name="Iodine-131", half_life=8.02, gamma_emission_probability=81.2, half_life_unit='d')
URANIUM_238 = Isotope(name="Uranium-238", half_life=4.468e9, gamma_emission_probability=0.06, half_life_unit='y')
CESIUM_137 = Isotope(name="Cesium-137", half_life=30.08, gamma_emission_probability=85.1, half_life_unit='y')