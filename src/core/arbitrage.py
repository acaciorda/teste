from src.infra.logging import get_logger

log = get_logger()

# Ciclos fixos: BTCUSDT, ETHUSDT, ETHBTC
def _cycle_usdt_eth_btc_usdt(p: dict, fee: float) -> dict:
    usdt = 1.0
    eth  = (usdt / p["ETHUSDT"]["ask"]) * (1 - fee)
    btc  =  eth * p["ETHBTC"]["bid"]    * (1 - fee)
    usdt2=  btc * p["BTCUSDT"]["bid"]   * (1 - fee)
    return {"name":"USDT->ETH->BTC->USDT", "payout": usdt2, "edge": usdt2 - 1.0}

def _cycle_usdt_btc_eth_usdt(p: dict, fee: float) -> dict:
    usdt = 1.0
    btc  = (usdt / p["BTCUSDT"]["ask"]) * (1 - fee)
    eth  =  btc / p["ETHBTC"]["ask"]    * (1 - fee)
    usdt2=  eth * p["ETHUSDT"]["bid"]   * (1 - fee)
    return {"name":"USDT->BTC->ETH->USDT", "payout": usdt2, "edge": usdt2 - 1.0}

def find_tri_opportunity(prices: dict, min_edge: float = 0.001, fee: float = 0.001):
    """Retorna a melhor oportunidade se edge > min_edge, senão None."""
    for s in ("BTCUSDT","ETHUSDT","ETHBTC"):
        if s not in prices:
            log.error(f"Preço ausente: {s}")
            return None
    a = _cycle_usdt_eth_btc_usdt(prices, fee)
    b = _cycle_usdt_btc_eth_usdt(prices, fee)
    best = a if a["edge"] >= b["edge"] else b
    if best["edge"] > min_edge:
        return best
    return None