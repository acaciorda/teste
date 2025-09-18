from src.infra.logging import get_logger
from src.infra.config import load_config
import os

log = get_logger()

def main():
    cfg = load_config()
    log.info("Sanity boot")
    log.info(f"BINANCE_TESTNET={os.getenv('BINANCE_TESTNET')}")
    log.info(f"Telegram set? token={bool(os.getenv('TELEGRAM_BOT_TOKEN'))}, chat_id={bool(os.getenv('TELEGRAM_CHAT_ID'))}")
    log.info(f"Chaves Binance set? key={bool(os.getenv('BINANCE_API_KEY'))}, secret={bool(os.getenv('BINANCE_API_SECRET'))}")
    log.info("OK: logging + config operando.")

if __name__ == "__main__":
    main()