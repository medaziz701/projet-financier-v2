# -*- coding: utf-8 -*-
from main import nombre_en_lettres_avec_millimes

CASES = [
    "0",
    "0.500",
    "12.000",
    "65.000",
    "1234.567",
    "-5.250",
    0,
    0.5,
    12.0,
    65.0,
    1234.567,
    -5.25,
]

if __name__ == "__main__":
    print("=== Tests conversion montants en lettres ===")
    for case in CASES:
        try:
            result = nombre_en_lettres_avec_millimes(case)
            print(f"Input: {repr(case):>10} -> {result}")
        except Exception as e:
            print(f"Input: {repr(case):>10} -> ERROR: {e}")
