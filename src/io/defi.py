from web3 import Web3
from src.infra.logging import get_logger
from src.infra.audit import audit
import os
from typing import Optional, Tuple

log = get_logger()

# Endereços oficiais em Arbitrum
WETH  = Web3.to_checksum_address("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1")  # Uniswap docs
USDC  = Web3.to_checksum_address("0xAf88d065e77c8CC2239327C5EDb3A432268e5831")  # USDC nativo (Circle)
USDCe = Web3.to_checksum_address("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8")  # USDC.e (bridged)
QUOTER_V2 = Web3.to_checksum_address("0x61fFE014bA17989E743c5F6cB21bF9697530B21e")  # Uniswap QuoterV2

ABI_QUOTER_V2 = [{
    "inputs":[{"components":[
        {"internalType":"address","name":"tokenIn","type":"address"},
        {"internalType":"address","name":"tokenOut","type":"address"},
        {"internalType":"uint24","name":"fee","type":"uint24"},
        {"internalType":"uint256","name":"amountIn","type":"uint256"},
        {"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}
    ],"internalType":"struct IQuoterV2.QuoteExactInputSingleParams","name":"params","type":"tuple"}],
    "name":"quoteExactInputSingle",
    "outputs":[
        {"internalType":"uint256","name":"amountOut","type":"uint256"},
        {"internalType":"uint160","name":"sqrtPriceX96After","type":"uint160"},
        {"internalType":"uint32","name":"initializedTicksCrossed","type":"uint32"},
        {"internalType":"uint256","name":"gasEstimate","type":"uint256"}
    ],
    "stateMutability":"nonpayable","type":"function"
}]

def _w3() -> Optional[Web3]:
    url = os.getenv("ETH_RPC_URL", "")
    if not url:
        log.warning("ETH_RPC_URL ausente. DeFi desativado.")
        return None
    w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout":10}))
    if not w3.is_connected():
        log.error("Falha ao conectar no RPC Arbitrum.")
        return None
    return w3

def uniswap_v3_weth_usdc_arbitrum(amount_weth: float = 1.0) -> Optional[dict]:
    """
    Usa QuoterV2 para cotar 1 WETH -> USDC em Arbitrum.
    Testa nativo USDC e USDC.e e fees 0.05% (500) e 0.3% (3000). Retorna o melhor.
    """
    w3 = _w3()
    if not w3:
        return None
    q = w3.eth.contract(address=QUOTER_V2, abi=ABI_QUOTER_V2)
    amount_in = int(amount_weth * 10**18)

    candidates = [(USDC, 500), (USDC, 3000), (USDCe, 500), (USDCe, 3000)]
    best: Tuple[int, str, int] | None = None  # (amountOut, tokenOut, fee)

    for token_out, fee in candidates:
        try:
            amount_out, _, _, _ = q.functions.quoteExactInputSingle((
                WETH, token_out, fee, amount_in, 0
            )).call()
            if best is None or amount_out > best[0]:
                best = (amount_out, token_out, fee)
        except Exception as e:
            log.warning(f"Quoter falhou para fee={fee} token={token_out}: {e}")

    if best is None:
        log.error("Nenhuma cotação retornada pelo Quoter.")
        return None

    amount_usdc = best[0] / 10**6  # USDC e USDC.e têm 6 casas
    audit("defi_uniswap_v3_quote",
          chain="arbitrum",
          amount_in_weth=amount_weth,
          token_out="USDC" if best[1] == USDC else "USDC.e",
          fee=best[2],
          usdc_out=amount_usdc)
    log.info(f"[DeFi] UniswapV3 Arbitrum: 1 WETH ≈ {amount_usdc:.4f} {'USDC' if best[1]==USDC else 'USDC.e'} @ fee {best[2]}")
    return {"price_usdc_per_weth": amount_usdc, "token_out": ("USDC" if best[1]==USDC else "USDC.e"), "fee": best[2]}