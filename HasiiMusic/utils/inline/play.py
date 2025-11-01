import time
from typing import Dict, List, Optional
from pyrogram.types import InlineKeyboardButton
from HasiiMusic.utils.formatters import time_to_seconds

# --- Sabitler (Constants) ---

# Kanal Butonu
CHANNEL_TEXT = "💙 𝐊𝐚𝐧𝐚𝐥"
CHANNEL_URL = "https://t.me/Hebunbots"

# İlerleme Çubuğu Ayarları
PROGRESS_BAR_LENGTH = 8
PROGRESS_FILLED = "▰"
PROGRESS_EMPTY = "▱"

# Zamanlayıcı Ayarları
LAST_UPDATE_TIME: Dict[int, float] = {}
PROGRESS_UPDATE_INTERVAL = 6  # Saniye

# --- Yardımcı Fonksiyonlar (Helper Functions) ---

def should_update_progress(chat_id: int) -> bool:
    """Oran sınırlarını aşmamak için ilerleme çubuğunun güncellenip güncellenmeyeceğini kontrol eder."""
    now = time.time()
    last_update = LAST_UPDATE_TIME.get(chat_id, 0)
    if now - last_update >= PROGRESS_UPDATE_INTERVAL:
        LAST_UPDATE_TIME[chat_id] = now
        return True
    return False


def generate_progress_bar(played_sec: int, duration_sec: int) -> str:
    """Metin tabanlı bir ilerleme çubuğu oluşturur."""
    if duration_sec == 0:
        percentage = 0.0
    else:
        percentage = min(max(played_sec / duration_sec, 0.0), 1.0)

    filled_length = int(round(PROGRESS_BAR_LENGTH * percentage))
    empty_length = PROGRESS_BAR_LENGTH - filled_length

    return (PROGRESS_FILLED * filled_length) + (PROGRESS_EMPTY * empty_length)


def _get_bottom_buttons(_, close_callback_data: str) -> List[InlineKeyboardButton]:
    """Tüm menülerde ortak olan alt buton sırasını oluşturur."""
    return [
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=close_callback_data),
        InlineKeyboardButton(text=CHANNEL_TEXT, url=CHANNEL_URL),
    ]

# --- Ana Buton Fonksiyonları (Markup Functions) ---



def stream_markup(_, chat_id: int) -> List[List[InlineKeyboardButton]]:
    """Sadece kanal butonunu gösterir."""
    return [
        [InlineKeyboardButton(text=CHANNEL_TEXT, url=CHANNEL_URL)]
    ]


def track_markup(_, videoid: str, user_id: int, channel: str, fplay: str) -> List[List[InlineKeyboardButton]]:
    """Ses ve video indirme/çalma butonlarını gösterir."""
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],  # Muhtemelen "Ses"
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],  # Muhtemelen "Video"
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        _get_bottom_buttons(_, close_callback_data=f"forceclose {videoid}|{user_id}"),
    ]


def playlist_markup(_, videoid: str, user_id: int, ptype: str, channel: str, fplay: str) -> List[List[InlineKeyboardButton]]:
    """Oynatma listesi için ses ve video butonlarını gösterir."""
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"TuneViaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        _get_bottom_buttons(_, close_callback_data=f"forceclose {videoid}|{user_id}"),
    ]


def livestream_markup(_, videoid: str, user_id: int, mode: str, channel: str, fplay: str) -> List[List[InlineKeyboardButton]]:
    """Canlı yayınlar için oynatma butonu gösterir."""
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],  # Muhtemelen "Canlı Yayını Oynat"
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            )
        ],
        _get_bottom_buttons(_, close_callback_data=f"forceclose {videoid}|{user_id}"),
    ]


def slider_markup(_, videoid: str, user_id: int, query: str, query_type: str, channel: str, fplay: str) -> List[List[InlineKeyboardButton]]:
    """Slider (kaydırıcı) sonuçları için butonları gösterir."""
    short_query = query[:20]  # Callback verisinin 64 byte limitini aşmamak için sorguyu kısalt

    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        _get_bottom_buttons(_, close_callback_data=f"forceclose {short_query}|{user_id}"),
    ]
