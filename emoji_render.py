# -*- coding: utf-8 -*-
"""
emoji_render.py — рендер ЦВЕТНЫХ эмодзи внутри pygame через Pillow.

Сам pygame не умеет рисовать цветные эмодзи (SDL_ttf отдаёт максимум
чёрно-белый "тофу"-квадратик), поэтому эмодзи-глифы рендерятся через
Pillow (используя системный цветной эмодзи-шрифт, например
NotoColorEmoji.ttf) в PNG-подобное RGBA изображение, которое затем
конвертируется в pygame.Surface и подставляется вместо символа текста.

Если на компьютере нет ни Pillow, ни цветного эмодзи-шрифта — модуль
тихо переключается в safe-режим и просто вырезает эмодзи из текста,
чтобы вместо них не показывались уродливые квадратики "тофу".

Использование: вместо `font.render(text, True, color)` вызывайте
`emoji_render.rtext(font, text, color)` — работает как обычный
font.render, но при этом эмодзи внутри текста рисуются цветными.
"""

import os
import re

try:
    from PIL import Image, ImageDraw, ImageFont
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

import pygame

# ----------------------------------------------------------------------
# Поиск системного цветного эмодзи-шрифта
# ----------------------------------------------------------------------
_EMOJI_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    "/usr/share/fonts/noto/NotoColorEmoji.ttf",
    "/system/fonts/NotoColorEmoji.ttf",                     # Android/Termux
    "/data/data/com.termux/files/usr/share/fonts/NotoColorEmoji.ttf",
    "/Library/Fonts/Apple Color Emoji.ttc",                 # macOS
    "/System/Library/Fonts/Apple Color Emoji.ttc",
    "C:/Windows/Fonts/seguiemj.ttf",                        # Windows
]

_STRIKE_SIZE = 109  # родной размер растровых страйков у NotoColorEmoji
_emoji_font = None
_emoji_font_path = None
_enabled = False


def _locate_emoji_font():
    for path in _EMOJI_FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def init():
    """Пытается инициализировать эмодзи-рендер. Безопасно вызывать многократно."""
    global _emoji_font, _emoji_font_path, _enabled
    if _emoji_font is not None or not _PIL_OK:
        return
    path = _locate_emoji_font()
    if not path:
        return
    try:
        font = ImageFont.truetype(path, _STRIKE_SIZE)
        # пробный рендер, чтобы убедиться что цветной страйк реально работает
        test_img = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        ImageDraw.Draw(test_img).text((0, 0), "🎯", font=font, embedded_color=True)
        if test_img.getbbox() is None:
            return  # шрифт не дал результата — не включаем режим эмодзи
        _emoji_font = font
        _emoji_font_path = path
        _enabled = True
    except Exception:
        _emoji_font = None
        _enabled = False


def is_enabled():
    return _enabled


# ----------------------------------------------------------------------
# Определение эмодзи-символов в строке
# ----------------------------------------------------------------------
_EMOJI_RANGES = [
    (0x1F300, 0x1FAFF),  # основной блок эмодзи (лица, объекты, символы, медали...)
    (0x2600, 0x27BF),     # разное + дингбаты (☀ ⚡ ✨ ⚔ ✅ и т.д.)
    (0x2190, 0x21FF),     # стрелки (↩ ↪ и т.д.)
    (0x2300, 0x23FF),     # разная техника (⏭ ⏮ ⏯ ⌛ и т.д.)
    (0x25A0, 0x25FF),     # геометрические фигуры (▶ ◀ и т.д.)
    (0x2B00, 0x2BFF),     # стрелки/звёзды (⬅ ⭐ и т.д.)
    (0x1F1E6, 0x1F1FF),   # региональные индикаторы (флаги)
]
_EMOJI_MODIFIERS = {0xFE0F, 0x200D, 0x20E3}  # variation selector, ZWJ, keycap


def _is_emoji_cp(cp):
    if cp in _EMOJI_MODIFIERS:
        return True
    for lo, hi in _EMOJI_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def _split_runs(text):
    """Возвращает список (is_emoji, кусок_текста) для смешанного текста."""
    runs = []
    cur = ""
    cur_is_emoji = None
    for ch in text:
        ch_is_emoji = _is_emoji_cp(ord(ch))
        if cur_is_emoji is None:
            cur_is_emoji = ch_is_emoji
        if ch_is_emoji == cur_is_emoji:
            cur += ch
        else:
            runs.append((cur_is_emoji, cur))
            cur = ch
            cur_is_emoji = ch_is_emoji
    if cur:
        runs.append((cur_is_emoji, cur))
    return runs


def strip_emoji(text):
    """Safe-фоллбек: убирает эмодзи из строки (если рендер недоступен)."""
    return "".join(ch for ch in text if not _is_emoji_cp(ord(ch))).strip()


# ----------------------------------------------------------------------
# Рендер одного эмодзи-ран(а) через Pillow -> pygame.Surface, с кэшем
# ----------------------------------------------------------------------
_surface_cache = {}


def _render_emoji_surface(run_text, target_h):
    key = (run_text, target_h)
    if key in _surface_cache:
        return _surface_cache[key]

    canvas = 160
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        draw.text((4, 4), run_text, font=_emoji_font, embedded_color=True)
    except TypeError:
        # старые версии Pillow без embedded_color
        draw.text((4, 4), run_text, font=_emoji_font)

    bbox = img.getbbox()
    if bbox is None:
        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        _surface_cache[key] = surf
        return surf

    img = img.crop(bbox)
    w, h = img.size
    if h <= 0:
        h = 1
    scale = target_h / h
    new_w = max(1, int(w * scale))
    img = img.resize((new_w, target_h), Image.LANCZOS)

    data = img.tobytes()
    surf = pygame.image.frombuffer(data, img.size, "RGBA").convert_alpha()
    _surface_cache[key] = surf
    return surf


# ----------------------------------------------------------------------
# Публичное API
# ----------------------------------------------------------------------
_text_cache = {}


def rtext(font, text, color):
    """
    Замена font.render(text, True, color), поддерживающая цветные эмодзи.
    Возвращает pygame.Surface (как обычный render).
    """
    if not text:
        return font.render(" ", True, color)

    if _emoji_font is None:
        init()

    if not _enabled:
        clean = strip_emoji(text)
        return font.render(clean if clean else text, True, color)

    cache_key = (id(font), text, color)
    if cache_key in _text_cache:
        return _text_cache[cache_key]

    runs = _split_runs(text)
    line_h = font.get_height()
    emoji_h = int(line_h * 1.15)

    pieces = []
    total_w = 0
    for is_emoji, chunk in runs:
        if not chunk:
            continue
        if is_emoji:
            esurf = _render_emoji_surface(chunk, emoji_h)
            pieces.append(("emoji", esurf))
            total_w += esurf.get_width() + 3
        else:
            tsurf = font.render(chunk, True, color)
            pieces.append(("text", tsurf))
            total_w += tsurf.get_width()

    if not pieces:
        return font.render(" ", True, color)

    out_h = max(line_h, emoji_h) + 4
    combined = pygame.Surface((max(1, total_w), out_h), pygame.SRCALPHA)
    x = 0
    for kind, surf in pieces:
        y = (out_h - surf.get_height()) // 2
        combined.blit(surf, (x, y))
        x += surf.get_width() + (3 if kind == "emoji" else 0)

    if len(_text_cache) > 2000:
        _text_cache.clear()
    _text_cache[cache_key] = combined
    return combined
