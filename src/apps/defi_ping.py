from src.infra.logging import get_logger
from src.infra.config import load_config
from src.io.defi import uniswap_v3_weth_usdc_arbitrum

log = get_logger()

def main():
    load_config()
    result = uniswap_v3_weth_usdc_arbitrum(1.0)
    if not result:
        log.warning("DeFi ping falhou. Verifique ETH_RPC_URL.")
        return
    log.info(f"Preço: {result['price_usdc_per_weth']:.4f} {result['token_out']} (fee {result['fee']})")

if __name__ == "__main__":
    main()