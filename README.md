# Bot de Discord — Alertas de Implied APY (Exponent)

Um bot em Python que monitora o **Implied APY** de um produto da Exponent Finance e envia alertas automaticamente para um **canal do Discord** quando o valor atinge determinados níveis de compra ou venda.

Esse projeto é ideal para quem quer acompanhar oportunidades sem precisar ficar atualizando a página manualmente.

<img width="1055" height="358" alt="image" src="https://github.com/user-attachments/assets/18c4e533-985b-41ff-8bb9-0b84e4232d84" />

## Funcionalidades

- Consulta periódica da página alvo usando **Playwright**
- Extração automática do **Implied APY**
- Envio de alertas no Discord quando:
  - APY é **menor ou igual ao limite de compra**
  - APY é **maior ou igual ao limite de venda**
- Evita spam ao só enviar alerta quando o valor muda dentro da mesma zona
- Configuração simples via variáveis de ambiente

## Como funciona

O bot roda em loop e, por padrão, verifica a página a cada **60 segundos**.

Quando o APY entra em uma das zonas:

- **Zona de compra** → APY ≤ limite de compra  
- **Zona de venda** → APY ≥ limite de venda  

O bot envia uma mensagem no canal configurado.

Para evitar notificações repetidas, ele só envia um novo alerta se o valor do APY mudar dentro da mesma zona.

## Requisitos

- Python **3.10+**
- Token de bot do Discord
- Servidor no Discord com permissões:
  - visualizar canal
  - enviar mensagens
- Playwright com Chromium instalado

## Estrutura do projeto

| Arquivo | Função |
|--------|--------|
| `discord-yt-bot.py` | Lógica principal do bot, cliente do Discord e regras de alerta |
| `exponent_scraper.py` | Scraper que acessa a página e extrai o APY |
| `requirements.txt` | Dependências do projeto |
| `.env.example` | Modelo de variáveis de ambiente |
| `Procfile` | Comando para deploy em plataformas como Heroku |

## Instalação

### 1. Clonar o repositório


```bash
git clone <url-do-seu-repositorio>
cd <nome-do-projeto>


