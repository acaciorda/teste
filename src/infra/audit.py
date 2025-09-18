import os, hashlib
from datetime import datetime, timezone
from typing import Dict
import orjson
from loguru import logger

LOG_DIR = os.path.join("src", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
AUDIT_PATH = os.path.join(LOG_DIR, "audit.jsonl")
SNAP_PATH  = os.path.join(LOG_DIR, "config_snapshot.json")

def _now():
    return datetime.now(timezone.utc).isoformat()

def sha256(s: str | None) -> str | None:
    if not s:
        return None
    return hashlib.sha256(s.encode()).hexdigest()

def mask(s: str | None, tail: int = 4) -> str:
    if not s:
        return ""
    if len(s) <= tail + 2:
        return "*" * len(s)
    return s[:2] + "*" * (len(s) - tail - 2) + s[-tail:]

def _write_audit(obj: Dict):
    with open(AUDIT_PATH, "ab") as f:
        f.write(orjson.dumps(obj) + b"\n")

def audit(event: str, **meta):
    rec = {"ts": _now(), "event": event, **meta}
    _write_audit(rec)
    logger.info(f"[audit] {event} { {k:v for k,v in meta.items() if 'secret' not in k.lower()} }")

KEYS = ["BINANCE_API_KEY","BINANCE_API_SECRET","TELEGRAM_BOT_TOKEN","TELEGRAM_CHAT_ID","ETH_RPC_URL"]

def config_snapshot()->Dict[str, Dict[str,str|None]]:
    snap = {}
    for k in KEYS:
        val = os.getenv(k)
        if val is None:
            continue
        snap[k] = {"mask": mask(val), "sha256": sha256(val)}
    return snap

def audit_config_snapshot():
    snap = config_snapshot()
    audit("config_snapshot", snapshot=snap)
    with open(SNAP_PATH, "wb") as f:
        f.write(orjson.dumps(snap))

def audit_config_changes():
    new = config_snapshot()
    old = {}
    if os.path.exists(SNAP_PATH):
        old = orjson.loads(open(SNAP_PATH,"rb").read())
    # compara por sha256
    for k, meta in new.items():
        prev = (old.get(k) or {}).get("sha256")
        cur  = meta.get("sha256")
        if prev != cur:
            audit("config_changed", key=k, from_sha=prev, to_sha=cur, mask=new[k]["mask"])
    with open(SNAP_PATH, "wb") as f:
        f.write(orjson.dumps(new))