# discord_bot.py
import asyncio
import datetime
import os
from pathlib import Path

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

# Importa a função do scraper
from exponent_scraper import get_implied_apy

# --- Configurações: use variáveis de ambiente ou um ficheiro .env (não versionado) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("CHANNEL_ID", "").strip()
TARGET_URL = os.environ.get(
    "TARGET_URL",
    "https://www.exponent.finance/farm/fragsol-10Jul25",
).strip()
CHECK_INTERVAL_SECONDS = 60  # Verificar a cada 60 segundos. Ajuste conforme necessário.
APY_BUY_THRESHOLD = 17.0
APY_SELL_THRESHOLD = 19.0

# --- Fim das Configurações ---

if not BOT_TOKEN:
    print("Erro: O token do bot (BOT_TOKEN) não foi definido.")
    print("Por favor, defina a variável de ambiente (BOT_TOKEN)" \
    " ou edite o script.")
    exit()

if not CHANNEL_ID:
    print("Erro: CHANNEL_ID não foi definido.")
    print("Defina CHANNEL_ID no .env ou nas variáveis de ambiente.")
    exit()

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print(f"Erro: CHANNEL_ID ('{CHANNEL_ID}') não é um ID numérico válido.")
    exit()

# Configura os intents. Para enviar DMs, intents básicos são suficientes.
# Se fosse para um servidor, precisaria de `members=True` e `message_content=True` dependendo das funcionalidades.
intents = discord.Intents.default()
# Para DMs, não precisamos de intents privilegiados específicos como members ou message_content
# mas se o bot fosse adicionado a servidores e precisasse ler mensagens ou ver membros, eles seriam necessários.

client = discord.Client(intents=intents)

# Variáveis para rastrear o último APY notificado para evitar spam
last_notified_buy_apy = None
last_notified_sell_apy = None

@client.event
async def on_ready():
    print(f"Bot '{client.user.name}' conectado e pronto!")
    print(f"ID do Bot: {client.user.id}")
    print(f"Enviando alertas para o canal com ID: {CHANNEL_ID}")
    check_price_task.start()

@tasks.loop(seconds=CHECK_INTERVAL_SECONDS)
async def check_price_task():
    global last_notified_buy_apy, last_notified_sell_apy
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verificando o preço...")
    
    # Usar asyncio.to_thread para rodar a função síncrona do Playwright em um thread separado
    # para não bloquear o loop de eventos do asyncio do Discord.
    current_apy = await asyncio.to_thread(get_implied_apy, TARGET_URL)

    if current_apy is not None:
        print(f"Implied APY atual: {current_apy}%")
        channel =  client.get_channel(CHANNEL_ID)
            
        if not channel:
            print(f"Erro: Não foi possível encontrar o canal com ID {CHANNEL_ID}.")
            return

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_content = f"**Alerta de Preço YT FRAGSOL (Exponent)!**\n"
        message_content += f"Data/Hora: {now}\n"
        message_content += f"Implied APY: **{current_apy}%**\n"
        message_content += f"Link: {TARGET_URL}"

        send_alert = False
        alert_type = ""

        if current_apy <= APY_BUY_THRESHOLD:
            alert_type = "COMPRA"
            # Só notifica se o preço mudou ou se é a primeira vez abaixo do threshold
            if last_notified_buy_apy is None or last_notified_buy_apy != current_apy:
                message_content += f"\nCondição: **Preço de COMPRA interessante (≤ {APY_BUY_THRESHOLD}%)**"
                last_notified_buy_apy = current_apy
                last_notified_sell_apy = None # Reseta o outro alerta para notificar se voltar
                send_alert = True
        
        elif current_apy >= APY_SELL_THRESHOLD:
            alert_type = "VENDA"
            # Só notifica se o preço mudou ou se é a primeira vez acima do threshold
            if last_notified_sell_apy is None or last_notified_sell_apy != current_apy:
                message_content += f"\nCondição: **Preço de VENDA interessante (≥ {APY_SELL_THRESHOLD}%)**"
                last_notified_sell_apy = current_apy
                last_notified_buy_apy = None # Reseta o outro alerta para notificar se voltar
                send_alert = True
        else:
            # Se o preço está entre os thresholds, reseta os últimos notificados para que 
            # a próxima vez que um threshold for atingido, ele notifique.
            last_notified_buy_apy = None
            last_notified_sell_apy = None

        if send_alert:
            try:
                await channel.send(message_content)
                print(f"Alerta de {alert_type} enviado para {channel.name} ({CHANNEL_ID}). APY: {current_apy}%")
            except discord.Forbidden:
                print(f"Erro: Não tenho permissão para enviar DM para o usuário {CHANNEL_ID}. O usuário pode ter DMs desabilitadas ou bloqueado o bot.")
            except discord.HTTPException as e:
                print(f"Erro ao enviar DM: {e}")
        else:
            print(f"Nenhuma condição de alerta atendida ou APY não mudou desde a última notificação de alerta. APY atual: {current_apy}%")

    else:
        print("Não foi possível obter o Implied APY desta vez.")

@check_price_task.before_loop
async def before_check_price_task():
    await client.wait_until_ready() # Espera o bot estar pronto

if __name__ == "__main__":
    if BOT_TOKEN and CHANNEL_ID:
        print("Iniciando o bot...")
        client.run(BOT_TOKEN)
    else:
        print("Verifique BOT_TOKEN e CHANNEL_ID (variáveis de ambiente ou .env).")

