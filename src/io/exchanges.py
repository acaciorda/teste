from binance.client import Client
from src.infra.logging import get_logger
import os

log = get_logger()

def _mask(k: str, tail: int = 4) -> str:
    if not k:
        return ""
    if len(k) <= tail + 2:
        return "*" * len(k)
    return k[:2] + "*" * (len(k) - tail - 2) + k[-tail:]

class BinanceClient:
    """Cliente simples p/ REST. Usa testnet se BINANCE_TESTNET='true'."""
    def __init__(self) -> None:
        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        testnet = str(os.getenv("BINANCE_TESTNET", "true")).lower() == "true"

        if api_key:
            log.info(f"[audit] Binance API key usada: { _mask(api_key) } | testnet={testnet}")
        else:
            log.warning("[audit] Binance sem API key. Usando apenas endpoints públicos.")

        self.client = Client(api_key or None, api_secret or None, testnet=testnet)

    def prices_best(self, symbols: list[str]) -> dict:
        """Retorna {symbol: {'bid': float, 'ask': float}} usando /ticker/bookTicker."""
        want = set(symbols)
        out = {}
        for t in self.client.get_orderbook_ticker():
            s = t["symbol"]
            if s in want:
                out[s] = {"bid": float(t["bidPrice"]), "ask": float(t["askPrice"])}
        missing = want - out.keys()
        if missing:
            log.warning(f"Tickers ausentes: {sorted(missing)}")
        return out