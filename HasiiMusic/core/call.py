import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls
from HasiiMusic.core.logger import LOGGER
import config  # API_ID, API_HASH, STRING1..5

class Call:
    def __init__(self):
        # Userbot ve PyTgCalls istemcilerini hazırla
        self.userbot1 = Client("HasiiXAssis1", config.API_ID, config.API_HASH, session_string=config.STRING1) if config.STRING1 else None
        self.one = PyTgCalls(self.userbot1) if self.userbot1 else None

        self.userbot2 = Client("HasiiXAssis2", config.API_ID, config.API_HASH, session_string=config.STRING2) if config.STRING2 else None
        self.two = PyTgCalls(self.userbot2) if self.userbot2 else None

        self.userbot3 = Client("HasiiXAssis3", config.API_ID, config.API_HASH, session_string=config.STRING3) if config.STRING3 else None
        self.three = PyTgCalls(self.userbot3) if self.userbot3 else None

        self.userbot4 = Client("HasiiXAssis4", config.API_ID, config.API_HASH, session_string=config.STRING4) if config.STRING4 else None
        self.four = PyTgCalls(self.userbot4) if self.userbot4 else None

        self.userbot5 = Client("HasiiXAssis5", config.API_ID, config.API_HASH, session_string=config.STRING5) if config.STRING5 else None
        self.five = PyTgCalls(self.userbot5) if self.userbot5 else None

        self.active_calls: set[int] = set()

    # -------------------- START METODU --------------------
    async def start(self):
        LOGGER(__name__).info("PyTgCalls İstemcileri Başlatılıyor...")
        if self.userbot1:
            await self.userbot1.start()
            await self.one.start()
        if self.userbot2:
            await self.userbot2.start()
            await self.two.start()
        if self.userbot3:
            await self.userbot3.start()
            await self.three.start()
        if self.userbot4:
            await self.userbot4.start()
            await self.four.start()
        if self.userbot5:
            await self.userbot5.start()
            await self.five.start()
        LOGGER(__name__).info("Tüm Userbot ve PyTgCalls istemcileri başlatıldı.")

    # -------------------- DECORATORS METODU --------------------
    async def decorators(self):
        # Eski kodlar bunu çağırıyor, boş metod olarak bırakıyoruz
        LOGGER(__name__).info("Call.decorators() çalıştırıldı. (Boş metod)")

# -------------------- JARVIS NESNESİ --------------------
JARVIS = Call()

# -------------------- BOTU BAŞLAT --------------------
async def init():
    await JARVIS.start()
    await JARVIS.decorators()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
