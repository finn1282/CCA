"""Explain-to-audit evidence log (D18, D28).

Every AI decision is appended as a record (inputs, outputs, model version, explanation,
counterfactual, block, MSPO criteria). Records are chained with SHA-256: each hash covers the
record plus the previous hash, so editing or deleting any past record breaks verification.
Production target: Azure Confidential Ledger (see 04_cloud_design.md); this is the demo equivalent.
Reviews (approve/override) are new records that reference the original — nothing is mutated.
"""
from __future__ import annotations

import hashlib
import json

from . import compliance, db

GENESIS = "0" * 64


def _digest(prev_hash: str, body: dict) -> str:
    return hashlib.sha256((prev_hash + db.dumps(body)).encode()).hexdigest()


def append(kind: str, record: dict, device_id: str | None = None, block_id: str | None = None) -> str:
    record = {**record, "block_id": block_id}
    mspo = compliance.criteria_for(kind, record)
    with db._lock:
        last = db.q("SELECT id, hash FROM evidence ORDER BY id DESC LIMIT 1")
        next_id = (last[0]["id"] + 1) if last else 1
        prev = last[0]["hash"] if last else GENESIS
        evidence_id = f"ev_{next_id:06d}"
        created = db.now()
        body = {"evidence_id": evidence_id, "created_at": created, "kind": kind, "device_id": device_id,
                "block_id": block_id, "record": record, "mspo": mspo}
        h = _digest(prev, body)
        db.x("INSERT INTO evidence(id, evidence_id, created_at, kind, device_id, block_id, record, mspo, prev_hash, hash)"
             " VALUES(?,?,?,?,?,?,?,?,?,?)",
             (next_id, evidence_id, created, kind, device_id, block_id, db.dumps(record), db.dumps(mspo), prev, h))
    return evidence_id


def _row(r) -> dict:
    return {"evidence_id": r["evidence_id"], "created_at": r["created_at"], "kind": r["kind"],
            "device_id": r["device_id"], "block_id": r["block_id"], "record": json.loads(r["record"]),
            "mspo": json.loads(r["mspo"]), "prev_hash": r["prev_hash"], "hash": r["hash"]}


def get(evidence_id: str) -> dict | None:
    rows = db.q("SELECT * FROM evidence WHERE evidence_id=?", (evidence_id,))
    return _row(rows[0]) if rows else None


def listing(limit: int = 50, block_id: str | None = None, kind: str | None = None,
            non_ok: bool = False, since: str | None = None) -> list[dict]:
    sql, args = "SELECT * FROM evidence WHERE 1=1", []
    if block_id:
        sql += " AND block_id=?"; args.append(block_id)
    if kind:
        sql += " AND kind=?"; args.append(kind)
    if since:
        sql += " AND created_at>=?"; args.append(since)
    if non_ok:
        sql += " AND NOT (kind='soil_recommendation' AND json_extract(record,'$.output.action')='ok')"
    sql += " ORDER BY id DESC LIMIT ?"; args.append(limit)
    return [_row(r) for r in db.q(sql, tuple(args))]


def verify() -> dict:
    prev, n = GENESIS, 0
    for r in db.q("SELECT * FROM evidence ORDER BY id"):
        e = _row(r)
        body = {k: e[k] for k in ("evidence_id", "created_at", "kind", "device_id", "block_id", "record", "mspo")}
        if e["prev_hash"] != prev or _digest(prev, body) != e["hash"]:
            return {"ok": False, "checked": n, "first_bad": e["evidence_id"],
                    "message": f"Chain broken at {e['evidence_id']} — record edited or removed after it was written"}
        prev, n = e["hash"], n + 1
    return {"ok": True, "checked": n, "head": prev, "message": f"All {n} records intact (SHA-256 chain)"}


def reviews_for(evidence_id: str) -> list[dict]:
    rows = db.q("SELECT * FROM evidence WHERE kind='review' AND json_extract(record,'$.target')=? ORDER BY id",
                (evidence_id,))
    return [_row(r) for r in rows]


def audit_pack(block_id: str | None = None, since: str | None = None) -> str:
    """Markdown MSPO audit pack: chain status, criterion coverage, decision table."""
    rows = list(reversed(listing(limit=100000, block_id=block_id, since=since)))
    v = verify()
    cov = compliance.coverage(rows)
    lines = [f"# SawitSense — MSPO evidence pack{' — block ' + block_id if block_id else ''}",
             "", f"Generated {db.now()} · records: {len(rows)} · chain: {'VERIFIED' if v['ok'] else 'BROKEN'} — {v['message']}",
             "", "## MSPO criterion coverage", "", "| Criterion | Requirement | Records | Last | Status | Reference |",
             "|---|---|---|---|---|---|"]
    for c in cov:
        lines.append(f"| {c['criterion']} | {c['title']} | {c['records']} | {c['last'] or '—'} | {c['status']} | {c['ref']} |")
    lines += ["", "## Decisions (non-routine)", "", "| Evidence | Time (UTC) | Block | Kind | Decision | Reason | Simulated | Hash (first 12) |",
              "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out = r["record"].get("output", {})
        if r["kind"] == "soil_recommendation" and out.get("action") == "ok":
            continue
        decision = out.get("action") or out.get("label") or r["record"].get("decision", "")
        reason = (out.get("reason") or out.get("explanation") or r["record"].get("note", "")).replace("|", "/")
        lines.append(f"| {r['evidence_id']} | {r['created_at']} | {r['block_id'] or '—'} | {r['kind']} | {decision} | "
                     f"{reason} | {'yes' if out.get('simulated') else 'no'} | `{r['hash'][:12]}` |")
    routine = sum(1 for r in rows if r["kind"] == "soil_recommendation" and r["record"].get("output", {}).get("action") == "ok")
    lines += ["", f"Routine 'ok' soil checks logged: {routine} (full detail via `/api/v1/evidence`).",
              "", "_Fertiliser decisions marked 'Simulated' use simulated agronomy thresholds (labelled per SPEC §4)._"]
    return "\n".join(lines)
