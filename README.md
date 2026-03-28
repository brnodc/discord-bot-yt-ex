# Discord bot — alertas de Implied APY (Exponent)

Bot em Python que consulta periodicamente a página da Exponent Finance (via Playwright), lê o **Implied APY** do produto configurado e envia mensagens a um **canal do Discord** quando o APY cruza limiares de compra ou venda.

## O que faz

- A cada intervalo (por defeito 60 segundos), abre a URL alvo e extrai o APY.
- Se o APY for **≤ limiar de compra** ou **≥ limiar de venda**, e o valor tiver mudado face ao último alerta desse tipo, publica um aviso no canal.
- Evita spam ao só notificar quando o APY notificado muda dentro da mesma zona (compra/venda).

## Requisitos

- Python 3.10+ (usa `float | None` no scraper)
- Conta Discord com [aplicação de bot](https://discord.com/developers/applications) e token de bot
- Bot adicionado ao servidor com permissão para **ver o canal** e **enviar mensagens** nesse canal

## Configuração

### 1. Variáveis de ambiente (ficheiro `.env`)

Copie o modelo e edite:

```bash
copy .env.example .env
```

No `.env`, use o formato **chave=valor** (sem espaços à volta do `=`). O ficheiro `.env` está no `.gitignore` e **não** deve ser commitado.

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `BOT_TOKEN` | Sim | Token do bot (Discord Developer Portal → Bot → Reset / copiar token). |
| `CHANNEL_ID` | Sim | ID numérico do canal onde o bot envia alertas (modo desenvolvedor no Discord → copiar ID do canal). |
| `TARGET_URL` | Não | URL da página Exponent a analisar. Se omitir, usa o valor por defeito no código. |

Opcionalmente pode definir as mesmas variáveis no painel do Heroku/Railway/etc., em vez de usar `.env`.

### 2. Como o `.env` é carregado

O script usa [python-dotenv](https://pypi.org/project/python-dotenv/): `load_dotenv()` é chamado com o caminho do ficheiro `.env` **na mesma pasta que `discord-yt-bot.py`**, para funcionar mesmo que corra o programa a partir de outra pasta.

### 3. Limiares e intervalo (código)

Em `discord-yt-bot.py` pode ajustar:

- `CHECK_INTERVAL_SECONDS` — frequência das verificações  
- `APY_BUY_THRESHOLD` / `APY_SELL_THRESHOLD` — limiares de alerta  

## Instalação

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Execução local

```bash
python discord-yt-bot.py
```

## Deploy (Heroku)

O repositório inclui um `Procfile` com `worker: python discord-yt-bot.py`. Defina `BOT_TOKEN` e `CHANNEL_ID` nas config vars e garanta que o build instala dependências e browsers do Playwright conforme a documentação da plataforma.

## Estrutura do projeto

| Ficheiro | Função |
|----------|--------|
| `discord-yt-bot.py` | Cliente Discord, tarefa periódica e lógica de alertas. |
| `exponent_scraper.py` | Playwright: abre a URL e extrai o texto do APY. |
| `requirements.txt` | Dependências Python. |
| `.env.example` | Modelo de variáveis (sem segredos). |
| `Procfile` | Comando para workers em PaaS tipo Heroku. |

## Avisos

- O seletor CSS no scraper depende do HTML do site; se a Exponent alterar a página, pode ser preciso atualizar `exponent_scraper.py`.
- Os alertas são informativos; não constituem aconselhamento financeiro.

## Licença

Indique a licença que preferir no repositório (por exemplo MIT), se for tornar o projeto público.
