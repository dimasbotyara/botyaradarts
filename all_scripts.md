
config.py:
```
# -*- coding: utf-8 -*-
"""
config.py — все константы проекта: цвета, размеры, шрифты, геометрия мишени,
настройки режимов игры. Меняйте значения здесь, чтобы настроить игру
под свой экран/телевизор.
"""

import os

# ----------------------------------------------------------------------
# ЭКРАН
# ----------------------------------------------------------------------
# Стартовое разрешение окна. Игра адаптирует всю разметку под текущий
# размер окна, поэтому его можно свободно растягивать/разворачивать
# на весь экран телевизора (клавиша F11 — полноэкранный режим).
DEFAULT_WIDTH = 1600
DEFAULT_HEIGHT = 900
MIN_WIDTH = 1100
MIN_HEIGHT = 650
FPS = 60
WINDOW_TITLE = "Дартс — Домашний счёт"

# Доля экрана, отдаваемая под мишень (слева). Остальное — правая панель.
BOARD_PANEL_RATIO = 1.0 / 3.0

# ----------------------------------------------------------------------
# ЦВЕТА (для "крутого" тёмного интерфейса, хорошо видно с дивана)
# ----------------------------------------------------------------------
BG_TOP = (18, 20, 28)
BG_BOTTOM = (10, 11, 16)
PANEL_BG = (26, 29, 39)
PANEL_BG_LIGHT = (34, 38, 50)
PANEL_BORDER = (58, 64, 82)

ACCENT = (255, 196, 0)          # золотой акцент
ACCENT_2 = (0, 200, 180)        # бирюзовый акцент
DANGER = (235, 70, 70)
SUCCESS = (80, 210, 120)

TEXT_MAIN = (240, 242, 248)
TEXT_DIM = (150, 156, 172)
TEXT_DIM2 = (105, 110, 128)

BOARD_BLACK = (25, 25, 28)
BOARD_CREAM = (232, 220, 196)
BOARD_RED = (196, 30, 45)
BOARD_GREEN = (20, 120, 70)
BOARD_WIRE = (150, 150, 150)
BOARD_OUT = (14, 15, 20)
BOARD_RIM = (60, 45, 30)

BUTTON_BG = (44, 49, 64)
BUTTON_BG_HOVER = (62, 68, 88)
BUTTON_BG_ACTIVE = (255, 196, 0)
BUTTON_TEXT = (240, 242, 248)
BUTTON_TEXT_ACTIVE = (20, 20, 24)

TEAM_COLORS = [ (90, 170, 255), (255, 120, 120), (140, 230, 140), (230, 170, 255) ]
PLAYER_COLORS = [
    (255, 196, 0), (0, 200, 180), (255, 120, 150), (130, 170, 255),
    (170, 255, 120), (255, 150, 60), (200, 140, 255), (120, 220, 220),
]

# ----------------------------------------------------------------------
# ШРИФТЫ (относительные размеры пересчитываются в main по разрешению)
# ----------------------------------------------------------------------
FONT_NAME = None  # None -> системный шрифт pygame (SysFont), поддерживает кириллицу
FONT_NAME_CANDIDATES = ["dejavusans", "arial", "notosans", "freesans"]

# ----------------------------------------------------------------------
# ГЕОМЕТРИЯ МИШЕНИ (в долях от радиуса, приближено к реальным пропорциям)
# ----------------------------------------------------------------------
R_BULL = 0.075          # яблочко (50)
R_OUTER_BULL = 0.187    # внешний бул (25)
R_TRIPLE_IN = 0.582
R_TRIPLE_OUT = 0.629
R_DOUBLE_IN = 0.953
R_DOUBLE_OUT = 1.0

# Порядок секторов по часовой стрелке начиная с сектора "20" (сверху)
SECTOR_ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

# ----------------------------------------------------------------------
# ПРАВИЛА РЕЖИМОВ (домашние, не профессиональные)
# ----------------------------------------------------------------------
DARTS_PER_TURN_DEFAULT = 3

MODE_CLASSIC = "classic"
MODE_DUEL = "duel"
MODE_TEAMS = "teams"
MODE_SPRINT6 = "sprint6"
MODE_UPGRADES = "upgrades"

MODE_INFO = {
    MODE_CLASSIC: {
        "title": "Обычный",
        "icon": "🎯",
        "desc": "От 2 игроков. Каждый ход — 3 дротика. Играем N раундов, "
                "побеждает набравший больше очков.",
        "rounds": 8,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_DUEL: {
        "title": "Дуэль",
        "icon": "⚔️",
        "desc": "Ровно 2 игрока «стенка на стенку». 3 дротика за ход, "
                "8 раундов, у кого больше очков — тот и чемпион.",
        "rounds": 8,
        "min_players": 2,
        "max_players": 2,
        "teams": False,
    },
    MODE_TEAMS: {
        "title": "Команды",
        "icon": "🤝",
        "desc": "Две команды. Игроки кидают по очереди, очки команды "
                "суммируются. 8 раундов.",
        "rounds": 8,
        "min_players": 2,
        "max_players": 8,
        "teams": True,
    },
    MODE_SPRINT6: {
        "title": "Спринт 6х6",
        "icon": "⚡",
        "desc": "6 раундов с нарастающей нагрузкой: раунды 1-2 — по "
                "1 дротику за ход, раунды 3-4 — по 2 дротика сразу, "
                "раунды 5-6 — по 3 дротика сразу. Задача — точность под давлением!",
        "rounds": 6,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_UPGRADES: {
        "title": "С улучшениями",
        "icon": "✨",
        "desc": "7 раундов. В начале каждого хода игроку выпадает "
                "случайное улучшение (с анимацией слот-машины). "
                "Чем дальше в игру — тем мощнее улучшения!",
        "rounds": 7,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
}

def darts_for_round(mode, round_no):
    """Сколько дротиков за ход в данном раунде (нумерация раундов с 1)."""
    if mode == MODE_SPRINT6:
        if round_no <= 2:
            return 1
        elif round_no <= 4:
            return 2
        else:
            return 3
    return DARTS_PER_TURN_DEFAULT

# ----------------------------------------------------------------------
# ПРОЧЕЕ
# ----------------------------------------------------------------------
STATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "darts_stats.json")
UNDO_STACK_LIMIT = 500
```

dartboard.py:
```
# -*- coding: utf-8 -*-
"""
dartboard.py — отрисовка мишени и определение результата клика мышкой.

Мишень строится геометрически (без картинок), поэтому отлично
масштабируется на любое разрешение — хоть на весь телевизор.
"""

import math
import pygame
import config as C


class HitResult:
    """Результат попадания дротика."""
    __slots__ = ("value", "multiplier", "points", "label", "ring")

    def __init__(self, value, multiplier, label, ring):
        self.value = value              # базовое число сектора (0 если мимо/бул)
        self.multiplier = multiplier    # 1, 2 или 3 (для бул считаем 1)
        self.points = value * multiplier if ring not in ("bull", "outer_bull") else value
        self.label = label              # "T20", "D5", "20", "BULL", "25", "MISS"
        self.ring = ring                # "double" | "triple" | "single" | "bull" | "outer_bull" | "miss"

    def __repr__(self):
        return f"<Hit {self.label} = {self.points}>"


class Dartboard:
    """
    Мишень, вписанная в квадрат rect (pygame.Rect).
    Все геометрические расчёты идут от центра и радиуса = min(w,h)/2 * 0.94
    (немного отступа под обод/подпись).
    """

    def __init__(self, rect: pygame.Rect):
        self.set_rect(rect)
        self._surface_cache = None
        self._cache_key = None

    def set_rect(self, rect: pygame.Rect):
        self.rect = pygame.Rect(rect)
        self.cx = self.rect.centerx
        self.cy = self.rect.centery
        self.radius = int(min(self.rect.width, self.rect.height) * 0.47)
        self._surface_cache = None

    # ------------------------------------------------------------------
    # HIT DETECTION
    # ------------------------------------------------------------------
    def hit_test(self, pos):
        """pos = (x, y) экранные координаты. Возвращает HitResult."""
        dx = pos[0] - self.cx
        dy = pos[1] - self.cy
        dist = math.hypot(dx, dy)
        r = dist / self.radius if self.radius > 0 else 999

        if r > C.R_DOUBLE_OUT:
            return HitResult(0, 1, "МИМО", "miss")

        if r <= C.R_BULL:
            return HitResult(50, 1, "БУЛ 50", "bull")
        if r <= C.R_OUTER_BULL:
            return HitResult(25, 1, "25", "outer_bull")

        # угол: 0 градусов — вверх (сектор 20), далее по часовой стрелке
        angle = math.degrees(math.atan2(dx, -dy))  # -180..180, 0 = вверх
        angle = (angle + 360) % 360
        # каждый сектор 18 градусов, сектор i начинается с (angle_offset)
        sector_index = int(((angle + 9) % 360) // 18)
        value = C.SECTOR_ORDER[sector_index]

        if C.R_TRIPLE_IN < r <= C.R_TRIPLE_OUT:
            return HitResult(value, 3, f"T{value}", "triple")
        if C.R_DOUBLE_IN < r <= C.R_DOUBLE_OUT:
            return HitResult(value, 2, f"D{value}", "double")
        return HitResult(value, 1, f"{value}", "single")

    # ------------------------------------------------------------------
    # DRAWING
    # ------------------------------------------------------------------
    def draw(self, surface, hover_pos=None, last_hits=None):
        """
        Рисует мишень. last_hits — список (pos, color) точек попаданий
        текущего хода, чтобы отметить их на доске.
        """
        cache_key = (self.rect.width, self.rect.height, self.rect.topleft)
        if self._surface_cache is None or self._cache_key != cache_key:
            self._build_static_surface()
            self._cache_key = cache_key

        surface.blit(self._surface_cache, self.rect.topleft)

        # подсветка сектора под курсором
        if hover_pos:
            hit = self.hit_test(hover_pos)
            if hit.ring != "miss":
                self._draw_hover_highlight(surface, hit)

        # точки уже брошенных в этом ходе дротиков
        if last_hits:
            for pos, color in last_hits:
                pygame.draw.circle(surface, (255, 255, 255), pos, 9)
                pygame.draw.circle(surface, color, pos, 6)
                pygame.draw.circle(surface, (20, 20, 20), pos, 9, 2)

    def _build_static_surface(self):
        """Рендерит статичную часть мишени в закэшированную поверхность."""
        size = (self.rect.width, self.rect.height)
        surf = pygame.Surface(size, pygame.SRCALPHA)
        cx = self.rect.width // 2
        cy = self.rect.height // 2
        R = self.radius

        # внешний деревянный обод
        pygame.draw.circle(surf, C.BOARD_RIM, (cx, cy), int(R * 1.09))
        pygame.draw.circle(surf, C.BOARD_OUT, (cx, cy), int(R * C.R_DOUBLE_OUT) + 4)

        # сектора (single/triple/double чередуют cream/black и red/green)
        n = len(C.SECTOR_ORDER)
        for i, value in enumerate(C.SECTOR_ORDER):
            start_deg = -90 + i * 18 - 9  # -90 = верх, сектор центрирован на верх для i=0
            self._draw_sector_wedge(surf, cx, cy, R, start_deg, 18, i)

        # окружности-разделители колец
        for frac in (C.R_TRIPLE_IN, C.R_TRIPLE_OUT, C.R_DOUBLE_IN, C.R_DOUBLE_OUT):
            pygame.draw.circle(surf, C.BOARD_WIRE, (cx, cy), int(R * frac), 1)

        # бул
        pygame.draw.circle(surf, C.BOARD_GREEN, (cx, cy), int(R * C.R_OUTER_BULL))
        pygame.draw.circle(surf, C.BOARD_RED, (cx, cy), int(R * C.R_BULL))
        pygame.draw.circle(surf, C.BOARD_WIRE, (cx, cy), int(R * C.R_OUTER_BULL), 1)

        # проволочные линии секторов
        for i in range(n):
            deg = -90 + i * 18 - 9
            rad = math.radians(deg)
            x2 = cx + math.sin(rad) * R * C.R_DOUBLE_OUT
            y2 = cy - math.cos(rad) * R * C.R_DOUBLE_OUT
            x1 = cx + math.sin(rad) * R * C.R_OUTER_BULL
            y1 = cy - math.cos(rad) * R * C.R_OUTER_BULL
            pygame.draw.line(surf, C.BOARD_WIRE, (x1, y1), (x2, y2), 1)

        # номера секторов по кругу
        font = pygame.font.SysFont(_pick_font(), max(14, int(R * 0.11)), bold=True)
        label_r = R * 1.02
        for i, value in enumerate(C.SECTOR_ORDER):
            deg = -90 + i * 18
            rad = math.radians(deg)
            lx = cx + math.sin(rad) * label_r
            ly = cy - math.cos(rad) * label_r
            text = font.render(str(value), True, C.TEXT_MAIN)
            surf.blit(text, text.get_rect(center=(lx, ly)))

        self._surface_cache = surf

    def _draw_sector_wedge(self, surf, cx, cy, R, start_deg, span_deg, index):
        """Рисует один клин сектора с чередованием цветов по кольцам."""
        is_alt = index % 2 == 0
        single_color = C.BOARD_CREAM if is_alt else C.BOARD_BLACK
        special_color = C.BOARD_RED if is_alt else C.BOARD_GREEN

        rings = [
            (C.R_OUTER_BULL, C.R_TRIPLE_IN, single_color),
            (C.R_TRIPLE_IN, C.R_TRIPLE_OUT, special_color),
            (C.R_TRIPLE_OUT, C.R_DOUBLE_IN, single_color),
            (C.R_DOUBLE_IN, C.R_DOUBLE_OUT, special_color),
        ]
        for r_in, r_out, color in rings:
            self._draw_ring_wedge(surf, cx, cy, R * r_in, R * r_out, start_deg, span_deg, color)

    @staticmethod
    def _draw_ring_wedge(surf, cx, cy, r_in, r_out, start_deg, span_deg, color):
        """Рисует часть кольца (клин) через полигон из точек дуги."""
        steps = 6
        pts = []
        for s in range(steps + 1):
            deg = start_deg + span_deg * s / steps
            rad = math.radians(deg)
            pts.append((cx + math.sin(rad) * r_out, cy - math.cos(rad) * r_out))
        for s in range(steps + 1):
            deg = start_deg + span_deg * (steps - s) / steps
            rad = math.radians(deg)
            pts.append((cx + math.sin(rad) * r_in, cy - math.cos(rad) * r_in))
        if len(pts) >= 3:
            pygame.draw.polygon(surf, color, pts)

    def _draw_hover_highlight(self, surface, hit: HitResult):
        color = C.ACCENT if hit.ring in ("double", "triple") else (255, 255, 255)
        alpha_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # просто рисуем тонкое кольцо-курсор в позиции — упрощённая подсветка
        surface_rect = self.rect
        pygame.draw.rect(surface, color, surface_rect, 3, border_radius=int(self.radius * 0.05))


_FONT_CHOSEN = None

def _pick_font():
    global _FONT_CHOSEN
    if _FONT_CHOSEN:
        return _FONT_CHOSEN
    available = pygame.font.get_fonts()
    for cand in C.FONT_NAME_CANDIDATES:
        if cand in available:
            _FONT_CHOSEN = cand
            return cand
    _FONT_CHOSEN = pygame.font.get_default_font()
    return _FONT_CHOSEN
```

