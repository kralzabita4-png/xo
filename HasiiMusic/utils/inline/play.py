import time
from typing import Dict, List, Optional
from pyrogram.types import InlineKeyboardButton
from HasiiMusic.utils.formatters import time_to_seconds

# --- Sabitler (Constants) ---

# Kanal Butonu
CHANNEL_TEXT = "https://t.me/prenses_muzik_duyuru"
CHANNEL_URL = "https://t.me/prenses_muzik_duyuru"

# İlerleme Çubuğu Ayarları

# 

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
