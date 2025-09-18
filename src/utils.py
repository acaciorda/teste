import os
import requests
from src.infra.logging import get_logger

log = get_logger()

def mask(s: str) -> str:
    if not s:
        return ""
    return f"{s[:4]}...{s[-4:]}"

def telegram_alert(text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        log.warning("Telegram não configurado. Alerta ignorado.")
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text, "disable_web_page_preview": True})
        if r.status_code == 200:
            log.info("Alerta Telegram enviado.")
            return True
        log.error(f"Telegram falhou {r.status_code}: {r.text}")
        return False
    except Exception as e:
        log.exception(f"Erro Telegram: {e}")
        return False