emoji_render.py:
```
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
```

fx.py:
```
# -*- coding: utf-8 -*-
"""
fx.py — система визуальных эффектов ("сочность" интерфейса): частицы при
попадании дротика, пульсирующее кольцо на месте удара, вспышка экрана на
крутых попаданиях, всплывающий текст-коллаут ("БУЛ!", "TRIPLE!"), рябь на
кнопках при клике и конфетти на экране победы.

Всё живёт в EffectsManager — main.py просто зовёт update(dt)/draw(...) раз
в кадр и spawn_* при нужных событиях.
"""

import math
import random
import pygame
import config as C
import emoji_render


# ==========================================================================
# ЧАСТИЦЫ (взрыв при попадании дротика)
# ==========================================================================
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "radius", "gravity")

    def __init__(self, x, y, vx, vy, life, color, radius, gravity=260):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.radius = radius
        self.gravity = gravity

    def update(self, dt):
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * t)
        r = max(1, int(self.radius * (0.4 + 0.6 * t)))
        if alpha <= 0 or r <= 0:
            return
        d = r * 2 + 2
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), r)
        surface.blit(s, (self.x - d // 2, self.y - d // 2))


class ParticleBurst:
    """Управляет коллекцией частиц-искр, разлетающихся из точки попадания."""

    def __init__(self):
        self.particles = []

    def spawn(self, pos, color, count=16, speed_range=(70, 260),
              life_range=(0.35, 0.8), radius_range=(2, 5), gravity=260):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(*life_range)
            radius = random.uniform(*radius_range)
            self.particles.append(Particle(pos[0], pos[1], vx, vy, life, color, radius, gravity))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


# ==========================================================================
# ПУЛЬСИРУЮЩЕЕ КОЛЬЦО (на месте попадания дротика)
# ==========================================================================
class RingPulse:
    def __init__(self, pos, color, max_radius=70, duration=0.5, start_radius=6, width=4):
        self.pos = pos
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.start_radius = start_radius
        self.width = width
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        radius = self.start_radius + (self.max_radius - self.start_radius) * t
        alpha = int(255 * (1 - t))
        if alpha <= 0:
            return
        d = int(radius * 2 + self.width * 2 + 4)
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), int(radius), self.width)
        surface.blit(s, (self.pos[0] - d // 2, self.pos[1] - d // 2))


class RingPulseManager:
    def __init__(self):
        self.rings = []

    def spawn(self, pos, color, **kw):
        self.rings.append(RingPulse(pos, color, **kw))

    def update(self, dt):
        for r in self.rings:
            r.update(dt)
        self.rings = [r for r in self.rings if r.alive]

    def draw(self, surface):
        for r in self.rings:
            r.draw(surface)


# ==========================================================================
# ВСПЫШКА ЭКРАНА (на бул/трипл/джекпот)
# ==========================================================================
class ScreenFlash:
    def __init__(self, color, alpha0=110, duration=0.22):
        self.color = color
        self.alpha0 = alpha0
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        alpha = int(self.alpha0 * (1 - t))
        if alpha <= 0:
            return
        w, h = surface.get_width(), surface.get_height()
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surface.blit(s, (0, 0))


class ScreenFlashManager:
    def __init__(self):
        self.flashes = []

    def spawn(self, color, **kw):
        self.flashes.append(ScreenFlash(color, **kw))

    def update(self, dt):
        for f in self.flashes:
            f.update(dt)
        self.flashes = [f for f in self.flashes if f.alive]

    def draw(self, surface):
        for f in self.flashes:
            f.draw(surface)


# ==========================================================================
# ВСПЛЫВАЮЩИЙ ТЕКСТ-КОЛЛАУТ ("БУЛ!", "TRIPLE!", "180!") — с поп-эффектом
# ==========================================================================
class Callout:
    def __init__(self, text, color, pos, duration=0.95, base_size=1.0):
        self.text = text
        self.color = color
        self.pos = pos
        self.duration = duration
        self.base_size = base_size
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface, font):
        t = min(1.0, self.age / self.duration)
        # поп-эффект: быстро растёт до 1.15, потом плавно садится к 1.0, в конце тухнет
        if t < 0.25:
            scale = self._ease_out_back(t / 0.25) * 1.15
        elif t < 0.7:
            local = (t - 0.25) / 0.45
            scale = 1.15 - 0.15 * local
        else:
            scale = 1.0
        alpha = 255 if t < 0.7 else int(255 * (1 - (t - 0.7) / 0.3))
        y_off = -40 * t

        base_surf = emoji_render.rtext(font, self.text, self.color)
        w, h = base_surf.get_size()
        scale = max(0.05, scale * self.base_size)
        scaled = pygame.transform.smoothscale(base_surf, (max(1, int(w * scale)), max(1, int(h * scale))))
        scaled.set_alpha(max(0, alpha))
        rect = scaled.get_rect(center=(self.pos[0], self.pos[1] + y_off))
        surface.blit(scaled, rect)

    @staticmethod
    def _ease_out_back(t):
        c1 = 1.70158
        c3 = c1 + 1
        t = max(0.0, min(1.0, t))
        return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


class CalloutManager:
    def __init__(self):
        self.callouts = []

    def spawn(self, text, color, pos, **kw):
        self.callouts.append(Callout(text, color, pos, **kw))

    def update(self, dt):
        for c in self.callouts:
            c.update(dt)
        self.callouts = [c for c in self.callouts if c.alive]

    def draw(self, surface, font):
        for c in self.callouts:
            c.draw(surface, font)


# ==========================================================================
# РЯБЬ НА КНОПКАХ (тактильный отклик клика)
# ==========================================================================
class Ripple:
    def __init__(self, pos, color, max_radius=55, duration=0.35):
        self.pos = pos
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        radius = self.max_radius * (0.2 + 0.8 * t)
        alpha = int(160 * (1 - t))
        if alpha <= 0:
            return
        d = int(radius * 2 + 4)
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), int(radius))
        surface.blit(s, (self.pos[0] - d // 2, self.pos[1] - d // 2))


class RippleManager:
    def __init__(self):
        self.ripples = []

    def spawn(self, pos, color, **kw):
        self.ripples.append(Ripple(pos, color, **kw))

    def update(self, dt):
        for r in self.ripples:
            r.update(dt)
        self.ripples = [r for r in self.ripples if r.alive]

    def draw(self, surface):
        for r in self.ripples:
            r.draw(surface)


# ==========================================================================
# КОНФЕТТИ (экран победы)
# ==========================================================================
class ConfettiPiece:
    __slots__ = ("x", "y", "vx", "vy", "size", "color", "angle", "spin", "life", "max_life")

    def __init__(self, x, y, vx, vy, size, color, angle, spin, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.angle = angle
        self.spin = spin
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.vy += 60 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.spin * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * min(1.0, t * 2.2))
        s = pygame.Surface((self.size, self.size * 2), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        rotated = pygame.transform.rotate(s, self.angle)
        surface.blit(rotated, rotated.get_rect(center=(self.x, self.y)))


class ConfettiSystem:
    def __init__(self):
        self.pieces = []

    def spawn(self, width, colors, count=140, y0=-20):
        for _ in range(count):
            x = random.uniform(0, width)
            y = random.uniform(y0 - 200, y0)
            vx = random.uniform(-40, 40)
            vy = random.uniform(40, 140)
            size = random.uniform(6, 12)
            color = random.choice(colors)
            angle = random.uniform(0, 360)
            spin = random.uniform(-220, 220)
            life = random.uniform(2.5, 4.5)
            self.pieces.append(ConfettiPiece(x, y, vx, vy, size, color, angle, spin, life))

    def update(self, dt):
        for p in self.pieces:
            p.update(dt)
        self.pieces = [p for p in self.pieces if p.alive]

    def draw(self, surface):
        for p in self.pieces:
            p.draw(surface)

    def clear(self):
        self.pieces = []


# ==========================================================================
# МЕНЕДЖЕР ВСЕХ ЭФФЕКТОВ
# ==========================================================================
RING_HIT_COLORS = {
    "bull": (255, 90, 90),
    "outer_bull": (255, 150, 90),
    "triple": C.ACCENT,
    "double": C.ACCENT_2,
    "single": (200, 205, 215),
    "miss": (110, 115, 130),
}


class EffectsManager:
    def __init__(self):
        self.particles = ParticleBurst()
        self.rings = RingPulseManager()
        self.flashes = ScreenFlashManager()
        self.callouts = CalloutManager()
        self.ripples = RippleManager()
        self.confetti = ConfettiSystem()

    def update(self, dt):
        self.particles.update(dt)
        self.rings.update(dt)
        self.flashes.update(dt)
        self.callouts.update(dt)
        self.ripples.update(dt)
        self.confetti.update(dt)

    # --------------------------------------------------------------
    def on_hit(self, pos, hit, player_color):
        """Спавнит подходящий набор эффектов под конкретное попадание дротика."""
        ring = hit.ring
        color = RING_HIT_COLORS.get(ring, player_color)

        if ring == "miss":
            self.particles.spawn(pos, color, count=8, speed_range=(40, 120),
                                  life_range=(0.25, 0.45), radius_range=(1.5, 3))
            self.rings.spawn(pos, color, max_radius=34, duration=0.35, width=3)
            return

        # чем ценнее попадание — тем мощнее эффект
        big = ring in ("bull", "triple")
        count = 28 if big else (18 if ring in ("outer_bull", "double") else 12)
        self.particles.spawn(pos, color, count=count,
                              speed_range=(90, 300) if big else (60, 200),
                              life_range=(0.4, 0.9), radius_range=(2, 6 if big else 4.5))
        self.rings.spawn(pos, color, max_radius=90 if big else 55,
                          duration=0.55 if big else 0.4, width=5 if big else 3)

        if ring == "bull":
            self.flashes.spawn((255, 80, 80), alpha0=90, duration=0.22)
            self.callouts.spawn("🎯 БУЛ! 50", (255, 210, 90), pos, duration=1.0, base_size=1.15)
        elif ring == "triple":
            self.flashes.spawn(C.ACCENT, alpha0=55, duration=0.18)
            self.callouts.spawn(f"TRIPLE {hit.value}!", C.ACCENT, pos, duration=0.85)
        elif ring == "outer_bull":
            self.callouts.spawn("25!", (255, 170, 110), pos, duration=0.7, base_size=0.85)
        elif ring == "double":
            self.callouts.spawn(f"DOUBLE {hit.value}!", C.ACCENT_2, pos, duration=0.7, base_size=0.85)

    def on_big_turn(self, pos, total_points):
        """Особый коллаут за суперсильный ход (сумма очков за ход)."""
        if total_points >= 150:
            self.flashes.spawn(C.ACCENT, alpha0=130, duration=0.3)
            self.callouts.spawn(f"🔥 МАКСИМАЛКА! {total_points}", C.ACCENT, pos, duration=1.3, base_size=1.3)
        elif total_points >= 100:
            self.callouts.spawn(f"⚡ ОГОНЬ! {total_points}", C.ACCENT_2, pos, duration=1.0, base_size=1.05)

    def on_button_click(self, pos, color=None):
        self.ripples.spawn(pos, color or C.ACCENT)

    def spawn_confetti(self, width, colors):
        self.confetti.spawn(width, colors)

    def clear_confetti(self):
        self.confetti.clear()

    # --------------------------------------------------------------
    def draw_board_layer(self, surface):
        """Частицы + кольца + коллауты — рисуются поверх мишени."""
        self.particles.draw(surface)
        self.rings.draw(surface)

    def draw_callouts(self, surface, font):
        self.callouts.draw(surface, font)

    def draw_ripples(self, surface):
        self.ripples.draw(surface)

    def draw_flashes(self, surface):
        self.flashes.draw(surface)

    def draw_confetti(self, surface):
        self.confetti.draw(surface)
```

