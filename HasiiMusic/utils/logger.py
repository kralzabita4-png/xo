import psutil
from pyrogram.enums import ParseMode
from HasiiMusic import app
from HasiiMusic.utils.database import (
    get_served_chats,
    get_active_chats,
    get_active_video_chats,
    is_on_off,
)
from config import LOG, LOGGER_ID


def colorize(value: float) -> str:
    """CPU/RAM/Disk değerini renkli emoji ile döndürür."""
    if value <= 50:
        return f"🟢 {value}%"
    elif value <= 75:
        return f"🟡 {value}%"
    else:
        return f"🔴 {value}%"


async def play_logs(message, streamtype):
    chat_id = message.chat.id
    uye_sayisi = await app.get_chat_members_count(chat_id)
    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    if await is_on_off(LOG):

        # Grup linki oluşturma (gizli gruplar dahil)
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        else:
            try:
                invite_link = await app.export_chat_invite_link(chat_id)
                chat_link = invite_link
            except Exception:
                chat_link = "🔗 Link alınamadı"

        # Kullanıcı adı kontrolü
        username = f"@{message.from_user.username}" if message.from_user.username else "🌸 Kullanıcı Adı Yok"

        # Tarih formatı
        tarih = message.date.strftime("%d.%m.%Y • %H:%M:%S")

        # Sistem durumu
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        cpu_colored = colorize(cpu)
        ram_colored = colorize(ram)
        disk_colored = colorize(disk)

        # Log metni
        logger_text = f"""
🎵 <b>Yeni Oynatma Başladı!</b>

🏷 <b>Grup:</b> <a href="{chat_link}">{message.chat.title}</a> <code>[{message.chat.id}]</code>  
👥 <b>Üye Sayısı:</b> <code>{uye_sayisi}</code>  
👤 <b>Kullanıcı:</b> {message.from_user.mention}  
🔖 <b>Kullanıcı Adı:</b> {username}  
🆔 <b>Kullanıcı ID:</b> <code>{message.from_user.id}</code>

🎧 <b>İstek Türü:</b> <code>{streamtype}</code>  
🎹 <b>Sorgu:</b> <code>{message.text or "—"}</code>

💻 <b>Bot Durumu</b>  
🌍 <b>Toplam Grup:</b> <code>{toplam_grup}</code>  
🎙 <b>Aktif Sesli Sohbet:</b> <code>{aktif_sesli}</code>  
📹 <b>Aktif Video Sohbet:</b> <code>{aktif_video}</code>  
🖥️ <b>CPU:</b> <code>{cpu_colored}</code>  
🧠 <b>RAM:</b> <code>{ram_colored}</code>  
🗄️ <b>Disk:</b> <code>{disk_colored}</code>

⏰ <b>Kayıt Alındı:</b> <code>{tarih}</code>
"""

        # Log grubuna gönder
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
        return
