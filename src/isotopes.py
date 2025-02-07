from dataclasses import dataclass

@dataclass
class Isotope:
    name: str
    half_life: float
    half_life_unit: str                     # s, d, or y

CARBON_14 = Isotope(name="Carbon-14", half_life=5730, half_life_unit='y')
IODINE_131 = Isotope(name="Iodine-131", half_life=8.02, half_life_unit='d')
URANIUM_238 = Isotope(name="Uranium-238", half_life=4.468e9, half_life_unit='y')