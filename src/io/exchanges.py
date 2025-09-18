from binance.client import Client
from src.infra.logging import get_logger
from src.infra.audit import audit, sha256
import os

log = get_logger()

def _mask(k: str, tail: int = 4) -> str:
    if not k:
        return ""
    if len(k) <= tail + 2:
        return "*" * len(k)
    return k[:2] + "*" * (len(k) - tail - 2) + k[-tail:]

class BinanceClient:
    """Cliente REST. Usa testnet se BINANCE_TESTNET='true'."""
    def __init__(self) -> None:
        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        testnet = str(os.getenv("BINANCE_TESTNET", "true")).lower() == "true"

        if api_key:
            log.info(f"[audit] Binance API key usada: {_mask(api_key)} | testnet={testnet}")
        else:
            log.warning("[audit] Binance sem API key. Usando endpoints públicos.")

        self.client = Client(api_key or None, api_secret or None, testnet=testnet)

        # Auditoria de inicialização
        audit(
            "binance_client_init",
            testnet=testnet,
            api_key_mask=_mask(api_key),
            api_key_sha256=sha256(api_key),
            has_secret=bool(api_secret),
        )

    def prices_best(self, symbols: list[str]) -> dict:
        """{symbol: {'bid': float, 'ask': float}} via /ticker/bookTicker"""
        want = set(symbols)
        out: dict[str, dict[str, float]] = {}
        for t in self.client.get_orderbook_ticker():
            s = t["symbol"]
            if s in want:
                out[s] = {"bid": float(t["bidPrice"]), "ask": float(t["askPrice"])}
        missing = want - out.keys()
        if missing:
            log.warning(f"Tickers ausentes: {sorted(missing)}")
            audit("missing_tickers", missing=sorted(missing))
        else:
            audit("prices_best_ok", count=len(out))
        return out