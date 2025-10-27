from pyrogram.enums import ParseMode
from HasiiMusic import app
from HasiiMusic.utils.database import (
    get_served_chats,
    get_active_chats,
    get_active_video_chats,
    is_on_off,
)
from config import LOG, LOGGER_ID


async def send_deluxe_log(message, event_type: str, extra_info: str = None):
    """HasiiMusic Deluxe Log Panel — her eylem için ortak fonksiyon."""
    chat_id = message.chat.id
    uye_sayisi = await app.get_chat_members_count(chat_id)
    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    if not await is_on_off(LOG):
        return

    # Grup linki kontrolü
    if message.chat.username:
        chat_link = f"https://t.me/{message.chat.username}"
    else:
        try:
            invite_link = await app.export_chat_invite_link(chat_id)
            chat_link = invite_link
        except Exception:
            chat_link = "🔒 Gizli Grup (Link alınamadı)"

    # Kullanıcı kontrolü
    username = f"@{message.from_user.username}" if message.from_user.username else "🌸 Kullanıcı Adı Yok"

    tarih = message.date.strftime("%d.%m.%Y • %H:%M:%S")

    # 🔥 Deluxe HTML log metni
    logger_text = f"""
<pre>╔══════════════════════════════╗</pre>
<b>💫 𝐇𝐀𝐒𝐈𝐈 𝐌𝐔𝐒𝐈𝐂 - 𝐋𝐎𝐆 𝐏𝐀𝐍𝐄𝐋 💫</b>
<pre>╚══════════════════════════════╝</pre>

🎛 <b>Olay Türü:</b> <code>{event_type}</code>
🏷 <b>Grup:</b> <a href="{chat_link}">{message.chat.title}</a> <code>[{message.chat.id}]</code>  
👥 <b>Üye Sayısı:</b> <code>{uye_sayisi}</code>  
👤 <b>Kullanıcı:</b> {message.from_user.mention}  
🔖 <b>Kullanıcı Adı:</b> {username}  
🆔 <b>Kullanıcı ID:</b> <code>{message.from_user.id}</code>

🎧 <b>Detay:</b> <code>{extra_info or "—"}</code>

<pre>──────────────────────────────</pre>
📊 <b>Bot Durumu</b>  
🌍 <b>Toplam Grup:</b> <code>{toplam_grup}</code>  
🎙 <b>Aktif Sesli Sohbet:</b> <code>{aktif_sesli}</code>  
📹 <b>Aktif Video Sohbet:</b> <code>{aktif_video}</code>  

<pre>──────────────────────────────</pre>
🕒 <b>Kayıt Alındı:</b> <code>{tarih}</code>  
👾 <b>Bot:</b> <a href="https://t.me/HasiiMusic">Hasii Music</a> 🎧
<pre>──────────────────────────────</pre>
💠 <i>“Müziği Hisset, Sessizliği Duy.”</i>
"""

    # Gönderim
    if message.chat.id != LOGGER_ID:
        try:
            await app.send_message(
                LOGGER_ID,
                logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            await app.set_chat_title(LOGGER_ID, f"🎶 Aktif Ses: {aktif_sesli}")
        except Exception as e:
            print(f"[Log Hatası] {e}")
