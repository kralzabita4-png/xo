import socket
import time
import heroku3
from pyrogram import filters

import config
from HasiiMusic.core.mongo import mongodb
from HasiiMusic.logging import LOGGER

SUDOERS = filters.user()
HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


def dbb():
    global db
    db = {}
    LOGGER.info("ᴅᴀᴛᴀʙᴀsᴇ ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ 💗")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)

    sudoersdb = mongodb.sudoers
    data = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not data else data.get("sudoers", [])

    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )

    for user_id in sudoers:
        SUDOERS.add(user_id)

    LOGGER.info("sᴜᴅᴏ ᴜsᴇʀs ʟᴏᴀᴅᴇᴅ ✅")


def heroku():
    global HAPP
    if is_heroku():
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                hk = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = hk.app(config.HEROKU_APP_NAME)
                LOGGER.info("ʜᴇʀᴏᴋᴜ ᴀᴘᴘ ᴄᴏɴғɪɢᴜʀᴇᴅ ✅")
            except Exception as e:
                LOGGER.warning(f"ʜᴇʀᴏᴋᴜ ʜᴀᴛᴀ: {e}")
