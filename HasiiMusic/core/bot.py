import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER
# 'commands.py' dosyasından fonksiyonu içe aktar
from .commands import set_bot_commands  # <-- EKLENDİ

class JARVIS(Client):
    def __init__(self):
        super().__init__(
            name="TuneViaBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            workers=48,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot istemcisi başlatıldı.")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        # Bot komutlarını ayarla
        await set_bot_commands(self)  # <-- EKLENDİ

        try:
            await self.send_message(
                config.LOGGER_ID,
                (
                    f"<u><b>» {self.mention} ʙᴏᴛ ʙᴀşʟᴀᴛɪʟᴅɪ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ᴀᴅ : {self.name}\n"
                    f"ᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("❌ Bot log grubuna/kanalına erişemiyor – önce ekleyin ve yetki verin!")
            sys.exit()
        except Exception as exc:
            LOGGER(__name__).error(f"❌ Bot log grubuna erişemedi.\nSebep: {type(exc).__name__}")
            sys.exit()

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Botu log grubunda/kanalında yönetici olarak yetkilendirin.")
                sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Yönetici durumu kontrol edilemedi: {e}")
            sys.exit()

        LOGGER(__name__).info(f"✅ Müzik Botu {self.name} (@{self.username}) olarak başlatıldı")
