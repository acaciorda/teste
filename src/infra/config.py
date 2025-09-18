import os
from typing import Dict
from dotenv import load_dotenv, dotenv_values
from .secrets import decrypt_env_to_osenv, ENV_ENC

def load_config() -> Dict[str, str]:
    """
    Prioridade:
    1) Se existir .env → carrega e retorna.
    2) Se existir .env.enc → requer FERNET_KEY no ambiente, decripta e retorna.
    3) Senão, retorna {}.
    """
    if os.path.exists(".env"):
        load_dotenv(".env", override=True)
        return dict(dotenv_values(".env"))

    if os.path.exists(ENV_ENC):
        key = os.getenv("FERNET_KEY")
        if not key:
            raise RuntimeError("FERNET_KEY ausente para descriptografar .env.enc")
        return decrypt_env_to_osenv(key)

    return {}