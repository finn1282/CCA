"""M7 — MSPO compliance knowledge base and coverage reasoner (O4, D28).

Maps each kind of evidence record to the MSPO clauses it supports: MS 2530-3-2:2022 for
estates > 500 ha [MPOCC-P32] and MS 2530-4-1:2022 for mills [MPOCC-P41] (clause numbers per MPOCC guidance, research file 06 §b), then checks which clauses a
block has evidence for in a period.
"""
from __future__ import annotations

# key → (short title, what evidence satisfies it, citation placeholder)
CRITERIA: dict[str, dict] = {
    "SOIL_FERTILITY": {"title": "SOP records: soil-fertility management",
                       "evidence": "Dated soil readings (pH, moisture, nutrient proxy) per block with calibration ID",
                       "ref": "MS 2530-3-2:2022 4.1.3.1 (MPOCC-P32)"},
    "FERTILISER_RECORDS": {"title": "SOP records: fertilising",
                           "evidence": "Fertilise / skip / lime decisions with the reason, approver and block",
                           "ref": "MS 2530-3-2:2022 4.1.3.1 (MPOCC-P32)"},
    "GHG_N2O": {"title": "GHG emissions — N₂O from fertiliser",
                "evidence": "Avoided or reduced fertiliser rounds (skip_fertiliser) logged per block",
                "ref": "MS 2530-3-2:2022 4.5.4; MS 2530-4-1:2022 4.5.4 (mills) (MPOCC-P32; MPOCC-P41)"},
    "PEST_DISEASE": {"title": "Integrated Pest Management (Ganoderma)",
                     "evidence": "Screening results (satellite/drone/ground) and follow-up actions",
                     "ref": "MS 2530-3-2:2022 4.1.3.5 (MPOCC-P32)"},
    "HARVEST_QUALITY": {"title": "SOP records: FFB harvesting",
                        "evidence": "Ripeness grades at harvest with model version",
                        "ref": "MS 2530-3-2:2022 4.1.3.1 (MPOCC-P32)"},
    "TRACEABILITY": {"title": "Traceability + block reference system",
                     "evidence": "Every record tied to an estate block ID (geolocated) — EUDR-ready",
                     "ref": "MS 2530-3-2:2022 4.2.2, 4.1.3.4; MS 2530-4-1:2022 4.2.2 (mill traceability) (MPOCC-P32; MPOCC-P41)"},
    "WATER_MGMT": {"title": "Water resources management",
                   "evidence": "Irrigation / drainage advice logged per block",
                   "ref": "MS 2530-3-2:2022 4.5.5 (MPOCC-P32)"},
    "HUMAN_OVERSIGHT": {"title": "Management review of AI decisions",
                        "evidence": "Human approve/override records on AI recommendations",
                        "ref": "MS 2530-3-2:2022 4.1.3 — records of implementation (MPOCC-P32)"},
}


def criteria_for(kind: str, record: dict) -> list[str]:
    tags = ["TRACEABILITY"] if record.get("block_id") else []
    if kind == "soil_recommendation":
        tags.append("SOIL_FERTILITY")
        acts = {a["action"] for a in record.get("output", {}).get("actions", [])}
        if acts & {"fertilise", "skip_fertiliser", "lime"}:
            tags.append("FERTILISER_RECORDS")
        if "skip_fertiliser" in acts or "fertilise" in acts:
            tags.append("GHG_N2O")
        if acts & {"irrigate", "drain"}:
            tags.append("WATER_MGMT")
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
