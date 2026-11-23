"""SQLite storage for the demo build (production target: Cosmos DB / ADLS Gen2, see 07)."""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timedelta, timezone

from . import config as C

_lock = threading.RLock()
_conn: sqlite3.Connection | None = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT NOT NULL, block_id TEXT, seq INTEGER, ts TEXT, received_at TEXT NOT NULL, captured_at TEXT,
  buffered INTEGER DEFAULT 0, payload TEXT NOT NULL, recommendation TEXT, evidence_id TEXT, response TEXT
);
CREATE INDEX IF NOT EXISTS ix_readings_dev ON readings(device_id, id);
CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY, tds_baseline REAL, tds_margin REAL, cal_id TEXT, updated_at TEXT,
  last_seen TEXT, last_rssi INTEGER, fw_version TEXT
);
CREATE TABLE IF NOT EXISTS commands (
  id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT NOT NULL, cmd TEXT NOT NULL,
  created_at TEXT NOT NULL, consumed_at TEXT
);
CREATE TABLE IF NOT EXISTS evidence (
  id INTEGER PRIMARY KEY AUTOINCREMENT, evidence_id TEXT UNIQUE, created_at TEXT NOT NULL,
  kind TEXT NOT NULL, device_id TEXT, block_id TEXT, record TEXT NOT NULL,
  mspo TEXT NOT NULL, prev_hash TEXT NOT NULL, hash TEXT NOT NULL
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def conn() -> sqlite3.Connection:
    global _conn
    with _lock:
        if _conn is None:
            C.ensure_dirs()
            _conn = sqlite3.connect(C.DB_PATH, check_same_thread=False, isolation_level=None)
            _conn.row_factory = sqlite3.Row
            _conn.execute("PRAGMA journal_mode=WAL")
            _conn.executescript(SCHEMA)
            cols = {r[1] for r in _conn.execute("PRAGMA table_info(readings)")}
            if "captured_at" not in cols:   # migrate DBs created before v0.2.2
                _conn.execute("ALTER TABLE readings ADD COLUMN captured_at TEXT")
            if "response" not in cols:      # v0.2.3 idempotency
                _conn.execute("ALTER TABLE readings ADD COLUMN response TEXT")
            _conn.execute("CREATE INDEX IF NOT EXISTS ix_readings_seq ON readings(device_id, seq)")
        return _conn


def shift(iso: str, seconds: int) -> str:
    t = datetime.fromisoformat(iso.replace("Z", "+00:00")) + timedelta(seconds=seconds)
    return t.isoformat(timespec="seconds").replace("+00:00", "Z")


def reset_for_tests(path) -> None:
    global _conn
    with _lock:
        if _conn is not None:
            _conn.close()
        _conn = None
        C.DB_PATH = path


def q(sql: str, args: tuple = ()) -> list[sqlite3.Row]:
    with _lock:
        return conn().execute(sql, args).fetchall()


def x(sql: str, args: tuple = ()) -> int:
    with _lock:
        cur = conn().execute(sql, args)
        return cur.lastrowid


def get_device(device_id: str) -> dict:
    rows = q("SELECT * FROM devices WHERE device_id=?", (device_id,))
    return dict(rows[0]) if rows else {"device_id": device_id, "tds_baseline": None, "tds_margin": None, "cal_id": None}


def touch_device(device_id: str, rssi=None, fw=None) -> None:
    x("""INSERT INTO devices(device_id, last_seen, last_rssi, fw_version) VALUES(?,?,?,?)
         ON CONFLICT(device_id) DO UPDATE SET last_seen=excluded.last_seen,
         last_rssi=COALESCE(excluded.last_rssi, devices.last_rssi), fw_version=COALESCE(excluded.fw_version, devices.fw_version)""",
      (device_id, now(), rssi, fw))


def set_calibration(device_id: str, baseline: float, margin: float, cal_id: str) -> None:
    x("""INSERT INTO devices(device_id, tds_baseline, tds_margin, cal_id, updated_at) VALUES(?,?,?,?,?)
         ON CONFLICT(device_id) DO UPDATE SET tds_baseline=excluded.tds_baseline, tds_margin=excluded.tds_margin,
         cal_id=excluded.cal_id, updated_at=excluded.updated_at""", (device_id, baseline, margin, cal_id, now()))


def dumps(o) -> str:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