game.py:
```
# -*- coding: utf-8 -*-
"""
game.py — «мозг» игры: очередность ходов, начисление очков, режимы,
undo/skip, определение победителя. Не знает ничего про pygame-рисование
(за исключением того, что хранит координаты точек попаданий для отрисовки
на мишени) — вся отрисовка в ui.py / main.py.
"""

import config as C
from player import Player
from upgrades import roll_upgrade


class GameManager:
    def __init__(self, mode, player_names, team_of=None, dartboard=None):
        """
        mode: одна из config.MODE_*
        player_names: список имён игроков по порядку хода
        team_of: список int (0/1) той же длины, что player_names, для режима "teams"; иначе None
        """
        self.mode = mode
        self.info = C.MODE_INFO[mode]
        self.rounds_total = self.info["rounds"]
        self.teams_mode = self.info["teams"]
        self.dartboard = dartboard

        self.players = []
        for i, name in enumerate(player_names):
            team = team_of[i] if team_of else None
            color = C.TEAM_COLORS[team] if (self.teams_mode and team is not None) \
                else C.PLAYER_COLORS[i % len(C.PLAYER_COLORS)]
            self.players.append(Player(name, color, team=team, index=i))

        self.turn_order = self._build_turn_order()
        self.turn_pointer = 0
        self.round_no = 1
        self.game_over = False
        self.winner_players = []
        self.winner_team = None

        self.undo_stack = []
        self.last_hits = []          # [(pos, color), ...] точки текущего хода
        self.floating_texts = []     # [(text, player), ...] для короткой анимации
        self.awaiting_upgrade = False  # True пока не применили улучшение и не начали ход

        self._start_turn(first=True)

    # ------------------------------------------------------------------
    def _build_turn_order(self):
        n = len(self.players)
        if not self.teams_mode:
            return list(range(n))
        # интерлив команд: T0p0, T1p0, T0p1, T1p1, ...
        by_team = {}
        for i, p in enumerate(self.players):
            by_team.setdefault(p.team, []).append(i)
        order = []
        max_len = max(len(v) for v in by_team.values())
        teams_sorted = sorted(by_team.keys())
        for k in range(max_len):
            for t in teams_sorted:
                if k < len(by_team[t]):
                    order.append(by_team[t][k])
        return order

    @property
    def current_player(self):
        return self.players[self.turn_order[self.turn_pointer]]

    @property
    def darts_per_turn_base(self):
        return C.darts_for_round(self.mode, self.round_no)

    # ------------------------------------------------------------------
    def _start_turn(self, first=False):
        p = self.current_player
        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus - p.pending_dart_penalty
        p.darts_remaining = max(1, base)
        p.pending_dart_penalty = 0
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        p.turn_multiplier = p.perm_multiplier
        p.miss_floor = p.perm_miss_floor
        p.current_round_points = 0
        self.last_hits = []

        # пассивный доход очков от постоянных улучшений — начисляется
        # автоматически в начале каждого хода, до самих бросков
        if p.perm_flat_per_turn:
            p.total_score += p.perm_flat_per_turn
            p.current_round_points += p.perm_flat_per_turn
            self.floating_texts.append((f"+{p.perm_flat_per_turn}", p))

        if self.mode == C.MODE_UPGRADES:
            self.awaiting_upgrade = True
        else:
            self.awaiting_upgrade = False

    def roll_upgrade_for_current(self):
        """Вызывается UI перед началом хода в режиме 'С улучшениями'."""
        return roll_upgrade(self.round_no, self.rounds_total)

    def apply_upgrade(self, upgrade):
        p = self.current_player
        income_before = p.perm_flat_per_turn
        upgrade.apply(self, p)
        p.upgrades_collected.append((upgrade.name, upgrade.duration))

        # постоянные улучшения могли поднять perm_multiplier/perm_miss_floor/доход —
        # применяем их сразу к текущему ходу, т.к. игрок ещё не бросал дротики
        if upgrade.duration == "permanent":
            p.turn_multiplier = p.perm_multiplier
            p.miss_floor = max(p.miss_floor, p.perm_miss_floor)
            income_delta = p.perm_flat_per_turn - income_before
            if income_delta > 0:
                p.total_score += income_delta
                p.current_round_points += income_delta
                self.floating_texts.append((f"+{income_delta}", p))

        # применение улучшения могло изменить extra_darts_bonus/perm_extra_darts —
        # пересчитаем итоговое число дротиков на этот ход
        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus
        p.darts_remaining = max(1, base)
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        self.awaiting_upgrade = False

    # ------------------------------------------------------------------
    def snapshot(self):
        return {
            "players": [p.snapshot() for p in self.players],
            "turn_pointer": self.turn_pointer,
            "round_no": self.round_no,
            "game_over": self.game_over,
            "last_hits": list(self.last_hits),
            "awaiting_upgrade": self.awaiting_upgrade,
        }

    def _push_undo(self):
        self.undo_stack.append(self.snapshot())
        if len(self.undo_stack) > C.UNDO_STACK_LIMIT:
            self.undo_stack.pop(0)

    def can_undo(self):
        return len(self.undo_stack) > 0

    def undo(self):
        if not self.undo_stack:
            return
        snap = self.undo_stack.pop()
        for p, ps in zip(self.players, snap["players"]):
            p.restore(ps)
        self.turn_pointer = snap["turn_pointer"]
        self.round_no = snap["round_no"]
        self.game_over = snap["game_over"]
        self.last_hits = list(snap["last_hits"])
        self.awaiting_upgrade = snap["awaiting_upgrade"]
        self.winner_players = []
        self.winner_team = None

    # ------------------------------------------------------------------
    def throw(self, pos):
        """Бросок дротика мышкой по координате pos на мишени."""
        if self.game_over or self.awaiting_upgrade or not self.dartboard:
            return None
        p = self.current_player
        if p.darts_remaining <= 0:
            return None

        hit = self.dartboard.hit_test(pos)
        self._push_undo()

        points = hit.points
        if hit.ring == "miss" and p.miss_floor > 0:
            points = p.miss_floor
        points = int(round(points * p.turn_multiplier))

        p.total_score += points
        p.current_round_points += points
        p.register_throw(points, hit.ring)
        p.darts_remaining -= 1
        self.last_hits.append((pos, p.color))

        if points != hit.points:
            self.floating_texts.append((f"+{points}", p))

        if p.darts_remaining <= 0:
            self._end_turn()

        return hit

    def skip_turn(self):
        """Пропустить оставшиеся дротики текущего хода без начисления очков."""
        if self.game_over or self.awaiting_upgrade:
            return
        self._push_undo()
        p = self.current_player
        p.darts_remaining = 0
        self._end_turn()

    def _end_turn(self):
        p = self.current_player
        p.finish_round()
        self.turn_pointer += 1
        if self.turn_pointer >= len(self.turn_order):
            self.turn_pointer = 0
            self.round_no += 1
            if self.round_no > self.rounds_total:
                self._finish_game()
                return
        self._start_turn()

    def _finish_game(self):
        self.game_over = True
        if self.teams_mode:
            totals = {}
            for p in self.players:
                totals[p.team] = totals.get(p.team, 0) + p.total_score
            best = max(totals.values())
            self.winner_team = [t for t, v in totals.items() if v == best]
            self.winner_players = [p for p in self.players if p.team in self.winner_team]
        else:
            best = max(p.total_score for p in self.players)
            self.winner_players = [p for p in self.players if p.total_score == best]

    # ------------------------------------------------------------------
    def team_totals(self):
        """dict: team_index -> суммарный счёт (только для teams_mode)."""
        totals = {}
        for p in self.players:
            totals[p.team] = totals.get(p.team, 0) + p.total_score
        return totals

    def players_sorted(self):
        return sorted(self.players, key=lambda p: p.total_score, reverse=True)

    def darts_thrown_progress(self):
        """(брошено, всего) дротиков в текущем ходе — для UI."""
        p = self.current_player
        total = max(p.darts_total_this_turn, 1)
        thrown = total - p.darts_remaining
        return thrown, total
```

