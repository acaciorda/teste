from loguru import logger
import os, sys

# Diretório de logs
LOG_DIR = os.path.join("src", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "arb-bot.log")

# Configuração dos handlers
logger.remove()  # remove default
logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False)
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    level="INFO"
)

def get_logger():
    """Retorna instância configurada do logger"""
    return logger