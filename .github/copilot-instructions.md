# Copilot Instructions for arb-bot

## Visão Geral
Este projeto é um bot de arbitragem para exchanges de criptomoedas, com foco em performance, segurança e integração com APIs de mercado. O código está organizado para facilitar extensões e manutenção, priorizando componentes assíncronos e uso de tipagem forte.

## Estrutura Principal
- O diretório raiz contém apenas arquivos de configuração (`requirements.txt`, `.gitignore`).
- O código-fonte e módulos principais devem estar em subdiretórios como `src/` (não presente, mas referenciado em `.gitignore`).
- Logs são salvos em `src/logs/` ou `logs/`.
- Variáveis de ambiente são gerenciadas via `.env` e `python-dotenv`.

## Dependências e Integrações
- Exchanges: `python-binance`, `websockets`, `requests`.
- Configuração e segurança: `python-dotenv`, `cryptography`, `pydantic`.
- Logging: `loguru`, serialização rápida com `orjson`.
- Performance: `numpy`, `numba`.
- Async: `aiohttp`, `uvloop` (exceto Windows).

## Convenções e Padrões
- Use tipagem forte com `pydantic` para validação de dados.
- Prefira logging com `loguru` para rastreamento detalhado.
- Serialização de dados deve usar `orjson`.
- Configurações sensíveis devem estar em `.env` (nunca versionar `.env`, use `.env.sample` para exemplos).
- Testes e caches são ignorados conforme `.gitignore`.

## Fluxos de Desenvolvimento
- Instale dependências com: `pip install -r requirements.txt`.
- Configure variáveis de ambiente em `.env`.
- Para rodar o bot, execute o módulo principal (exemplo: `python src/main.py`).
- Logs detalhados são gerados automaticamente.
- Para testes, utilize frameworks compatíveis (ex: `pytest`).

## Exemplos de Integração
- Para conectar à Binance:
  ```python
  from binance import Client
  client = Client(api_key, api_secret)
  ```
- Para carregar variáveis de ambiente:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
- Para logging:
  ```python
  from loguru import logger
  logger.info('Mensagem de log')
  ```

## Observações
- O projeto está preparado para rodar em ambientes Windows, mas algumas otimizações (ex: `uvloop`) são desabilitadas.
- Sempre consulte o `.gitignore` para evitar versionar arquivos sensíveis ou desnecessários.
- Estruture novos módulos em subdiretórios e siga os padrões de tipagem e logging.

---

Seções incompletas ou dúvidas sobre fluxos específicos? Informe para que as instruções sejam aprimoradas.