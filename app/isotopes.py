from dataclasses import dataclass

@dataclass
class Isotope:
    name: str
    half_life: float
    gamma_emission_probability: float
    half_life_unit: str                     # s, d, or y

CARBON_14 = Isotope(name="Carbon-14", half_life=5730, gamma_emission_probability=99.85, half_life_unit='y')
IODINE_131 = Isotope(name="Iodine-131", half_life=8.02, gamma_emission_probability=81.2, half_life_unit='d')
URANIUM_238 = Isotope(name="Uranium-238", half_life=4.468e9, gamma_emission_probability=23, half_life_unit='y')
BISMUTH_193M = Isotope(name="Bismuth-193m", half_life=3.2, gamma_emission_probability=90, half_life_unit='s')