main.py:
```
# -*- coding: utf-8 -*-
"""
main.py — точка входа. Управляет окном, экранами (меню -> настройка ->
игра -> итоги) и связывает вместе dartboard.py, game.py, ui.py, upgrades.py,
stats_storage.py.

Запуск:
    python3 main.py

Управление:
    Мышь        — клик по мишени = бросок дротика
    F11         — полноэкранный режим
    ESC         — выйти из полноэкранного режима / закрыть игру в меню
"""

import sys
import pygame

import config as C
from dartboard import Dartboard
from game import GameManager
from upgrades import UpgradeSpinner
import ui
import stats_storage
import emoji_render
import fx

STATE_MENU = "menu"
STATE_SETUP = "setup"
STATE_GAME = "game"
STATE_END = "end"
STATE_LEADERBOARD = "leaderboard"


def pick_font_name():
    available = pygame.font.get_fonts()
    for cand in C.FONT_NAME_CANDIDATES:
        if cand in available:
            return cand
    return None


class App:
    def __init__(self):
        pygame.init()
        emoji_render.init()
        pygame.display.set_caption(C.WINDOW_TITLE)
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode((C.DEFAULT_WIDTH, C.DEFAULT_HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        self.running = True

        self.font_name = pick_font_name()
        self.fonts = {}
        self._rebuild_fonts()

        self.state = STATE_MENU
        self.mode = None
        self.game = None
        self.dartboard = None
        self.fx = fx.EffectsManager()
        self.confetti_spawned = False

        # setup-экран
        self.setup_player_count = 2
        self.setup_inputs = []     # список TextInput
        self.setup_teams = []      # список 0/1 на игрока (для teams)
        self.setup_error = ""

        # игровой экран
        self.spinner = None
        self.spinner_hold_ms = 0
        self.active_floats = []    # [{"text","color","pos","start"}]
        self.stats_recorded = False

        self.leaderboard_rows = []

        self.buttons = {}
        self._layout_dirty = True

    # ------------------------------------------------------------------
    def _rebuild_fonts(self):
        h = self.screen.get_height()
        def sz(frac):
            return max(12, int(h * frac))
        self.fonts = {
            "tiny": pygame.font.SysFont(self.font_name, sz(0.018)),
            "small": pygame.font.SysFont(self.font_name, sz(0.022)),
            "medium": pygame.font.SysFont(self.font_name, sz(0.028)),
            "medium_bold": pygame.font.SysFont(self.font_name, sz(0.030), bold=True),
            "large": pygame.font.SysFont(self.font_name, sz(0.040), bold=True),
            "huge": pygame.font.SysFont(self.font_name, sz(0.055), bold=True),
            "score": pygame.font.SysFont(self.font_name, sz(0.11), bold=True),
            "title": pygame.font.SysFont(self.font_name, sz(0.075), bold=True),
        }

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((C.DEFAULT_WIDTH, C.DEFAULT_HEIGHT), pygame.RESIZABLE)
        self._rebuild_fonts()
        self._layout_dirty = True
        if self.dartboard:
            self.dartboard.set_rect(self._compute_layout()["board"])

    # ------------------------------------------------------------------
    def _compute_layout(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        board_w = int(w * C.BOARD_PANEL_RATIO)
        margin = int(h * 0.025)

        board_rect = pygame.Rect(margin, margin, board_w - margin * 2, h - margin * 2)
        # квадратизируем и центрируем по вертикали
        side = min(board_rect.width, board_rect.height)
        board_rect = pygame.Rect(0, 0, side, side)
        board_rect.center = (margin + (board_w - margin * 2) // 2, h // 2)

        right_x = board_w
        right_w = w - board_w - margin
        player_panel = pygame.Rect(right_x, margin, right_w, int(h * 0.42))
        scoreboard = pygame.Rect(right_x, player_panel.bottom + margin,
                                  right_w, int(h * 0.36))
        buttons_area = pygame.Rect(right_x, scoreboard.bottom + margin,
                                    right_w, h - scoreboard.bottom - margin * 2)
        return {"board": board_rect, "player_panel": player_panel,
                "scoreboard": scoreboard, "buttons": buttons_area}

    def _build_game_buttons(self, layout):
        self.buttons.clear()
        area = layout["buttons"]
        gap = int(area.width * 0.02)
        bw = (area.width - gap * 2) // 3
        bh = min(area.height, int(self.screen.get_height() * 0.075))
        y = area.top + (area.height - bh) // 2
        self.buttons["new_game"] = ui.Button((area.left, y, bw, bh), "🔄 Новая игра",
                                              self.fonts["medium_bold"], style="ghost")
        self.buttons["undo"] = ui.Button((area.left + bw + gap, y, bw, bh), "↩️ Отменить",
                                          self.fonts["medium_bold"], style="normal",
                                          enabled=self.game.can_undo() if self.game else False)
        self.buttons["skip"] = ui.Button((area.left + (bw + gap) * 2, y, bw, bh), "⏭️ Пропустить",
                                          self.fonts["medium_bold"], style="danger")
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons.values():
            b.hovered = b.enabled and b.rect.collidepoint(mouse_pos)

    # ------------------------------------------------------------------
    # MENU
    # ------------------------------------------------------------------
    def _draw_menu(self):
        self._draw_background()
        w, h = self.screen.get_width(), self.screen.get_height()
        title = emoji_render.rtext(self.fonts["title"], "🎯 ДАРТС — Домашний счёт", C.ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))
        sub = emoji_render.rtext(self.fonts["medium"], "Выберите режим игры 👇", C.TEXT_DIM)
        self.screen.blit(sub, sub.get_rect(center=(w // 2, int(h * 0.16))))

        modes = list(C.MODE_INFO.keys())
        cols = 3 if w > 1200 else 2 if w > 800 else 1
        rows = (len(modes) + cols - 1) // cols
        pad = int(w * 0.03)
        area_top = int(h * 0.22)
        area_bottom = int(h * 0.88)
        card_w = (w - pad * (cols + 1)) // cols
        card_h = min(int((area_bottom - area_top - pad * (rows - 1)) / rows), int(h * 0.28))

        self.buttons.clear()
        for i, mode_key in enumerate(modes):
            col = i % cols
            row = i // cols
            x = pad + col * (card_w + pad)
            y = area_top + row * (card_h + pad)
            rect = pygame.Rect(x, y, card_w, card_h)
            info = C.MODE_INFO[mode_key]
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            bg = C.PANEL_BG_LIGHT if hovered else C.PANEL_BG
            ui.draw_panel(self.screen, rect, bg=bg, border=C.ACCENT if hovered else C.PANEL_BORDER)

            title_s = emoji_render.rtext(self.fonts["large"], f"{info['icon']} {info['title']}", C.ACCENT)
            self.screen.blit(title_s, (rect.left + 20, rect.top + 16))
            lines = ui.render_text_wrapped(self.fonts["small"], info["desc"], C.TEXT_DIM, rect.width - 40)
            ly = rect.top + 16 + title_s.get_height() + 12
            for line in lines:
                self.screen.blit(line, (rect.left + 20, ly))
                ly += line.get_height() + 4

            rounds_txt = self.fonts["tiny"].render(
                f"Раундов: {info['rounds']}  •  Игроков: {info['min_players']}-{info['max_players']}",
                True, C.TEXT_DIM2)
            self.screen.blit(rounds_txt, (rect.left + 20, rect.bottom - rounds_txt.get_height() - 14))

            self.buttons[f"mode_{mode_key}"] = rect

        # кнопка статистики
        lb_rect = pygame.Rect(w - int(w * 0.22) - pad, int(h * 0.02), int(w * 0.22), int(h * 0.05))
        ui.draw_panel(self.screen, lb_rect, bg=C.PANEL_BG_LIGHT, border=C.ACCENT_2)
        lb_txt = emoji_render.rtext(self.fonts["small"], "📊 Статистика игроков", C.ACCENT_2)
        self.screen.blit(lb_txt, lb_txt.get_rect(center=lb_rect.center))
        self.buttons["leaderboard"] = lb_rect
        self.fx.draw_ripples(self.screen)

    def _handle_menu_click(self, pos):
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.fx.on_button_click(pos, C.ACCENT)
                if key == "leaderboard":
                    self.leaderboard_rows = stats_storage.leaderboard()
                    self.state = STATE_LEADERBOARD
                    return
                if key.startswith("mode_"):
                    self.mode = key[len("mode_"):]
                    info = C.MODE_INFO[self.mode]
                    self.setup_player_count = info["min_players"]
                    self._build_setup_inputs()
                    self.setup_error = ""
                    self.state = STATE_SETUP
                    return

    # ------------------------------------------------------------------
    # SETUP
    # ------------------------------------------------------------------
    def _build_setup_inputs(self):
        self.setup_inputs = []
        self.setup_teams = []
        for i in range(self.setup_player_count):
            ti = ui.TextInput((0, 0, 10, 10), self.fonts["medium"], text=f"Игрок {i + 1}",
                               placeholder=f"Игрок {i + 1}", max_len=14)
            self.setup_inputs.append(ti)
            self.setup_teams.append(i % 2)

    def _draw_setup(self):
        self._draw_background()
        w, h = self.screen.get_width(), self.screen.get_height()
        info = C.MODE_INFO[self.mode]

        title = emoji_render.rtext(self.fonts["large"], f"{info['icon']} Настройка: {info['title']}", C.ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.08))))

        panel = pygame.Rect(int(w * 0.2), int(h * 0.16), int(w * 0.6), int(h * 0.66))
        ui.draw_panel(self.screen, panel)

        pad = int(panel.width * 0.05)
        y = panel.top + pad

        self.buttons.clear()
        if info["min_players"] != info["max_players"]:
            cnt_label = self.fonts["medium"].render(
                f"Количество игроков: {self.setup_player_count}", True, C.TEXT_MAIN)
            self.screen.blit(cnt_label, (panel.left + pad, y))
            minus_rect = pygame.Rect(panel.right - pad - 160, y - 6, 70, 44)
            plus_rect = pygame.Rect(panel.right - pad - 80, y - 6, 70, 44)
            ui.Button(minus_rect, "-", self.fonts["medium_bold"]).draw(self.screen)
            ui.Button(plus_rect, "+", self.fonts["medium_bold"]).draw(self.screen)
            self.buttons["count_minus"] = minus_rect
            self.buttons["count_plus"] = plus_rect
            y += 60

        input_h = max(40, int(h * 0.05))
        input_w = int(panel.width * 0.5) if not info["teams"] else int(panel.width * 0.38)
        for i, ti in enumerate(self.setup_inputs):
            ti.rect = pygame.Rect(panel.left + pad, y, input_w, input_h)
            ti.font = self.fonts["medium"]
            ti.draw(self.screen)
            if info["teams"]:
                team_rect = pygame.Rect(ti.rect.right + 16, y, panel.width - pad * 2 - input_w - 16, input_h)
                team_color = C.TEAM_COLORS[self.setup_teams[i]]
                pygame.draw.rect(self.screen, C.PANEL_BG_LIGHT, team_rect, border_radius=10)
                pygame.draw.rect(self.screen, team_color, team_rect, 2, border_radius=10)
                team_txt = self.fonts["small"].render(f"Команда {self.setup_teams[i] + 1} (клик — сменить)",
                                                        True, team_color)
                self.screen.blit(team_txt, team_txt.get_rect(center=team_rect.center))
                self.buttons[f"team_{i}"] = team_rect
            y += input_h + 14

        if self.setup_error:
            err = self.fonts["small"].render(self.setup_error, True, C.DANGER)
            self.screen.blit(err, (panel.left + pad, panel.bottom - pad - err.get_height() - 60))

        start_rect = pygame.Rect(panel.centerx - 140, panel.bottom - pad - 50, 280, 50)
        back_rect = pygame.Rect(panel.left + pad, panel.bottom - pad - 50, 140, 50)
        ui.Button(start_rect, "▶️ Начать игру", self.fonts["medium_bold"], style="accent").draw(self.screen)
        ui.Button(back_rect, "⬅️ Назад", self.fonts["medium_bold"], style="ghost").draw(self.screen)
        self.buttons["start"] = start_rect
        self.buttons["back"] = back_rect

    def _handle_setup_event(self, event):
        for ti in self.setup_inputs:
            ti.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if not rect.collidepoint(event.pos):
                    continue
                if key == "count_plus":
                    info = C.MODE_INFO[self.mode]
                    if self.setup_player_count < info["max_players"]:
                        self.setup_player_count += 1
                        self._build_setup_inputs()
                elif key == "count_minus":
                    info = C.MODE_INFO[self.mode]
                    if self.setup_player_count > info["min_players"]:
                        self.setup_player_count -= 1
                        self._build_setup_inputs()
                elif key.startswith("team_"):
                    idx = int(key.split("_")[1])
                    self.setup_teams[idx] = 1 - self.setup_teams[idx]
                elif key == "start":
                    self._try_start_game()
                elif key == "back":
                    self.state = STATE_MENU

    def _try_start_game(self):
        names = [ti.text.strip() or f"Игрок {i+1}" for i, ti in enumerate(self.setup_inputs)]
        if len(set(n.lower() for n in names)) != len(names):
            self.setup_error = "Имена игроков должны быть разными!"
            return
        info = C.MODE_INFO[self.mode]
        team_of = self.setup_teams if info["teams"] else None
        if info["teams"] and (0 not in team_of or 1 not in team_of):
            self.setup_error = "В обеих командах должен быть хотя бы один игрок!"
            return

        layout = self._compute_layout()
        self.dartboard = Dartboard(layout["board"])
        self.game = GameManager(self.mode, names, team_of=team_of, dartboard=self.dartboard)
        self.spinner = None
        self.active_floats = []
        self.stats_recorded = False
        self.confetti_spawned = False
        self.state = STATE_GAME

    # ------------------------------------------------------------------
    # GAME
    # ------------------------------------------------------------------
    def _draw_game(self):
        self._draw_background()
        layout = self._compute_layout()
        if self.dartboard.rect != layout["board"]:
            self.dartboard.set_rect(layout["board"])
        self._build_game_buttons(layout)

        hover = None
        if self.dartboard.rect.collidepoint(pygame.mouse.get_pos()) and not self.game.awaiting_upgrade:
            hover = pygame.mouse.get_pos()
        self.dartboard.draw(self.screen, hover_pos=hover, last_hits=self.game.last_hits)
        self.fx.draw_board_layer(self.screen)          # частицы + пульс-кольца поверх мишени

        ui.draw_player_panel(self.screen, layout["player_panel"], self.game, self.fonts)
        ui.draw_scoreboard(self.screen, layout["scoreboard"], self.game, self.fonts)

        for b in self.buttons.values():
            b.draw(self.screen)
        self.fx.draw_ripples(self.screen)               # рябь от клика по кнопкам

        self._draw_floating_texts()
        self.fx.draw_callouts(self.screen, self.fonts["large"])  # "БУЛ!", "TRIPLE!" и т.д.
        self.fx.draw_flashes(self.screen)                # вспышка экрана на крутых попаданиях

        if self.game.mode == C.MODE_UPGRADES and self.game.awaiting_upgrade:
            self._draw_upgrade_spinner(layout)

        if self.game.game_over:
            if not self.stats_recorded:
                stats_storage.record_game(self.game)
                self.stats_recorded = True
            self.state = STATE_END

    def _draw_upgrade_spinner(self, layout):
        w, h = self.screen.get_width(), self.screen.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((5, 5, 8, 190))
        self.screen.blit(overlay, (0, 0))

        p = self.game.current_player
        name_txt = emoji_render.rtext(self.fonts["large"], f"🎁 {p.name}, твоё улучшение…", p.color)
        self.screen.blit(name_txt, name_txt.get_rect(center=(w // 2, int(h * 0.22))))

        panel_w = min(560, int(w * 0.4))
        panel_h = int(h * 0.42)
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (w // 2, h // 2)

        if self.spinner is None:
            result = self.game.roll_upgrade_for_current()
            self.spinner = UpgradeSpinner(result)

        self.spinner.draw(self.screen, panel_rect, self.fonts["large"], self.fonts["small"], self.fonts["tiny"])

        if self.spinner.done:
            self.spinner_hold_ms += self.clock.get_time()
            hint = emoji_render.rtext(self.fonts["small"], "👉 Клик, чтобы продолжить", C.TEXT_DIM)
            self.screen.blit(hint, hint.get_rect(center=(w // 2, panel_rect.bottom + 40)))

    def _draw_floating_texts(self):
        now = pygame.time.get_ticks()
        alive = []
        for f in self.active_floats:
            age = now - f["start"]
            if age > 1200:
                continue
            alive.append(f)
            t = age / 1200
            alpha = int(255 * (1 - t))
            y_off = -30 * t
            surf = self.fonts["large"].render(f["text"], True, f["color"])
            surf.set_alpha(alpha)
            pos = (f["pos"][0], f["pos"][1] + y_off)
            self.screen.blit(surf, surf.get_rect(center=pos))
        self.active_floats = alive

    def _spawn_floats_from_game(self, layout):
        if not self.game.floating_texts:
            return
        base_pos = layout["player_panel"].center
        for text, player in self.game.floating_texts:
            self.active_floats.append({
                "text": text, "color": player.color,
                "pos": (base_pos[0], base_pos[1] - 40),
                "start": pygame.time.get_ticks(),
            })
        self.game.floating_texts = []

    def _handle_game_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.game.mode == C.MODE_UPGRADES and self.game.awaiting_upgrade:
                if self.spinner and self.spinner.done and self.spinner_hold_ms > 150:
                    self.game.apply_upgrade(self.spinner.result)
                    self.spinner = None
                    self.spinner_hold_ms = 0
                return
            for key, btn in self.buttons.items():
                if btn.rect.collidepoint(pos):
                    self.fx.on_button_click(pos, C.ACCENT if key != "skip" else C.DANGER)
                    if key == "new_game":
                        self.state = STATE_MENU
                    elif key == "undo":
                        self.game.undo()
                    elif key == "skip":
                        self.game.skip_turn()
                    return
            if self.dartboard.rect.collidepoint(pos):
                thrower = self.game.current_player
                rounds_before = len(thrower.round_scores)
                hit = self.game.throw(pos)
                if hit is not None:
                    self.fx.on_hit(pos, hit, thrower.color)
                    if len(thrower.round_scores) > rounds_before:
                        # ход только что завершился — проверим, не суперсильный ли он
                        self.fx.on_big_turn(pos, thrower.round_scores[-1])
                layout = self._compute_layout()
                self._spawn_floats_from_game(layout)

    # ------------------------------------------------------------------
    # END SCREEN
    # ------------------------------------------------------------------
    def _draw_end(self):
        self._draw_background()
        w, h = self.screen.get_width(), self.screen.get_height()
        game = self.game

        if not self.confetti_spawned:
            colors = [p.color for p in (game.winner_players or game.players)] or [C.ACCENT, C.ACCENT_2]
            self.fx.spawn_confetti(w, colors)
            self.confetti_spawned = True

        if game.teams_mode:
            if len(game.winner_team) > 1:
                winner_txt = "🤝 Ничья между командами " + " и ".join(str(t + 1) for t in game.winner_team) + "!"
            else:
                winner_txt = f"🏆 Победила команда {game.winner_team[0] + 1}! 🎉"
        else:
            names = ", ".join(p.name for p in game.winner_players)
            winner_txt = f"🏆 Победитель: {names}! 🎉" if len(game.winner_players) == 1 else f"🤝 Ничья: {names}!"

        title = emoji_render.rtext(self.fonts["title"], winner_txt, C.ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))

        panel = pygame.Rect(int(w * 0.15), int(h * 0.18), int(w * 0.7), int(h * 0.62))
        ui.draw_panel(self.screen, panel)

        pad = 24
        y = panel.top + pad
        cols_x = [panel.left + pad, panel.left + int(panel.width * 0.34),
                  panel.left + int(panel.width * 0.52), panel.left + int(panel.width * 0.70),
                  panel.left + int(panel.width * 0.86)]
        headers = ["Игрок", "Очки", "Ср/дротик", "Точность", "Лучший ход"]
        for hx, htext in zip(cols_x, headers):
            hs = self.fonts["small"].render(htext, True, C.TEXT_DIM)
            self.screen.blit(hs, (hx, y))
        y += 30
        pygame.draw.line(self.screen, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 2)
        y += 10

        medals = ["🥇 ", "🥈 ", "🥉 "]
        for rank, p in enumerate(game.players_sorted()):
            row_color = p.color
            name_display = (medals[rank] if rank < 3 else "") + p.name
            vals = [name_display, str(p.total_score), f"{p.average_per_dart:.1f}",
                    f"{p.accuracy_percent:.0f}%", str(p.best_round)]
            for hx, v in zip(cols_x, vals):
                if hx == cols_x[0]:
                    vs = emoji_render.rtext(self.fonts["medium"], v, row_color)
                else:
                    vs = self.fonts["medium"].render(v, True, C.TEXT_MAIN)
                self.screen.blit(vs, (hx, y))
            y += int(self.fonts["medium"].get_height() * 1.6)

        if game.mode == C.MODE_UPGRADES and y < panel.bottom - pad - 20:
            pygame.draw.line(self.screen, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 1)
            y += 10
            perm_header = emoji_render.rtext(self.fonts["small"], "♾️ Постоянные улучшения за партию:", C.ACCENT_2)
            self.screen.blit(perm_header, (panel.left + pad, y))
            y += perm_header.get_height() + 4
            for p in game.players_sorted():
                if y > panel.bottom - pad - 20:
                    break
                perm_names = [name for name, dur in p.upgrades_collected if dur == "permanent"]
                line = f"{p.name}: " + (", ".join(perm_names) if perm_names else "—")
                ls = emoji_render.rtext(self.fonts["tiny"], line, p.color)
                self.screen.blit(ls, (panel.left + pad, y))
                y += ls.get_height() + 3

        self.buttons.clear()
        again_rect = pygame.Rect(w // 2 - 220, panel.bottom + 24, 200, 54)
        menu_rect = pygame.Rect(w // 2 + 20, panel.bottom + 24, 200, 54)
        ui.Button(again_rect, "🔁 Ещё раз", self.fonts["medium_bold"], style="accent").draw(self.screen)
        ui.Button(menu_rect, "🏠 В меню", self.fonts["medium_bold"], style="ghost").draw(self.screen)
        self.buttons["again"] = again_rect
        self.buttons["to_menu"] = menu_rect

        self.fx.draw_confetti(self.screen)  # конфетти рисуем поверх всего
        self.fx.draw_ripples(self.screen)

    def _handle_end_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    self.fx.on_button_click(event.pos, C.ACCENT)
                    if key == "again":
                        names = [p.name for p in self.game.players]
                        team_of = [p.team for p in self.game.players] if self.game.teams_mode else None
                        layout = self._compute_layout()
                        self.dartboard.set_rect(layout["board"])
                        self.game = GameManager(self.mode, names, team_of=team_of, dartboard=self.dartboard)
                        self.stats_recorded = False
                        self.active_floats = []
                        self.confetti_spawned = False
                        self.state = STATE_GAME
                    elif key == "to_menu":
                        self.state = STATE_MENU

    # ------------------------------------------------------------------
    # LEADERBOARD
    # ------------------------------------------------------------------
    def _draw_leaderboard(self):
        self._draw_background()
        w, h = self.screen.get_width(), self.screen.get_height()
        title = emoji_render.rtext(self.fonts["title"], "📊 Статистика игроков", C.ACCENT_2)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))

        panel = pygame.Rect(int(w * 0.12), int(h * 0.2), int(w * 0.76), int(h * 0.62))
        ui.draw_panel(self.screen, panel)

        if not self.leaderboard_rows:
            empty = self.fonts["medium"].render("Пока нет сыгранных партий.", True, C.TEXT_DIM)
            self.screen.blit(empty, empty.get_rect(center=panel.center))
        else:
            pad = 24
            cols_x = [panel.left + pad, panel.left + int(panel.width * 0.30),
                      panel.left + int(panel.width * 0.45), panel.left + int(panel.width * 0.60),
                      panel.left + int(panel.width * 0.76), panel.left + int(panel.width * 0.90)]
            headers = ["Игрок", "Партий", "Побед", "Ср/дротик", "Лучший ход", "Лучший бросок"]
            y = panel.top + pad
            for hx, htext in zip(cols_x, headers):
                hs = self.fonts["small"].render(htext, True, C.TEXT_DIM)
                self.screen.blit(hs, (hx, y))
            y += 30
            pygame.draw.line(self.screen, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 2)
            y += 10
            for row in self.leaderboard_rows:
                vals = [row["name"], str(row["games"]), f'{row["wins"]} ({row["winrate"]:.0f}%)',
                        f'{row["avg"]:.1f}', str(row["best_round"]), str(row["best_single"])]
                for hx, v in zip(cols_x, vals):
                    vs = self.fonts["medium"].render(v, True, C.TEXT_MAIN)
                    self.screen.blit(vs, (hx, y))
                y += int(self.fonts["medium"].get_height() * 1.6)

        self.buttons.clear()
        back_rect = pygame.Rect(w // 2 - 100, panel.bottom + 24, 200, 54)
        ui.Button(back_rect, "⬅️ Назад", self.fonts["medium_bold"], style="ghost").draw(self.screen)
        self.buttons["back"] = back_rect
        self.fx.draw_ripples(self.screen)

    def _handle_leaderboard_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buttons.get("back") and self.buttons["back"].collidepoint(event.pos):
                self.fx.on_button_click(event.pos, C.ACCENT_2)
                self.state = STATE_MENU

    # ------------------------------------------------------------------
    def _draw_background(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        ui.draw_vertical_gradient(self.screen, (0, 0, w, h), C.BG_TOP, C.BG_BOTTOM)

    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(C.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        (max(C.MIN_WIDTH, event.w), max(C.MIN_HEIGHT, event.h)), pygame.RESIZABLE)
                    self._rebuild_fonts()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        if self.fullscreen:
                            self.toggle_fullscreen()
                        elif self.state == STATE_MENU:
                            self.running = False

                if self.state == STATE_MENU:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self._handle_menu_click(event.pos)
                elif self.state == STATE_SETUP:
                    self._handle_setup_event(event)
                elif self.state == STATE_GAME:
                    self._handle_game_event(event)
                    for b in self.buttons.values():
                        if hasattr(b, "handle_event"):
                            b.handle_event(event)
                elif self.state == STATE_END:
                    self._handle_end_event(event)
                elif self.state == STATE_LEADERBOARD:
                    self._handle_leaderboard_event(event)

            for ti in self.setup_inputs:
                ti.update(dt)

            self.fx.update(dt / 1000.0)

            if self.state == STATE_MENU:
                self._draw_menu()
            elif self.state == STATE_SETUP:
                self._draw_setup()
            elif self.state == STATE_GAME:
                self._draw_game()
            elif self.state == STATE_END:
                self._draw_end()
            elif self.state == STATE_LEADERBOARD:
                self._draw_leaderboard()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
```

