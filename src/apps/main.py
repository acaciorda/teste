import time
import argparse
from src.infra.logging import get_logger
from src.io.exchanges import BinanceClient
from src.core.arbitrage import find_tri_opportunity
from src.utils import telegram_alert

log = get_logger()
SYMBOLS = ["BTCUSDT", "ETHUSDT", "ETHBTC"]

def run_once(min_edge: float = 0.001, fee: float = 0.001) -> int:
    ex = BinanceClient()
    prices = ex.prices_best(SYMBOLS)
    if len(prices) != len(SYMBOLS):
        log.error("Faltam símbolos. Abortando loop.")
        return 1
    opp = find_tri_opportunity(prices, min_edge=min_edge, fee=fee)
    if opp:
        msg = f"[SIM] TRI-ARB edge={opp['edge']*100:.3f}% payout={opp['payout']:.6f} cycle={opp['name']}"
        log.info(msg)
        telegram_alert(msg)
    else:
        log.info("[SIM] Sem oportunidade acima do threshold.")
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="executa um único ciclo")
    ap.add_argument("--min_edge", type=float, default=0.001, help="lucro mínimo por ciclo (0.001=0.1%)")
    ap.add_argument("--fee", type=float, default=0.001, help="taker fee por perna (ex.: 0.001=0.1%)")
    args = ap.parse_args()

    if args.once:
        raise SystemExit(run_once(min_edge=args.min_edge, fee=args.fee))

    while True:
        try:
            run_once(min_edge=args.min_edge, fee=args.fee)
            time.sleep(2)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()