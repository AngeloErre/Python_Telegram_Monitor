"""List private Telegram dialogs to help identify IDs of work accounts you own/control."""
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import User

load_dotenv()
API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "telegram_monitor")
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    print("Private dialogs / Chat private")
    print("=" * 72)
    async for dialog in client.iter_dialogs(limit=None):
        entity = dialog.entity
        if isinstance(entity, User):
            name = " ".join(x for x in (entity.first_name, entity.last_name) if x)
            username = f"@{entity.username}" if entity.username else "-"
            print(f"{name:30} | {username:20} | ID: {entity.id}")

with client:
    client.loop.run_until_complete(main())
