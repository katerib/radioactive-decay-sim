# Natural Decay Series
URANIUM_238_SERIES = {
    "U-238", "Th-234", "Pa-234m", "U-234", "Th-230", "Ra-226", 
    "Rn-222", "Po-218", "Pb-214", "Bi-214", "Po-214", "Pb-210", 
    "Bi-210", "Po-210", "Pb-206"
}

THORIUM_232_SERIES = {
    "Th-232", "Ra-228", "Ac-228", "Th-228", "Ra-224", "Rn-220",
    "Po-216", "Pb-212", "Bi-212", "Po-212", "Pb-208"
}

URANIUM_235_SERIES = {
    "U-235", "Th-231", "Pa-231", "Ac-227", "Th-227", "Ra-223",
    "Rn-219", "Po-215", "Pb-211", "Bi-211", "Tl-207", "Pb-207"
}

NEPTUNIUM_237_SERIES = {
    "Np-237", "Pa-233", "U-233", "Th-229", "Ra-225", "Ac-225",
    "Fr-221", "At-217", "Bi-213", "Po-213", "Pb-209", "Bi-209"
}

# Medical / Industrial
MEDICAL_ISOTOPES = {
    "I-131", "Tc-99m", "Co-60", "Cs-137", "Sr-90", "P-32",
    "Y-90", "Mo-99", "Lu-177", "Ir-192"
}

# Major Fission Products
FISSION_PRODUCTS = {
    "Cs-137", "Sr-90", "I-131", "Xe-133", "Kr-85", "Ru-106",
    "Ce-144", "Zr-95"
}

TARGET_ISOTOPES = (
    URANIUM_238_SERIES | THORIUM_232_SERIES | URANIUM_235_SERIES |
    NEPTUNIUM_237_SERIES | MEDICAL_ISOTOPES | FISSION_PRODUCTS
)