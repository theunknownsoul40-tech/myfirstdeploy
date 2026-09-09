from __future__ import annotations

import re

# Jurisdiction-aware rules. Extend this registry as verified government/source
# conventions are added; ambiguous historical units must not be guessed.
CONVERSIONS = {
    "maharashtra": {
        "guntha": (0.0101171411, "hectare", "Maharashtra_guntha_v1"),
        "acre": (0.4046856422, "hectare", "international_acre_v1"),
        "hectare": (1.0, "hectare", "si_hectare_v1"),
        "sq metre": (0.0001, "hectare", "si_square_metre_v1"),
        "square metre": (0.0001, "hectare", "si_square_metre_v1"),
        "cent": (0.0040468564, "hectare", "international_cent_v1"),
    }
}


def _canonical_unit(unit: str) -> str:
    value = unit.strip().lower().replace(".", "")
    aliases = {
        "g": "guntha", "gunthas": "guntha", "gunta": "guntha",
        "ac": "acre", "acres": "acre", "ha": "hectare", "hectares": "hectare",
        "sqm": "sq metre", "sq m": "sq metre", "m²": "sq metre",
        "cents": "cent",
    }
    return aliases.get(value, value)


def normalize_area(text: str, jurisdiction: str | None = None) -> dict:
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*([A-Za-z² ]+)", text)
    if not match:
        raise ValueError(f"Could not parse area: {text!r}")

    value = float(match.group(1).replace(",", ""))
    unit = _canonical_unit(match.group(2))
    rules = CONVERSIONS.get((jurisdiction or "").strip().lower(), {})

    if unit not in rules:
        return {
            "original_value": value,
            "original_unit": unit,
            "original_text": text,
            "standard_area": None,
            "standard_area_unit": "hectare",
            "conversion_rule": None,
            "conversion_confidence": 0.0,
            "requires_review": True,
        }

    factor, standard_unit, rule = rules[unit]
    return {
        "original_value": value,
        "original_unit": unit,
        "original_text": text,
        "standard_area": round(value * factor, 10),
        "standard_area_unit": standard_unit,
        "conversion_rule": rule,
        "conversion_confidence": 1.0,
        "requires_review": False,
    }