player.py:
```
# -*- coding: utf-8 -*-
"""
player.py — модель игрока и его статистики в рамках одной партии.
"""


class Player:
    def __init__(self, name, color, team=None, index=0):
        self.name = name
        self.color = color
        self.team = team          # None или индекс команды (0/1)
        self.index = index

        self.total_score = 0
        self.round_scores = []    # список очков за каждый завершённый раунд
        self.current_round_points = 0

        # состояние текущего хода (сбрасывается после хода)
        self.darts_remaining = 0
        self.darts_total_this_turn = 0  # сколько дротиков положено в этом ходе (для UI)
        self.turn_multiplier = 1        # эффект улучшений: множитель очков за ход
        self.extra_darts_bonus = 0      # эффект улучшений: доп. дротики
        self.miss_floor = 0             # эффект улучшений: промах засчитывается как N очков

        # ПОСТОЯННЫЕ (пассивные) эффекты — действуют до конца всей партии,
        # накапливаются при выпадении улучшений с duration="permanent"
        self.perm_multiplier = 1.0      # постоянный множитель очков (стакается умножением)
        self.perm_extra_darts = 0       # доп. дротики каждый ход до конца игры
        self.perm_flat_per_turn = 0     # пассивный доход очков в начале каждого хода
        self.perm_miss_floor = 0        # промахи навсегда считаются как минимум N очков
        self.perm_shield = 0.0          # доля (0..0.9) снижения урона от краж/атак соперников
        self.pending_dart_penalty = 0   # временный "минус дротик" от чужой диверсии (на след. ход)

        # статистика на партию
        self.throws_count = 0
        self.miss_count = 0
        self.single_count = 0
        self.double_count = 0
        self.triple_count = 0
        self.bull_count = 0
        self.outer_bull_count = 0
        self.best_single_throw = 0
        self.best_round = 0
        self.upgrades_collected = []    # список (name, duration) — для истории партии

    def register_throw(self, hit_points, ring):
        self.throws_count += 1
        if ring == "miss":
            self.miss_count += 1
        elif ring == "single":
            self.single_count += 1
        elif ring == "double":
            self.double_count += 1
        elif ring == "triple":
            self.triple_count += 1
        elif ring == "bull":
            self.bull_count += 1
        elif ring == "outer_bull":
            self.outer_bull_count += 1
        if hit_points > self.best_single_throw:
            self.best_single_throw = hit_points

    def finish_round(self):
        self.round_scores.append(self.current_round_points)
        if self.current_round_points > self.best_round:
            self.best_round = self.current_round_points
        self.current_round_points = 0

    @property
    def average_per_dart(self):
        if self.throws_count == 0:
            return 0.0
        return self.total_score / self.throws_count

    @property
    def accuracy_percent(self):
        if self.throws_count == 0:
            return 0.0
        hits = self.throws_count - self.miss_count
        return 100.0 * hits / self.throws_count

    def snapshot(self):
        """Лёгкий словарь-снимок для undo (без ссылок на изменяемые вложенные списки)."""
        return {
            "total_score": self.total_score,
            "round_scores": list(self.round_scores),
            "current_round_points": self.current_round_points,
            "darts_remaining": self.darts_remaining,
            "darts_total_this_turn": self.darts_total_this_turn,
            "turn_multiplier": self.turn_multiplier,
            "extra_darts_bonus": self.extra_darts_bonus,
            "miss_floor": self.miss_floor,
            "perm_multiplier": self.perm_multiplier,
            "perm_extra_darts": self.perm_extra_darts,
            "perm_flat_per_turn": self.perm_flat_per_turn,
            "perm_miss_floor": self.perm_miss_floor,
            "perm_shield": self.perm_shield,
            "pending_dart_penalty": self.pending_dart_penalty,
            "throws_count": self.throws_count,
            "miss_count": self.miss_count,
            "single_count": self.single_count,
            "double_count": self.double_count,
            "triple_count": self.triple_count,
            "bull_count": self.bull_count,
            "outer_bull_count": self.outer_bull_count,
            "best_single_throw": self.best_single_throw,
            "best_round": self.best_round,
            "upgrades_collected": list(self.upgrades_collected),
        }

    def restore(self, snap):
        self.total_score = snap["total_score"]
        self.round_scores = list(snap["round_scores"])
        self.current_round_points = snap["current_round_points"]
        self.darts_remaining = snap["darts_remaining"]
        self.darts_total_this_turn = snap.get("darts_total_this_turn", self.darts_remaining)
        self.turn_multiplier = snap["turn_multiplier"]
        self.extra_darts_bonus = snap["extra_darts_bonus"]
        self.miss_floor = snap.get("miss_floor", 0)
        self.perm_multiplier = snap.get("perm_multiplier", 1.0)
        self.perm_extra_darts = snap.get("perm_extra_darts", 0)
        self.perm_flat_per_turn = snap.get("perm_flat_per_turn", 0)
        self.perm_miss_floor = snap.get("perm_miss_floor", 0)
        self.perm_shield = snap.get("perm_shield", 0.0)
        self.pending_dart_penalty = snap.get("pending_dart_penalty", 0)
        self.throws_count = snap["throws_count"]
        self.miss_count = snap["miss_count"]
        self.single_count = snap["single_count"]
        self.double_count = snap["double_count"]
        self.triple_count = snap["triple_count"]
        self.bull_count = snap["bull_count"]
        self.outer_bull_count = snap["outer_bull_count"]
        self.best_single_throw = snap["best_single_throw"]
        self.best_round = snap["best_round"]
        self.upgrades_collected = list(snap["upgrades_collected"])
```

