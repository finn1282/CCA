"""M7 — MSPO compliance knowledge base and coverage reasoner (O4, D28).

Maps each kind of evidence record to the MSPO MS 2530:2022 requirements it supports, then checks
which requirements a block has evidence for in a period. Criterion numbers are placeholders until
Research wave 2 (request R1b) returns the clause numbers; requirement themes follow [MPOCC-P21]
and [MSPO-EFI2025].
"""
from __future__ import annotations

# key → (short title, what evidence satisfies it, citation placeholder)
CRITERIA: dict[str, dict] = {
    "SOIL_FERTILITY": {"title": "Soil fertility monitoring & records",
                       "evidence": "Dated soil readings (pH, moisture, nutrient proxy) per block with calibration ID",
                       "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
    "FERTILISER_RECORDS": {"title": "Fertiliser application justified & recorded",
                           "evidence": "Fertilise / skip / lime decisions with the reason, approver and block",
                           "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
    "GHG_N2O": {"title": "GHG awareness — N₂O from fertiliser",
                "evidence": "Avoided or reduced fertiliser rounds (skip_fertiliser) logged per block",
                "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
    "PEST_DISEASE": {"title": "Pest & disease (Ganoderma) monitoring",
                     "evidence": "Screening results (satellite/drone/ground) and follow-up actions",
                     "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
    "HARVEST_QUALITY": {"title": "FFB harvesting standards / quality",
                        "evidence": "Ripeness grades at harvest with model version",
                        "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
    "TRACEABILITY": {"title": "Traceability & block geolocation",
                     "evidence": "Every record tied to an estate block ID (geolocated) — EUDR-ready",
                     "ref": "MS 2530:2022 [criterion TBC — R1b] (MSPO-EFI2025)"},
    "HUMAN_OVERSIGHT": {"title": "Management review of AI decisions",
                        "evidence": "Human approve/override records on AI recommendations",
                        "ref": "MS 2530:2022 [criterion TBC — R1b] (MPOCC-P21)"},
}


def criteria_for(kind: str, record: dict) -> list[str]:
    tags = ["TRACEABILITY"] if record.get("block_id") else []
    if kind == "soil_recommendation":
        tags.append("SOIL_FERTILITY")
        acts = {a["action"] for a in record.get("output", {}).get("actions", [])}
        if acts & {"fertilise", "skip_fertiliser", "lime"}:
            tags.append("FERTILISER_RECORDS")
        if "skip_fertiliser" in acts:
            tags.append("GHG_N2O")
    elif kind == "ripeness":
        tags.append("HARVEST_QUALITY")
    elif kind == "ganoderma_screening":
        tags.append("PEST_DISEASE")
    elif kind == "review":
        tags.append("HUMAN_OVERSIGHT")
    elif kind == "calibration":
        tags.append("SOIL_FERTILITY")
    return tags


def coverage(records: list[dict]) -> list[dict]:
    """records: evidence rows (with 'mspo' list). Returns per-criterion status."""
    out = []
    for key, c in CRITERIA.items():
        hits = [r for r in records if key in r["mspo"]]
        out.append({"criterion": key, **c, "records": len(hits),
                    "last": hits[-1]["created_at"] if hits else None,
                    "status": "evidenced" if hits else "gap"})
    return out
