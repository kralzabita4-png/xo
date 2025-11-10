import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from HasiiMusic import LOGGER, app, userbot
from HasiiMusic.core.call import JARVIS
from HasiiMusic.misc import sudo
from HasiiMusic.plugins import ALL_MODULES
from HasiiMusic.utils.database import get_banned_users, get_gbanned
from HasiiMusic.utils.cookie_handler import fetch_and_store_cookies
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER.error("Assistant session bulunamadı. Lütfen session string ekle!")
        exit()

    try:
        await fetch_and_store_cookies()
        LOGGER.info("YouTube Cookies başarıyla yüklendi ✅")
    except Exception as e:
        LOGGER.warning(f"Cookie Hatası: {e}")

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except Exception as e:
        LOGGER.warning(f"Banlı kullanıcılar yüklenemedi: {e}")

    await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("HasiiMusic.plugins." + all_module)

    LOGGER.info("Bütün Plugin Modülleri Başarıyla Yüklendi ✅")

    await userbot.start()
    await JARVIS.start()

    try:
        await JARVIS.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER.error("Lütfen log grubunun sesli sohbetini açıp botu tekrar başlatın!")
        exit()
    except:
        pass

    await JARVIS.decorators()

    LOGGER.info("Tune Music Bot Başarıyla Başlatıldı ✅")
    await idle()

    await app.stop()
    await userbot.stop()

    LOGGER.info("Bot Durduruldu. Görüşmek üzere 👋")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
