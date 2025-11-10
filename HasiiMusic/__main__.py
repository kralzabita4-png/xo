import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from HasiiMusic.logging import LOGGER
from HasiiMusic import app, userbot
from HasiiMusic.core.call import JARVIS
from HasiiMusic.misc import sudo
from HasiiMusic.plugins import ALL_MODULES
from HasiiMusic.utils.database import get_banned_users, get_gbanned
from HasiiMusic.utils.cookie_handler import fetch_and_store_cookies
from config import BANNED_USERS


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER("Tune").error("Assistant session bulunamadı. Lütfen SESSION ekle!")
        exit()

    try:
        await fetch_and_store_cookies()
        LOGGER("Tune").info("YouTube Cookies başarıyla yüklendi ✅")
    except Exception as e:
        LOGGER("Tune").warning(f"Cookie Hatası: {e}")

    await sudo()

    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)

        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)

    except Exception as e:
        LOGGER("Tune").warning(f"Banlı kullanıcı listesi yüklenemedi: {e}")

    # Uygulamayı başlat
    await app.start()

    # Tüm pluginleri yükle
    for module in ALL_MODULES:
        importlib.import_module("HasiiMusic.plugins." + module)

    LOGGER("Tune").info("Tüm plugin modülleri yüklendi ✅")

    await userbot.start()
    await JARVIS.start()

    try:
        # Örnek stream
        await JARVIS.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Tune").error("Log grubunda sesli sohbet açık değil! Aç ve botu yeniden başlat.")
        exit()
    except Exception:
        pass

    await JARVIS.decorators()

    LOGGER("Tune").info("Tune Music Bot Başarıyla Aktif 🎧")

    # Bot idle durumda beklesin
    await idle()

    # Bot durduruluyor
    await app.stop()
    await userbot.stop()

    LOGGER("Tune").info("Bot durduruldu 👋")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
