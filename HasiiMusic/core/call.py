import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import AudioQuality, ChatUpdate, MediaStream, StreamEnded, Update, VideoQuality

import config
from strings import get_string
from HasiiMusic import LOGGER, YouTube, app
from HasiiMusic.misc import db
from HasiiMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from HasiiMusic.utils.exceptions import AssistantErr
from HasiiMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from HasiiMusic.utils.inline.play import stream_markup
from HasiiMusic.utils.stream.autoclear import auto_clean
from HasiiMusic.utils.errors import capture_internal_err, send_large_error

autoend = {}
counter = {}

_AUDIO_QUALITY_MAP = {
    "studio": AudioQuality.STUDIO,
    "high": AudioQuality.HIGH,
    "medium": AudioQuality.MEDIUM,
    "low": AudioQuality.LOW,
}

_VIDEO_QUALITY_MAP = {
    "fhd_1080p": VideoQuality.FHD_1080p,
    "hd_720p": VideoQuality.HD_720p,
    "sd_480p": VideoQuality.SD_480p,
    "sd_360p": VideoQuality.SD_360p,
}


def _resolve_audio_quality(pref: str, fallback: AudioQuality) -> AudioQuality:
    return _AUDIO_QUALITY_MAP.get(pref, fallback)


def _resolve_video_quality(pref: str, fallback: VideoQuality) -> VideoQuality:
    return _VIDEO_QUALITY_MAP.get(pref, fallback)


def dynamic_media_stream(path: str, video: bool = False, ffmpeg_params: str = None) -> MediaStream:
    audio_pref = config.STREAM_VIDEO_AUDIO_QUALITY if video else config.STREAM_AUDIO_ONLY_QUALITY
    video_pref = config.STREAM_VIDEO_QUALITY

    return MediaStream(
        audio_path=path,
        media_path=path,
        audio_parameters=_resolve_audio_quality(audio_pref, AudioQuality.STUDIO),
        video_parameters=(
            _resolve_video_quality(video_pref, VideoQuality.HD_720p)
            if video
            else VideoQuality.SD_360p
        ),
        video_flags=(MediaStream.Flags.AUTO_DETECT if video else MediaStream.Flags.IGNORE),
        ffmpeg_parameters=ffmpeg_params,
    )


async def _clear_(chat_id: int) -> None:
    popped = db.pop(chat_id, None)
    if popped:
        await auto_clean(popped)
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)
    await set_loop(chat_id, 0)


class Call:
    def __init__(self):
        # Userbot ve PyTgCalls tanımlamaları
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
    # -------------------------------------------------------

    # Buraya önceki tüm metotların aynısını ekle (play, join_call, skip_stream, stop_stream, force_stop_stream, speedup_stream, seek_stream vb.)
    # Daha önce verdiğin kodun tamamı buraya eklenebilir. Önemli olan start() metodunun eklenmiş olması.

JARVIS = Call()