stats_storage.py:
```
# -*- coding: utf-8 -*-
"""
stats_storage.py — простая персистентная статистика игроков между запусками
игры. Хранится в JSON-файле рядом со скриптом (darts_stats.json).
"""

import json
import os
import config as C


def _empty_db():
    return {"players": {}, "games_played": 0}


def load_db():
    if not os.path.exists(C.STATS_FILE):
        return _empty_db()
    try:
        with open(C.STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "players" not in data:
            return _empty_db()
        return data
    except (json.JSONDecodeError, OSError):
        return _empty_db()


def save_db(db):
    try:
        with open(C.STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # если нет прав на запись — молча пропускаем, игра не должна падать


def record_game(game_manager):
    """Сохраняет результаты завершённой партии в базу статистики."""
    db = load_db()
    db["games_played"] = db.get("games_played", 0) + 1
    is_winner_ids = {id(p) for p in game_manager.winner_players}

    for p in game_manager.players:
        entry = db["players"].setdefault(p.name, {
            "games": 0, "wins": 0, "total_points": 0, "total_throws": 0,
            "best_round_ever": 0, "best_single_ever": 0,
            "bulls": 0, "triples": 0, "doubles": 0,
        })
        entry["games"] += 1
        if id(p) in is_winner_ids:
            entry["wins"] += 1
        entry["total_points"] += p.total_score
        entry["total_throws"] += p.throws_count
        entry["best_round_ever"] = max(entry["best_round_ever"], p.best_round)
        entry["best_single_ever"] = max(entry["best_single_ever"], p.best_single_throw)
        entry["bulls"] += p.bull_count
        entry["triples"] += p.triple_count
        entry["doubles"] += p.double_count

    save_db(db)
    return db


def leaderboard(db=None, limit=10):
    """Топ игроков по среднему очков за дротик (минимум 1 партия)."""
    db = db or load_db()
    rows = []
    for name, e in db["players"].items():
        avg = e["total_points"] / e["total_throws"] if e["total_throws"] else 0
        winrate = 100.0 * e["wins"] / e["games"] if e["games"] else 0
        rows.append({
            "name": name, "games": e["games"], "wins": e["wins"],
            "avg": avg, "winrate": winrate,
            "best_round": e["best_round_ever"], "best_single": e["best_single_ever"],
        })
    rows.sort(key=lambda r: r["avg"], reverse=True)
    return rows[:limit]
```

ui.py:
```
# -*- coding: utf-8 -*-
"""
ui.py — переиспользуемые виджеты интерфейса: кнопки, текстовые поля,
панели, отрисовка таблицы счёта и панели текущего игрока.
"""

import math
import pygame
import config as C
import emoji_render


# ==========================================================================
# БАЗОВЫЕ ХЕЛПЕРЫ
# ==========================================================================
def draw_vertical_gradient(surface, rect, top_color, bottom_color):
    x, y, w, h = rect
    if h <= 0:
        return
    for i in range(h):
        t = i / h
        color = tuple(int(top_color[c] + (bottom_color[c] - top_color[c]) * t) for c in range(3))
        pygame.draw.line(surface, color, (x, y + i), (x + w, y + i))


def draw_panel(surface, rect, radius=16, bg=C.PANEL_BG, border=C.PANEL_BORDER, border_w=2):
    pygame.draw.rect(surface, bg, rect, border_radius=radius)
    if border_w > 0:
        pygame.draw.rect(surface, border, rect, border_w, border_radius=radius)


def render_text_wrapped(font, text, color, max_width):
    """Возвращает список отрендеренных Surface, по одной на строку."""
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.size(trial)[0] <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return [font.render(line, True, color) for line in lines]


# ==========================================================================
# КНОПКА
# ==========================================================================
class Button:
    def __init__(self, rect, text, font, style="normal", enabled=True, subtext=None, subfont=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.style = style  # normal | accent | danger | ghost
        self.enabled = enabled
        self.hovered = False
        self.subtext = subtext
        self.subfont = subfont

    def handle_event(self, event):
        clicked = False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.enabled and self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled and self.rect.collidepoint(event.pos):
                clicked = True
        return clicked

    def draw(self, surface):
        if not self.enabled:
            bg = (36, 38, 46)
            text_color = C.TEXT_DIM2
            border = C.PANEL_BORDER
        elif self.style == "accent":
            bg = C.ACCENT if not self.hovered else (255, 210, 60)
            text_color = C.BUTTON_TEXT_ACTIVE
            border = C.ACCENT
        elif self.style == "danger":
            bg = C.DANGER if self.hovered else (150, 50, 55)
            text_color = C.TEXT_MAIN
            border = C.DANGER
        elif self.style == "ghost":
            bg = C.PANEL_BG_LIGHT if self.hovered else C.PANEL_BG
            text_color = C.TEXT_MAIN
            border = C.PANEL_BORDER
        else:
            bg = C.BUTTON_BG_HOVER if self.hovered else C.BUTTON_BG
            text_color = C.BUTTON_TEXT
            border = C.PANEL_BORDER

        radius = max(8, self.rect.height // 4)
        pygame.draw.rect(surface, bg, self.rect, border_radius=radius)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=radius)

        label = emoji_render.rtext(self.font, self.text, text_color)
        if self.subtext:
            sub = emoji_render.rtext(self.subfont, self.subtext, text_color)
            total_h = label.get_height() + sub.get_height() + 2
            label_y = self.rect.centery - total_h // 2
            surface.blit(label, label.get_rect(midtop=(self.rect.centerx, label_y)))
            surface.blit(sub, sub.get_rect(midtop=(self.rect.centerx, label_y + label.get_height() + 2)))
        else:
            surface.blit(label, label.get_rect(center=self.rect.center))


# ==========================================================================
# ТЕКСТОВОЕ ПОЛЕ ВВОДА
# ==========================================================================
class TextInput:
    def __init__(self, rect, font, text="", placeholder="", max_len=16):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text = text
        self.placeholder = placeholder
        self.max_len = max_len
        self.active = False
        self._cursor_visible = True
        self._cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                self.active = False
            elif event.unicode and event.unicode.isprintable() and len(self.text) < self.max_len:
                self.text += event.unicode

    def update(self, dt_ms):
        self._cursor_timer += dt_ms
        if self._cursor_timer >= 500:
            self._cursor_timer = 0
            self._cursor_visible = not self._cursor_visible

    def draw(self, surface):
        bg = C.PANEL_BG_LIGHT if self.active else C.PANEL_BG
        border = C.ACCENT if self.active else C.PANEL_BORDER
        pygame.draw.rect(surface, bg, self.rect, border_radius=10)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=10)

        if self.text:
            label = self.font.render(self.text, True, C.TEXT_MAIN)
        else:
            label = self.font.render(self.placeholder, True, C.TEXT_DIM2)
        surface.blit(label, label.get_rect(midleft=(self.rect.left + 14, self.rect.centery)))

        if self.active and self._cursor_visible:
            tw = self.font.size(self.text)[0]
            cx = self.rect.left + 14 + tw + 2
            pygame.draw.line(surface, C.ACCENT, (cx, self.rect.top + 10), (cx, self.rect.bottom - 10), 2)


# ==========================================================================
# ПАНЕЛЬ ТЕКУЩЕГО ИГРОКА
# ==========================================================================
def draw_player_panel(surface, rect, game, fonts):
    draw_panel(surface, rect)
    p = game.current_player
    pad = int(rect.height * 0.06)

    # пульсирующее свечение вокруг панели текущего игрока — привлекает взгляд,
    # особенно полезно с дивана перед телевизором
    pulse = (math.sin(pygame.time.get_ticks() / 320.0) + 1) / 2  # 0..1
    glow_alpha = int(50 + 90 * pulse)
    glow_pad = 8
    glow_surf = pygame.Surface((rect.width + glow_pad * 2, rect.height + glow_pad * 2), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*p.color, glow_alpha), glow_surf.get_rect(),
                      width=4, border_radius=22)
    surface.blit(glow_surf, (rect.left - glow_pad, rect.top - glow_pad))

    # цветная полоска-акцент игрока
    pygame.draw.rect(surface, p.color, (rect.left, rect.top, rect.width, 8),
                      border_top_left_radius=16, border_top_right_radius=16)

    y = rect.top + pad + 6
    label = emoji_render.rtext(fonts["small"], "🎯 ХОДИТ СЕЙЧАС", C.TEXT_DIM)
    surface.blit(label, (rect.left + pad, y))
    y += label.get_height() + 4

    name_surf = fonts["huge"].render(p.name, True, p.color)
    surface.blit(name_surf, (rect.left + pad, y))
    y += name_surf.get_height() + int(pad * 0.4)

    if game.teams_mode:
        team_txt = fonts["small"].render(f"Команда {p.team + 1}", True, C.TEXT_DIM)
        surface.blit(team_txt, (rect.left + pad, y))
        y += team_txt.get_height() + 8

    # общий счёт крупно
    score_label = fonts["small"].render("ОБЩИЙ СЧЁТ", True, C.TEXT_DIM)
    surface.blit(score_label, (rect.left + pad, y))
    y += score_label.get_height() + 2
    score_surf = fonts["score"].render(str(p.total_score), True, C.TEXT_MAIN)
    surface.blit(score_surf, (rect.left + pad, y))
    y += score_surf.get_height() + int(pad * 0.5)

    # индикатор дротиков (кружки)
    thrown, total = game.darts_thrown_progress()
    dot_r = max(10, int(rect.height * 0.022))
    dot_gap = dot_r * 3
    dx = rect.left + pad + dot_r
    dart_label = fonts["small"].render(
        f"ДРОТИКИ: осталось {p.darts_remaining} из {total}", True, C.TEXT_DIM)
    surface.blit(dart_label, (rect.left + pad, y))
    y += dart_label.get_height() + 10
    for i in range(total):
        filled = i < thrown
        cx = dx + i * dot_gap
        cy = y + dot_r
        if filled:
            pygame.draw.circle(surface, C.TEXT_DIM2, (cx, cy), dot_r)
        else:
            pygame.draw.circle(surface, p.color, (cx, cy), dot_r)
            pygame.draw.circle(surface, C.TEXT_MAIN, (cx, cy), dot_r, 2)
    y += dot_r * 2 + int(pad * 0.6)

    # активные бонусы хода (если есть от улучшений)
    tags = []
    if p.turn_multiplier > 1.001:
        tags.append(f"×{p.turn_multiplier:.2g} очки")
    if p.miss_floor > p.perm_miss_floor:
        tags.append(f"промах = {p.miss_floor}")
    if tags:
        tag_label = emoji_render.rtext(fonts["small"], "🔥 В ЭТОМ ХОДЕ: " + ", ".join(tags), C.ACCENT)
        surface.blit(tag_label, (rect.left + pad, y))
        y += tag_label.get_height() + 6

    # постоянные (пассивные) бонусы — действуют до конца партии
    perm_tags = []
    if p.perm_multiplier > 1.001:
        perm_tags.append(f"×{p.perm_multiplier:.2g} очки")
    if p.perm_extra_darts:
        perm_tags.append(f"+{p.perm_extra_darts} дротик/ход")
    if p.perm_flat_per_turn:
        perm_tags.append(f"+{p.perm_flat_per_turn} очков/ход")
    if p.perm_miss_floor:
        perm_tags.append(f"промах ≥ {p.perm_miss_floor}")
    if p.perm_shield:
        perm_tags.append(f"щит {int(p.perm_shield * 100)}%")
    if perm_tags:
        perm_label = emoji_render.rtext(fonts["small"], "♾️ НАВСЕГДА: " + ", ".join(perm_tags), C.ACCENT_2)
        surface.blit(perm_label, (rect.left + pad, y))
        y += perm_label.get_height() + 8

    # очки за текущий раунд/ход
    round_label = fonts["medium"].render(f"Очки за этот ход: {p.current_round_points}",
                                          True, C.ACCENT_2)
    surface.blit(round_label, (rect.left + pad, rect.bottom - round_label.get_height() - pad))

    # номер раунда справа сверху панели
    round_txt = fonts["medium"].render(f"Раунд {game.round_no}/{game.rounds_total}", True, C.TEXT_MAIN)
    surface.blit(round_txt, round_txt.get_rect(topright=(rect.right - pad, rect.top + pad)))

    mode_txt = fonts["small"].render(game.info["title"], True, C.TEXT_DIM)
    surface.blit(mode_txt, mode_txt.get_rect(topright=(rect.right - pad, rect.top + pad + round_txt.get_height() + 2)))


# ==========================================================================
# ТАБЛИЦА СЧЁТА
# ==========================================================================
def draw_scoreboard(surface, rect, game, fonts):
    draw_panel(surface, rect)
    pad = int(rect.height * 0.035)
    title = emoji_render.rtext(fonts["medium"], "📋 ТАБЛИЦА СЧЁТА", C.TEXT_MAIN)
    surface.blit(title, (rect.left + pad, rect.top + pad))

    top = rect.top + pad + title.get_height() + 10
    row_h = max(38, int((rect.height - (top - rect.top) - pad) / max(len(game.players), 1)))
    row_h = min(row_h, int(rect.height * 0.16))

    if game.teams_mode:
        _draw_team_scoreboard(surface, rect, top, row_h, game, fonts)
    else:
        _draw_player_scoreboard(surface, rect, top, row_h, game, fonts)


def _draw_player_scoreboard(surface, rect, top, row_h, game, fonts):
    pad = int(rect.height * 0.035)
    ranked = game.players_sorted()
    y = top
    for p in ranked:
        row_rect = pygame.Rect(rect.left + pad // 2, y, rect.width - pad, row_h - 6)
        is_current = p is game.current_player
        bg = C.PANEL_BG_LIGHT if is_current else None
        if bg:
            pygame.draw.rect(surface, bg, row_rect, border_radius=10)
        if is_current:
            pygame.draw.rect(surface, p.color, row_rect, 2, border_radius=10)

        pygame.draw.circle(surface, p.color, (row_rect.left + 18, row_rect.centery), 8)
        name_surf = fonts["medium"].render(p.name, True, C.TEXT_MAIN)
        surface.blit(name_surf, (row_rect.left + 36, row_rect.centery - name_surf.get_height() // 2))

        score_surf = fonts["medium_bold"].render(str(p.total_score), True, C.TEXT_MAIN)
        surface.blit(score_surf, score_surf.get_rect(midright=(row_rect.right - 12, row_rect.centery)))
        y += row_h


def _draw_team_scoreboard(surface, rect, top, row_h, game, fonts):
    pad = int(rect.height * 0.035)
    totals = game.team_totals()
    teams_sorted = sorted(totals.keys(), key=lambda t: totals[t], reverse=True)
    y = top
    for t in teams_sorted:
        header_rect = pygame.Rect(rect.left + pad // 2, y, rect.width - pad, row_h - 4)
        color = C.TEAM_COLORS[t % len(C.TEAM_COLORS)]
        pygame.draw.rect(surface, C.PANEL_BG_LIGHT, header_rect, border_radius=10)
        pygame.draw.rect(surface, color, header_rect, 2, border_radius=10)
        name_surf = emoji_render.rtext(fonts["medium_bold"], f"🛡️ Команда {t + 1}", color)
        surface.blit(name_surf, (header_rect.left + 14, header_rect.centery - name_surf.get_height() // 2))
        score_surf = fonts["medium_bold"].render(str(totals[t]), True, C.TEXT_MAIN)
        surface.blit(score_surf, score_surf.get_rect(midright=(header_rect.right - 12, header_rect.centery)))
        y += row_h - 4

        for p in game.players:
            if p.team != t:
                continue
            sub_h = int(row_h * 0.62)
            sub_rect = pygame.Rect(rect.left + pad // 2 + 20, y, rect.width - pad - 20, sub_h - 4)
            is_current = p is game.current_player
            if is_current:
                pygame.draw.rect(surface, C.PANEL_BG_LIGHT, sub_rect, 2, border_radius=8)
            small_name = fonts["small"].render(p.name, True, C.TEXT_DIM)
            surface.blit(small_name, (sub_rect.left + 6, sub_rect.centery - small_name.get_height() // 2))
            small_score = fonts["small"].render(str(p.total_score), True, C.TEXT_DIM)
            surface.blit(small_score, small_score.get_rect(midright=(sub_rect.right - 6, sub_rect.centery)))
            y += sub_h
        y += 6
```

