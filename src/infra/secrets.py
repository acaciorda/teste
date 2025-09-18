import os
from io import StringIO
from typing import Dict
from cryptography.fernet import Fernet
from dotenv import load_dotenv, dotenv_values

ENV_PLAIN = ".env"
ENV_ENC = ".env.enc"

def generate_key() -> str:
    """Gera chave Fernet (base64 urlsafe)."""
    key = Fernet.generate_key().decode()
    print(key)
    return key

def encrypt_env(fernet_key: str, src: str = ENV_PLAIN, dst: str = ENV_ENC) -> None:
    """Criptografa .env → .env.enc."""
    if not os.path.exists(src):
        raise FileNotFoundError(f"{src} não encontrado")
    data = open(src, "rb").read()
    enc = Fernet(fernet_key.encode()).encrypt(data)
    open(dst, "wb").write(enc)

def decrypt_env_to_osenv(fernet_key: str, enc_path: str = ENV_ENC) -> Dict[str, str]:
    """Descriptografa .env.enc e carrega para os.environ. Retorna dict."""
    if not os.path.exists(enc_path):
        raise FileNotFoundError(f"{enc_path} não encontrado")
    dec = Fernet(fernet_key.encode()).decrypt(open(enc_path, "rb").read()).decode()
    buf = StringIO(dec)
    load_dotenv(stream=buf, override=True)
    # também retorna como dict
    return dict(dotenv_values(stream=StringIO(dec)))