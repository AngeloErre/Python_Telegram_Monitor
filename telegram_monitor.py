"""
Telegram Work Account Status Monitor
Monitor di stato per account Telegram di lavoro controllati dall'utente.

Use only with accounts you own/control or where you have authorization.
Usare solo con account propri/controllati o per i quali si dispone di autorizzazione.
"""

# IT: Importa moduli standard per CSV, variabili d'ambiente e data/ora.
# EN: Import standard modules for CSV, environment variables, and date/time.
import csv
import os
from datetime import datetime
from pathlib import Path

# IT: Carica le variabili dal file .env senza inserirle nel codice.
# EN: Load variables from .env so secrets are not hard-coded.
from dotenv import load_dotenv

# IT: Telethon gestisce la connessione MTProto e gli aggiornamenti Telegram.
# EN: Telethon handles the MTProto connection and Telegram updates.
from telethon import TelegramClient, events
from telethon.tl.types import UserStatusOnline, UserStatusOffline

load_dotenv()

# IT: Legge API ID e API HASH dal file .env.
# EN: Read API ID and API HASH from the .env file.
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]

# IT: Percorso della sessione. Il file .session è sensibile e NON va pubblicato.
# EN: Session path. The .session file is sensitive and MUST NOT be published.
SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "telegram_monitor")

# IT: File CSV in cui vengono registrati gli eventi.
# EN: CSV file where status events are logged.
CSV_FILE = Path(os.getenv("CSV_FILE", "telegram_accessi.csv"))

# IT: Inserire nel .env gli ID degli account di lavoro da controllare.
# EN: Put the IDs of the work accounts you control in .env.
TARGETS = {}
for number in (1, 2):
    raw_id = os.getenv(f"TARGET_{number}_ID", "").strip()
    if raw_id:
        label = os.getenv(f"TARGET_{number}_NAME", f"Work account {number}")
        TARGETS[int(raw_id)] = label

if not TARGETS:
    raise RuntimeError(
        "No target IDs configured / Nessun ID configurato. "
        "Edit .env and set TARGET_1_ID (and optionally TARGET_2_ID)."
    )

# IT: Memorizza l'ultimo stato ricevuto per evitare duplicati consecutivi.
# EN: Remember the last received state to avoid consecutive duplicate rows.
last_state = {}

# IT: Configura il client con riconnessione automatica continua.
# EN: Configure the client with continuous automatic reconnection.
client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH,
    auto_reconnect=True,
    connection_retries=None,
    retry_delay=5,
)


def save_event(user_id: int, status: str) -> None:
    """IT: Salva un evento nel CSV. EN: Save one event to the CSV."""
    now = datetime.now().astimezone()
    new_file = not CSV_FILE.exists()

    # IT: Apertura/chiusura ad ogni evento riduce il rischio di perdere righe.
    # EN: Opening/closing on every event reduces the risk of losing rows.
    with CSV_FILE.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(["Date", "Time", "Account", "Status"])
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S %z"),
            TARGETS[user_id],
            status,
        ])

    # IT: Mostra lo stesso evento anche nel terminale.
    # EN: Show the same event in the terminal too.
    print(f"{now:%Y-%m-%d %H:%M:%S %z} | {TARGETS[user_id]} | {status}", flush=True)


# IT: Questo handler viene richiamato quando Telegram invia un UserUpdate.
# EN: This handler runs whenever Telegram sends a UserUpdate.
@client.on(events.UserUpdate)
async def status_handler(event):
    user_id = event.user_id

    # IT: Ignora tutti gli account non configurati.
    # EN: Ignore every account that is not configured.
    if user_id not in TARGETS:
        return

    # IT: Registra solo ONLINE e OFFLINE, non stati approssimativi/last-seen.
    # EN: Log only ONLINE and OFFLINE, not approximate/last-seen states.
    if isinstance(event.status, UserStatusOnline):
        status = "ONLINE"
    elif isinstance(event.status, UserStatusOffline):
        status = "OFFLINE"
    else:
        return

    # IT: Evita due righe consecutive identiche per lo stesso account.
    # EN: Avoid two identical consecutive rows for the same account.
    if last_state.get(user_id) == status:
        return

    last_state[user_id] = status
    save_event(user_id, status)


async def main():
    # IT: Visualizza un riepilogo senza stampare API key o sessione.
    # EN: Print a summary without exposing API keys or session credentials.
    print("=" * 56)
    print("TELEGRAM WORK ACCOUNT STATUS MONITOR")
    print("=" * 56)
    for label in TARGETS.values():
        print(f"- {label}")
    print(f"CSV: {CSV_FILE.resolve()}")
    print("Waiting for Telegram status updates / In attesa di aggiornamenti...")
    print("Press CTRL+C to stop / CTRL+C per terminare")
    print("=" * 56)

    # IT: Mantiene il processo attivo; Telethon gestisce la riconnessione.
    # EN: Keep the process alive; Telethon handles reconnection.
    await client.run_until_disconnected()


# IT: Al primo avvio Telethon chiederà telefono, codice Telegram ed eventuale 2FA.
# EN: On first run Telethon asks for phone, Telegram login code, and 2FA if enabled.
with client:
    client.loop.run_until_complete(main())