upgrades.py:
```
# -*- coding: utf-8 -*-
"""
upgrades.py — режим "С улучшениями": определения бонусов и анимация
слот-машины (прокрутка), которая "выпадает" каждому игроку в начале хода.

Улучшения делятся по двум осям:
  • tier (1/2/3)       — сила эффекта. Чем дальше раунд, тем чаще выпадают
                          старшие уровни ("чем дальше в лейт-гейм, тем круче").
  • duration           — "turn" (действует только в этом ходе) или
                          "permanent" (пассивный эффект до конца всей партии,
                          складывается с другими постоянными бонусами).

Постоянные эффекты хранятся в самом Player (perm_*) и применяются
автоматически в начале каждого хода в game.py — здесь только их выдача.
"""

import random
import pygame
import config as C
import emoji_render


class Upgrade:
    def __init__(self, key, name, desc, tier, duration, color, apply_fn):
        self.key = key
        self.name = name
        self.desc = desc
        self.tier = tier                # 1, 2, 3
        self.duration = duration        # "turn" | "permanent"
        self.color = color
        self.apply_fn = apply_fn        # apply_fn(game, player)

    def apply(self, game, player):
        self.apply_fn(game, player)


# ==========================================================================
# ЭФФЕКТЫ "НА ЭТОТ ХОД"
# ==========================================================================
def _fx_extra_dart(n):
    def fn(game, player):
        player.extra_darts_bonus += n
        player.darts_remaining += n
    return fn


def _fx_multiplier(mult):
    def fn(game, player):
        player.turn_multiplier *= mult
    return fn


def _fx_flat_bonus(n):
    def fn(game, player):
        player.total_score += n
        player.current_round_points += n
        game.floating_texts.append((f"+{n}", player))
    return fn


def _fx_steal_from_leader(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        leader = max(others, key=lambda p: p.total_score)
        effective = max(0, int(round(n * (1 - leader.perm_shield))))
        steal = min(effective, leader.total_score)
        leader.total_score -= steal
        player.total_score += steal
        player.current_round_points += steal
        game.floating_texts.append((f"-{steal}", leader))
        game.floating_texts.append((f"+{steal}", player))
    return fn


def _fx_weaken_leader(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        leader = max(others, key=lambda p: p.total_score)
        effective = max(0, int(round(n * (1 - leader.perm_shield))))
        loss = min(effective, leader.total_score)
        leader.total_score -= loss
        game.floating_texts.append((f"-{loss}", leader))
    return fn


def _fx_weaken_random_opponent(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player and p.team != player.team]
        if not others:
            others = [p for p in game.players if p is not player]
        if not others:
            return
        target = random.choice(others)
        effective = max(0, int(round(n * (1 - target.perm_shield))))
        loss = min(effective, target.total_score)
        target.total_score -= loss
        game.floating_texts.append((f"-{loss}", target))
    return fn


def _fx_miss_becomes(n):
    def fn(game, player):
        player.miss_floor = max(player.miss_floor, n)
    return fn


def _fx_sabotage_dart(n):
    """Случайный соперник получит на n дротиков меньше в свой следующий ход."""
    def fn(game, player):
        others = [p for p in game.players if p is not player and p.team != player.team]
        if not others:
            others = [p for p in game.players if p is not player]
        if not others:
            return
        target = random.choice(others)
        effective = max(0, int(round(n * (1 - target.perm_shield))))
        if effective <= 0:
            game.floating_texts.append(("ЩИТ!", target))
            return
        target.pending_dart_penalty += effective
        game.floating_texts.append((f"-{effective} дрот.", target))
    return fn


def _fx_double_darts_this_turn():
    def fn(game, player):
        extra = player.darts_remaining + player.extra_darts_bonus
        player.extra_darts_bonus += extra
        player.darts_remaining += extra
    return fn


def _fx_copy_best_round():
    """Мгновенно добавить очки, равные твоему же лучшему раунду за партию."""
    def fn(game, player):
        bonus = max(player.best_round, 15)
        player.total_score += bonus
        player.current_round_points += bonus
        game.floating_texts.append((f"+{bonus}", player))
    return fn


# ==========================================================================
# ЭФФЕКТЫ "НАВСЕГДА" (до конца партии) — пассивно применяются в game.py
# ==========================================================================
def _fx_perm_multiplier(factor):
    def fn(game, player):
        player.perm_multiplier *= factor
    return fn


def _fx_perm_flat_income(n):
    def fn(game, player):
        player.perm_flat_per_turn += n
    return fn


def _fx_perm_miss_floor(n):
    def fn(game, player):
        player.perm_miss_floor = max(player.perm_miss_floor, n)
    return fn


def _fx_perm_extra_dart(n):
    def fn(game, player):
        player.perm_extra_darts += n
    return fn


def _fx_perm_shield(amount):
    def fn(game, player):
        player.perm_shield = min(0.9, player.perm_shield + amount)
    return fn


# ==========================================================================
# КАТАЛОГ УЛУЧШЕНИЙ (30 штук: 10 на каждый уровень, примерно половина навсегда)
# ==========================================================================
UPGRADES = [
    # ---------------------------------------------------------------
    # TIER 1 — ранняя игра, лёгкие эффекты
    # ---------------------------------------------------------------
    Upgrade("t1_extra_dart", "Доп. дротик", "Ещё +1 дротик в этом ходе", 1, "turn",
            C.SUCCESS, _fx_extra_dart(1)),
    Upgrade("t1_small_bonus", "Мелкая удача", "Сразу +10 очков", 1, "turn",
            C.ACCENT_2, _fx_flat_bonus(10)),
    Upgrade("t1_poke_leader", "Укол лидеру", "Лидер теряет 5 очков", 1, "turn",
            C.DANGER, _fx_weaken_leader(5)),
    Upgrade("t1_safety_net", "Страховка", "Промахи в этом ходе = 5 очков", 1, "turn",
            (120, 170, 255), _fx_miss_becomes(5)),
    Upgrade("t1_pickpocket", "Мелкий саботаж", "Случайный соперник получит на 1 дротик меньше в свой ход", 1, "turn",
            C.DANGER, _fx_sabotage_dart(1)),
    Upgrade("t1_echo", "Эхо удачи", "Сразу получи очки, равные твоему лучшему раунду (мин. 15)", 1, "turn",
            C.ACCENT_2, _fx_copy_best_round()),

    Upgrade("t1_steady_hand", "Твёрдая рука", "НАВСЕГДА: промахи = минимум 3 очка", 1, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(3)),
    Upgrade("t1_warmup", "Разминка", "НАВСЕГДА: +2 очка в начале каждого хода", 1, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(2)),
    Upgrade("t1_focus", "Концентрация", "НАВСЕГДА: очки +5% до конца партии", 1, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.05)),
    Upgrade("t1_thick_skin", "Толстая кожа", "НАВСЕГДА: -20% урона от краж и атак соперников", 1, "permanent",
            (150, 200, 255), _fx_perm_shield(0.20)),

    # ---------------------------------------------------------------
    # TIER 2 — середина игры, эффекты ощутимее
    # ---------------------------------------------------------------
    Upgrade("t2_double_turn", "Двойной удар", "Все очки этого хода x2", 2, "turn",
            C.ACCENT, _fx_multiplier(2)),
    Upgrade("t2_steal", "Кража", "Забрать 10 очков у лидера", 2, "turn",
            C.DANGER, _fx_steal_from_leader(10)),
    Upgrade("t2_extra_dart2", "Второе дыхание", "Ещё +2 дротика в этом ходе", 2, "turn",
            C.SUCCESS, _fx_extra_dart(2)),
    Upgrade("t2_mid_bonus", "Джекпот-мини", "Сразу +25 очков", 2, "turn",
            C.ACCENT_2, _fx_flat_bonus(25)),
    Upgrade("t2_sabotage2", "Крупный саботаж", "Случайный соперник получит на 2 дротика меньше в свой ход", 2, "turn",
            C.DANGER, _fx_sabotage_dart(2)),
    Upgrade("t2_double_darts", "Удвоение бросков", "Удвоить количество дротиков, оставшихся в этом ходе", 2, "turn",
            C.SUCCESS, _fx_double_darts_this_turn()),

    Upgrade("t2_nerves", "Стальные нервы", "НАВСЕГДА: промахи = минимум 8 очков", 2, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(8)),
    Upgrade("t2_mindset", "Постоянный настрой", "НАВСЕГДА: очки +12% до конца партии", 2, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.12)),
    Upgrade("t2_coach", "Личный тренер", "НАВСЕГДА: +5 очков в начале каждого хода", 2, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(5)),
    Upgrade("t2_shield", "Щит", "НАВСЕГДА: -50% урона от краж и атак соперников", 2, "permanent",
            (150, 200, 255), _fx_perm_shield(0.30)),

    # ---------------------------------------------------------------
    # TIER 3 — лейт-гейм, самые мощные
    # ---------------------------------------------------------------
    Upgrade("t3_triple_turn", "Тройной удар", "Все очки этого хода x3!", 3, "turn",
            C.ACCENT, _fx_multiplier(3)),
    Upgrade("t3_jackpot", "ДЖЕКПОТ", "Сразу +40 очков!", 3, "turn",
            C.ACCENT_2, _fx_flat_bonus(40)),
    Upgrade("t3_crush_leader", "Разгром лидера", "Лидер теряет 20 очков", 3, "turn",
            C.DANGER, _fx_weaken_leader(20)),
    Upgrade("t3_big_steal", "Большая кража", "Забрать 25 очков у лидера", 3, "turn",
            C.DANGER, _fx_steal_from_leader(25)),
    Upgrade("t3_wreck", "Разгром рандома", "Случайный соперник теряет 15 очков", 3, "turn",
            C.DANGER, _fx_weaken_random_opponent(15)),
    Upgrade("t3_double_darts2", "Двойная перезарядка", "Удвоить оставшиеся дротики в этом ходе", 3, "turn",
            C.SUCCESS, _fx_double_darts_this_turn()),

    Upgrade("t3_legend", "Легенда дартса", "НАВСЕГДА: очки +25% до конца партии", 3, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.25)),
    Upgrade("t3_lifetime_income", "Пожизненный доход", "НАВСЕГДА: +10 очков в начале каждого хода", 3, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(10)),
    Upgrade("t3_sniper_perm", "Снайпер", "НАВСЕГДА: промахи = минимум 15 очков", 3, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(15)),
    Upgrade("t3_extra_hand", "Третья рука", "НАВСЕГДА: +1 дротик каждый ход до конца партии", 3, "permanent",
            C.SUCCESS, _fx_perm_extra_dart(1)),
]

UPGRADES_BY_TIER = {1: [u for u in UPGRADES if u.tier == 1],
                     2: [u for u in UPGRADES if u.tier == 2],
                     3: [u for u in UPGRADES if u.tier == 3]}

TIER_EMOJI = {1: "🌱", 2: "⚡", 3: "💎"}
DURATION_LABEL = {"turn": "⏳ ЭТОТ ХОД", "permanent": "♾️ НАВСЕГДА"}
DURATION_COLOR = {"turn": C.TEXT_DIM, "permanent": C.ACCENT}


def roll_upgrade(round_no, total_rounds):
    """
    Возвращает случайное улучшение. Веса тиров смещаются в сторону
    старших уровней по мере роста номера раунда.
    """
    progress = 0.0 if total_rounds <= 1 else (round_no - 1) / (total_rounds - 1)
    # веса [tier1, tier2, tier3] линейно смещаются от (70,25,5) к (10,35,55)
    w1 = 70 - 60 * progress
    w2 = 25 + 10 * progress
    w3 = 5 + 50 * progress
    tier = random.choices([1, 2, 3], weights=[w1, w2, w3], k=1)[0]
    return random.choice(UPGRADES_BY_TIER[tier])


class UpgradeSpinner:
    """
    Анимация слот-машины: быстрая прокрутка карточек улучшений,
    плавное замедление и остановка на выбранном улучшении.
    """

    DURATION_MS = 2200
    CARD_H = 106
    CARD_GAP = 14

    def __init__(self, result_upgrade: Upgrade, on_done=None):
        self.result = result_upgrade
        self.on_done = on_done
        self.start_ticks = pygame.time.get_ticks()
        self.done = False
        # лента карточек: случайные + результат в конце
        reel = [random.choice(UPGRADES) for _ in range(22)]
        reel.append(result_upgrade)
        self.reel = reel
        self.finished_hold = 0

    def update(self):
        if self.done:
            self.finished_hold += 1

    def progress(self):
        elapsed = pygame.time.get_ticks() - self.start_ticks
        t = min(1.0, elapsed / self.DURATION_MS)
        if t >= 1.0 and not self.done:
            self.done = True
            if self.on_done:
                self.on_done(self.result)
        return t

    @staticmethod
    def _ease_out_cubic(t):
        return 1 - (1 - t) ** 3

    def draw(self, surface, center_rect: pygame.Rect, font_title, font_desc, font_tag):
        t = self.progress()
        eased = self._ease_out_cubic(t)

        n = len(self.reel)
        total_h = n * (self.CARD_H + self.CARD_GAP)
        # финальное смещение — чтобы последняя карточка (result) была по центру окна
        final_offset = total_h - (self.CARD_H + self.CARD_GAP) * 0.5 - center_rect.height / 2
        offset = eased * final_offset

        clip = surface.get_clip()
        surface.set_clip(center_rect)

        # фон панели
        pygame.draw.rect(surface, C.PANEL_BG, center_rect, border_radius=18)
        pygame.draw.rect(surface, C.ACCENT, center_rect, 3, border_radius=18)

        y = center_rect.top - offset
        for card in self.reel:
            card_rect = pygame.Rect(center_rect.left + 16, int(y),
                                     center_rect.width - 32, self.CARD_H)
            if card_rect.bottom > center_rect.top - 20 and card_rect.top < center_rect.bottom + 20:
                self._draw_card(surface, card_rect, card, font_title, font_desc, font_tag)
            y += self.CARD_H + self.CARD_GAP

        # затемняющая рамка сверху/снизу для эффекта "окна"
        fade_h = 60
        top_fade = pygame.Surface((center_rect.width, fade_h), pygame.SRCALPHA)
        top_fade.fill((*C.PANEL_BG, 235))
        surface.blit(top_fade, (center_rect.left, center_rect.top))
        bottom_fade = pygame.Surface((center_rect.width, fade_h), pygame.SRCALPHA)
        bottom_fade.fill((*C.PANEL_BG, 235))
        surface.blit(bottom_fade, (center_rect.left, center_rect.bottom - fade_h))

        # индикатор-указатель по центру
        mid_y = center_rect.centery
        pygame.draw.polygon(surface, C.ACCENT, [
            (center_rect.left - 4, mid_y - 14),
            (center_rect.left - 4, mid_y + 14),
            (center_rect.left + 14, mid_y),
        ])
        pygame.draw.polygon(surface, C.ACCENT, [
            (center_rect.right + 4, mid_y - 14),
            (center_rect.right + 4, mid_y + 14),
            (center_rect.right - 14, mid_y),
        ])

        surface.set_clip(clip)

    def _draw_card(self, surface, rect, card: Upgrade, font_title, font_desc, font_tag):
        pygame.draw.rect(surface, C.PANEL_BG_LIGHT, rect, border_radius=12)
        pygame.draw.rect(surface, card.color, rect, 3, border_radius=12)
        tier_tag = emoji_render.rtext(font_tag, f"{TIER_EMOJI.get(card.tier, '')} УРОВЕНЬ {card.tier}", card.color)
        surface.blit(tier_tag, (rect.left + 16, rect.top + 8))
        dur_label = DURATION_LABEL.get(card.duration, "")
        dur_color = DURATION_COLOR.get(card.duration, C.TEXT_DIM)
        dur_tag = emoji_render.rtext(font_tag, dur_label, dur_color)
        surface.blit(dur_tag, dur_tag.get_rect(topright=(rect.right - 14, rect.top + 8)))
        title = emoji_render.rtext(font_title, card.name, C.TEXT_MAIN)
        surface.blit(title, (rect.left + 16, rect.top + 32))
        desc = font_desc.render(card.desc, True, C.TEXT_DIM)
        surface.blit(desc, (rect.left + 16, rect.top + 66))
```

darts_stats.json:
```
{
  "players": {
    "Даша": {
      "games": 1,
      "wins": 1,
      "total_points": 418,
      "total_throws": 24,
      "best_round_ever": 107,
      "best_single_ever": 57,
      "bulls": 1,
      "triples": 6,
      "doubles": 5
    },
    "Дима": {
      "games": 1,
      "wins": 0,
      "total_points": 372,
      "total_throws": 24,
      "best_round_ever": 92,
      "best_single_ever": 57,
      "bulls": 0,
      "triples": 2,
      "doubles": 0
    },
    "дима": {
      "games": 2,
      "wins": 0,
      "total_points": 591,
      "total_throws": 41,
      "best_round_ever": 104,
      "best_single_ever": 28,
      "bulls": 0,
      "triples": 0,
      "doubles": 1
    },
    "радуга": {
      "games": 1,
      "wins": 1,
      "total_points": 324,
      "total_throws": 21,
      "best_round_ever": 82,
      "best_single_ever": 48,
      "bulls": 0,
      "triples": 2,
      "doubles": 1
    },
    "димас ботярас": {
      "games": 2,
      "wins": 1,
      "total_points": 487,
      "total_throws": 36,
      "best_round_ever": 76,
      "best_single_ever": 51,
      "bulls": 0,
      "triples": 5,
      "doubles": 2
    },
    "Girl Dasha": {
      "games": 1,
      "wins": 1,
      "total_points": 130,
      "total_throws": 12,
      "best_round_ever": 55,
      "best_single_ever": 38,
      "bulls": 0,
      "triples": 0,
      "doubles": 1
    },
    "Дашенька": {
      "games": 1,
      "wins": 0,
      "total_points": 345,
      "total_throws": 24,
      "best_round_ever": 99,
      "best_single_ever": 60,
      "bulls": 0,
      "triples": 2,
      "doubles": 3
    },
    "Дашуля": {
      "games": 1,
      "wins": 1,
      "total_points": 318,
      "total_throws": 25,
      "best_round_ever": 80,
      "best_single_ever": 25,
      "bulls": 0,
      "triples": 0,
      "doubles": 3
    }
  },
  "games_played": 5
}```

all_scripts.md:
```
```

README.md:
```
# 🎯 Дартс — Домашний счёт

Полноценное pygame-приложение для подсчёта очков в дартс с большим,
"телевизорным" интерфейсом: подключаешь ноутбук к ТВ, разворачиваешь
на весь экран (`F11`) — и играешь всей компанией, кликая мышкой по
мишени вместо ввода очков с клавиатуры.

## Установка и запуск

```bash
pip install -r requirements.txt
python3 main.py
```

Python 3.9+ и `pygame >= 2.1`. Pillow нужен для цветных эмодзи в интерфейсе
(см. раздел «Эмодзи» ниже) — без него игра тоже прекрасно работает, просто
эмодзи в текстах будут аккуратно убраны, а не показаны квадратиками.

## Управление

- **Клик мышкой по мишени** — бросок дротика (учитывается зона: одиночный
  сектор, тройное кольцо (T), двойное кольцо (D), бул 25 и яблочко 50).
- **F11** — полноэкранный режим (для проекции на ТВ).
- **Esc** — выйти из полноэкранного режима / выйти из игры в главном меню.
- Кнопки на экране: **Новая игра**, **Отменить** (undo — работает даже
  после нескольких бросков подряд), **Пропустить** ход.

## Режимы игры

| Режим | Правила |
|---|---|
| **Обычный** | 2–8 игроков, 3 дротика за ход, 8 раундов. Побеждает набравший больше очков. |
| **Дуэль** | Ровно 2 игрока, та же схема, но один на один. |
| **Команды** | Две команды (2–8 игроков), ходят по очереди вперемешку, очки команды суммируются. |
| **Спринт 6×6** | 6 раундов с нарастающей сложностью: раунды 1–2 — по 1 дротику за ход, 3–4 — по 2 дротика сразу, 5–6 — по 3 сразу. |
| **С улучшениями** | 7 раундов. Перед каждым ходом — анимация слот-машины со случайным улучшением. Бывают **разовые** (действуют только этот ход: доп. дротики, x2/x3 очки, кража очков, саботаж соперника) и **постоянные** (действуют до конца всей партии: пассивный множитель очков, дротик каждый ход навсегда, пассивный доход очков в начале хода, щит от чужих атак и т.д.). Всего 30 разных улучшений (10 на каждый из 3 уровней), чем дальше раунд — тем чаще выпадают мощные. |

Правила — «домашние», без официальных дротичных сложностей (double-out,
checkout и т.п.): просто набираете очки и веселитесь.

## Статистика

После каждой партии результаты сохраняются в `darts_stats.json` рядом
со скриптом. На главном экране есть кнопка **📊 Статистика игроков** —
таблица лидеров по среднему очков за дротик, проценту побед, лучшему
ходу и лучшему одиночному броску.

## Эмодзи 🎯🔥

## Визуальные эффекты 🎆

При каждом попадании — взрыв частиц и пульсирующее кольцо в точке удара,
цвет зависит от зоны (бул — красно-золотой, трипл — золотой, дабл —
бирюзовый). На буллсай и трипл добавляется короткая вспышка экрана и
всплывающий текст-коллаут ("БУЛ! 50", "TRIPLE 20!") с эффектом "попа"
(быстро увеличивается и оседает). Если сумма очков за ход большая —
выскакивает "🔥 МАКСИМАЛКА!" (от 150) или "⚡ ОГОНЬ!" (от 100), как
183/180 в настоящем дартсе. На кнопках — лёгкая рябь при клике для
тактильного отклика, у панели текущего игрока — мягкое пульсирующее
свечение его цветом. На экране победы — конфетти цветов победителя.

Все эффекты — в отдельном модуле `fx.py`, ничего не завязано на логику
игры, поэтому их легко подкрутить (сила частиц, длительность, пороги
коллаутов) не трогая остальной код.


Сам pygame не умеет рисовать цветные эмодзи — по умолчанию получаются
чёрно-белые "тофу"-квадратики. Поэтому в проекте есть `emoji_render.py`:
он рендерит эмодзи через Pillow (используя системный цветной шрифт —
например `NotoColorEmoji.ttf` на Linux/Android или `Apple Color Emoji`
на macOS, `Segoe UI Emoji` на Windows) и подставляет их как цветные
картинки прямо внутрь текста, вперемешку с обычными буквами.

Если подходящий эмодзи-шрифт на компьютере не найден — модуль тихо
переключается в безопасный режим и просто убирает эмодзи из текста,
чтобы вместо них не было уродливых квадратиков. Игра при этом не падает
и не требует специальной настройки — обнаружение полностью автоматическое.

## Структура проекта

```
main.py            — точка входа, экраны (меню/настройка/игра/итоги), игровой цикл
config.py           — все константы: цвета, размеры, правила режимов
dartboard.py         — отрисовка мишени + определение результата клика
player.py            — модель игрока и статистика партии
game.py              — очередность ходов, начисление очков, undo, режимы, победитель
upgrades.py           — улучшения и анимация слот-машины (режим "С улучшениями")
fx.py                  — визуальные эффекты: частицы, вспышки, коллауты, конфетти, рябь
emoji_render.py         — цветной рендер эмодзи через Pillow (с безопасным фоллбеком)
ui.py                 — кнопки, текстовые поля, панели, таблица счёта
stats_storage.py       — персистентная статистика между запусками (JSON)
```

## Настройка под свой экран

В `config.py`:
- `DEFAULT_WIDTH` / `DEFAULT_HEIGHT` — стартовое разрешение окна.
- `BOARD_PANEL_RATIO` — доля экрана под мишень (по умолчанию 1/3 слева).
- `MODE_INFO[...]["rounds"]` — количество раундов в любом режиме.
- Цветовая палитра — блок `# ЦВЕТА` в начале файла.

Приятной игры! 🔥🎯
```

