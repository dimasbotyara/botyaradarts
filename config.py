# -*- coding: utf-8 -*-
"""
config.py — константы, темы оформления и настройки игры.
"""

import os
import json

# ----------------------------------------------------------------------
# ЭКРАН
# ----------------------------------------------------------------------
DEFAULT_WIDTH = 1600
DEFAULT_HEIGHT = 900
MIN_WIDTH = 1100
MIN_HEIGHT = 650
FPS = 60
WINDOW_TITLE = "Дартс — Домашний счёт"

BOARD_PANEL_RATIO = 0.42

# ----------------------------------------------------------------------
# ЦВЕТА (базовые)
# ----------------------------------------------------------------------
BG_TOP = (18, 20, 28)
BG_BOTTOM = (10, 11, 16)
PANEL_BG = (26, 29, 39)
PANEL_BG_LIGHT = (34, 38, 50)
PANEL_BORDER = (58, 64, 82)

ACCENT = (255, 196, 0)
ACCENT_2 = (0, 200, 180)
DANGER = (235, 70, 70)
SUCCESS = (80, 210, 120)

TEXT_MAIN = (240, 242, 248)
TEXT_DIM = (150, 156, 172)
TEXT_DIM2 = (105, 110, 128)

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

# Поворот мишени: "6_top" или "20_top"
BOARD_ROTATION = "6_top"   # по умолчанию как у тебя

# ----------------------------------------------------------------------
# ТЕМЫ ИНТЕРФЕЙСА
# ----------------------------------------------------------------------
UI_THEMES = {
    "custom_ui": {
        "name": "Кастомная (твоя)",
        "bg_top": (18, 20, 28),
        "bg_bottom": (10, 11, 16),
        "panel_bg": (26, 29, 39),
        "panel_bg_light": (34, 38, 50),
        "panel_border": (58, 64, 82),
        "accent": (255, 196, 0),
        "accent_2": (0, 200, 180),
        "danger": (235, 70, 70),
        "success": (80, 210, 120),
        "text_main": (240, 242, 248),
        "text_dim": (150, 156, 172),
        "text_dim2": (105, 110, 128),
        "button_bg": (44, 49, 64),
        "button_bg_hover": (62, 68, 88),
        "button_bg_active": (255, 196, 0),
        "button_text": (240, 242, 248),
        "button_text_active": (20, 20, 24),
    },
    "dark": {
        "name": "Тёмная классика",
        "bg_top": (30, 30, 30),
        "bg_bottom": (10, 10, 10),
        "panel_bg": (40, 40, 40),
        "panel_bg_light": (50, 50, 50),
        "panel_border": (80, 80, 80),
        "accent": (0, 120, 215),
        "accent_2": (0, 180, 150),
        "danger": (200, 50, 50),
        "success": (50, 200, 100),
        "text_main": (230, 230, 230),
        "text_dim": (170, 170, 170),
        "text_dim2": (120, 120, 120),
        "button_bg": (50, 50, 50),
        "button_bg_hover": (70, 70, 70),
        "button_bg_active": (0, 120, 215),
        "button_text": (230, 230, 230),
        "button_text_active": (255, 255, 255),
    },
    "light": {
        "name": "Светлая",
        "bg_top": (245, 245, 245),
        "bg_bottom": (220, 220, 220),
        "panel_bg": (255, 255, 255),
        "panel_bg_light": (240, 240, 240),
        "panel_border": (180, 180, 180),
        "accent": (0, 120, 215),
        "accent_2": (0, 150, 130),
        "danger": (220, 50, 50),
        "success": (50, 170, 80),
        "text_main": (30, 30, 30),
        "text_dim": (100, 100, 100),
        "text_dim2": (150, 150, 150),
        "button_bg": (230, 230, 230),
        "button_bg_hover": (210, 210, 210),
        "button_bg_active": (0, 120, 215),
        "button_text": (30, 30, 30),
        "button_text_active": (255, 255, 255),
    },
    "catppuccin_mocha": {
        "name": "Catppuccin Mocha",
        "bg_top": (30, 30, 46),
        "bg_bottom": (24, 24, 37),
        "panel_bg": (49, 50, 68),
        "panel_bg_light": (69, 71, 90),
        "panel_border": (108, 112, 134),
        "accent": (245, 194, 231),
        "accent_2": (148, 226, 213),
        "danger": (242, 143, 173),
        "success": (166, 227, 161),
        "text_main": (205, 214, 244),
        "text_dim": (166, 173, 200),
        "text_dim2": (127, 132, 156),
        "button_bg": (69, 71, 90),
        "button_bg_hover": (88, 91, 112),
        "button_bg_active": (245, 194, 231),
        "button_text": (205, 214, 244),
        "button_text_active": (30, 30, 46),
    },
    "catppuccin_latte": {
        "name": "Catppuccin Latte",
        "bg_top": (239, 241, 245),
        "bg_bottom": (220, 224, 232),
        "panel_bg": (255, 255, 255),
        "panel_bg_light": (230, 233, 239),
        "panel_border": (204, 208, 218),
        "accent": (114, 135, 253),
        "accent_2": (23, 146, 153),
        "danger": (210, 15, 57),
        "success": (64, 160, 43),
        "text_main": (76, 79, 105),
        "text_dim": (108, 111, 133),
        "text_dim2": (140, 143, 161),
        "button_bg": (230, 233, 239),
        "button_bg_hover": (204, 208, 218),
        "button_bg_active": (114, 135, 253),
        "button_text": (76, 79, 105),
        "button_text_active": (255, 255, 255),
    },
    "dracula": {
        "name": "Dracula",
        "bg_top": (40, 42, 54),
        "bg_bottom": (28, 30, 40),
        "panel_bg": (40, 42, 54),
        "panel_bg_light": (68, 71, 90),
        "panel_border": (98, 114, 164),
        "accent": (189, 147, 249),
        "accent_2": (80, 250, 123),
        "danger": (255, 85, 85),
        "success": (80, 250, 123),
        "text_main": (248, 248, 242),
        "text_dim": (191, 191, 191),
        "text_dim2": (139, 143, 167),
        "button_bg": (68, 71, 90),
        "button_bg_hover": (98, 114, 164),
        "button_bg_active": (189, 147, 249),
        "button_text": (248, 248, 242),
        "button_text_active": (40, 42, 54),
    },
    "nord": {
        "name": "Nord",
        "bg_top": (46, 52, 64),
        "bg_bottom": (59, 66, 82),
        "panel_bg": (76, 86, 106),
        "panel_bg_light": (94, 105, 126),
        "panel_border": (136, 192, 208),
        "accent": (136, 192, 208),
        "accent_2": (163, 190, 140),
        "danger": (191, 97, 106),
        "success": (163, 190, 140),
        "text_main": (236, 239, 244),
        "text_dim": (216, 222, 233),
        "text_dim2": (180, 186, 197),
        "button_bg": (94, 105, 126),
        "button_bg_hover": (121, 132, 156),
        "button_bg_active": (136, 192, 208),
        "button_text": (236, 239, 244),
        "button_text_active": (46, 52, 64),
    },
    "gruvbox_dark": {
        "name": "Gruvbox Dark",
        "bg_top": (40, 40, 40),
        "bg_bottom": (29, 32, 33),
        "panel_bg": (50, 48, 47),
        "panel_bg_light": (60, 56, 54),
        "panel_border": (124, 111, 100),
        "accent": (215, 153, 33),
        "accent_2": (131, 165, 152),
        "danger": (251, 73, 52),
        "success": (184, 187, 38),
        "text_main": (235, 219, 178),
        "text_dim": (189, 174, 147),
        "text_dim2": (146, 131, 116),
        "button_bg": (60, 56, 54),
        "button_bg_hover": (80, 73, 69),
        "button_bg_active": (215, 153, 33),
        "button_text": (235, 219, 178),
        "button_text_active": (40, 40, 40),
    },
    "solarized_dark": {
        "name": "Solarized Dark",
        "bg_top": (0, 43, 54),
        "bg_bottom": (7, 54, 66),
        "panel_bg": (7, 54, 66),
        "panel_bg_light": (88, 110, 117),
        "panel_border": (131, 148, 150),
        "accent": (181, 137, 0),
        "accent_2": (42, 161, 152),
        "danger": (220, 50, 47),
        "success": (133, 153, 0),
        "text_main": (238, 232, 213),
        "text_dim": (147, 161, 161),
        "text_dim2": (101, 123, 131),
        "button_bg": (88, 110, 117),
        "button_bg_hover": (101, 123, 131),
        "button_bg_active": (181, 137, 0),
        "button_text": (238, 232, 213),
        "button_text_active": (0, 43, 54),
    },
    "solarized_light": {
        "name": "Solarized Light",
        "bg_top": (253, 246, 227),
        "bg_bottom": (238, 232, 213),
        "panel_bg": (255, 255, 255),
        "panel_bg_light": (238, 232, 213),
        "panel_border": (147, 161, 161),
        "accent": (181, 137, 0),
        "accent_2": (42, 161, 152),
        "danger": (220, 50, 47),
        "success": (133, 153, 0),
        "text_main": (101, 123, 131),
        "text_dim": (131, 148, 150),
        "text_dim2": (147, 161, 161),
        "button_bg": (238, 232, 213),
        "button_bg_hover": (203, 196, 177),
        "button_bg_active": (181, 137, 0),
        "button_text": (101, 123, 131),
        "button_text_active": (253, 246, 227),
    },
    "one_dark": {
        "name": "One Dark",
        "bg_top": (40, 44, 52),
        "bg_bottom": (33, 37, 43),
        "panel_bg": (33, 37, 43),
        "panel_bg_light": (44, 48, 56),
        "panel_border": (92, 99, 112),
        "accent": (97, 175, 239),
        "accent_2": (152, 195, 121),
        "danger": (224, 108, 117),
        "success": (152, 195, 121),
        "text_main": (171, 178, 191),
        "text_dim": (140, 147, 160),
        "text_dim2": (92, 99, 112),
        "button_bg": (44, 48, 56),
        "button_bg_hover": (58, 63, 72),
        "button_bg_active": (97, 175, 239),
        "button_text": (171, 178, 191),
        "button_text_active": (40, 44, 52),
    },
}

# ----------------------------------------------------------------------
# ТЕМЫ МИШЕНИ
# ----------------------------------------------------------------------
BOARD_THEMES = {
    "custom_board": {
        "name": "Кастомная (твоя)",
        "board_black": (25, 25, 28),
        "board_cream": (232, 220, 196),
        "board_red": (196, 30, 45),
        "board_green": (20, 120, 70),
        "board_yellow": (255, 200, 0),
        "board_wire": (0, 0, 0),
        "board_out": (14, 15, 20),
        "board_rim": (60, 45, 30),
    },
    "classic": {
        "name": "Классическая",
        "board_black": (20, 20, 20),
        "board_cream": (240, 230, 210),
        "board_red": (220, 30, 30),
        "board_green": (20, 130, 70),
        "board_yellow": (240, 180, 0),
        "board_wire": (0, 0, 0),
        "board_out": (15, 15, 15),
        "board_rim": (80, 60, 40),
    },
    "inverted": {
        "name": "Инвертированная",
        "board_black": (240, 230, 210),
        "board_cream": (20, 20, 20),
        "board_red": (20, 130, 70),
        "board_green": (220, 30, 30),
        "board_yellow": (0, 0, 255),
        "board_wire": (0, 0, 0),
        "board_out": (240, 240, 240),
        "board_rim": (120, 100, 80),
    },
    "neon": {
        "name": "Неон",
        "board_black": (0, 0, 30),
        "board_cream": (255, 255, 255),
        "board_red": (255, 0, 255),
        "board_green": (0, 255, 255),
        "board_yellow": (255, 255, 0),
        "board_wire": (0, 0, 0),
        "board_out": (10, 10, 40),
        "board_rim": (60, 60, 120),
    },
    "wood": {
        "name": "Дерево",
        "board_black": (80, 50, 30),
        "board_cream": (220, 190, 150),
        "board_red": (180, 70, 40),
        "board_green": (80, 140, 80),
        "board_yellow": (240, 200, 100),
        "board_wire": (0, 0, 0),
        "board_out": (40, 30, 20),
        "board_rim": (120, 80, 40),
    },
}

DEFAULT_UI_THEME = "custom_ui"
DEFAULT_BOARD_THEME = "custom_board"
CURRENT_UI_THEME_NAME = DEFAULT_UI_THEME
CURRENT_BOARD_THEME_NAME = DEFAULT_BOARD_THEME

def apply_ui_theme(name):
    global CURRENT_UI_THEME_NAME
    if name not in UI_THEMES:
        name = DEFAULT_UI_THEME
    theme = UI_THEMES[name]
    CURRENT_UI_THEME_NAME = name
    globals_dict = globals()
    globals_dict["BG_TOP"] = theme["bg_top"]
    globals_dict["BG_BOTTOM"] = theme["bg_bottom"]
    globals_dict["PANEL_BG"] = theme["panel_bg"]
    globals_dict["PANEL_BG_LIGHT"] = theme["panel_bg_light"]
    globals_dict["PANEL_BORDER"] = theme["panel_border"]
    globals_dict["ACCENT"] = theme["accent"]
    globals_dict["ACCENT_2"] = theme["accent_2"]
    globals_dict["DANGER"] = theme["danger"]
    globals_dict["SUCCESS"] = theme["success"]
    globals_dict["TEXT_MAIN"] = theme["text_main"]
    globals_dict["TEXT_DIM"] = theme["text_dim"]
    globals_dict["TEXT_DIM2"] = theme["text_dim2"]
    globals_dict["BUTTON_BG"] = theme["button_bg"]
    globals_dict["BUTTON_BG_HOVER"] = theme["button_bg_hover"]
    globals_dict["BUTTON_BG_ACTIVE"] = theme["button_bg_active"]
    globals_dict["BUTTON_TEXT"] = theme["button_text"]
    globals_dict["BUTTON_TEXT_ACTIVE"] = theme["button_text_active"]

def apply_board_theme(name):
    global CURRENT_BOARD_THEME_NAME
    if name not in BOARD_THEMES:
        name = DEFAULT_BOARD_THEME
    theme = BOARD_THEMES[name]
    CURRENT_BOARD_THEME_NAME = name
    globals_dict = globals()
    globals_dict["BOARD_BLACK"] = theme["board_black"]
    globals_dict["BOARD_CREAM"] = theme["board_cream"]
    globals_dict["BOARD_RED"] = theme["board_red"]
    globals_dict["BOARD_GREEN"] = theme["board_green"]
    globals_dict["BOARD_YELLOW"] = theme["board_yellow"]
    globals_dict["BOARD_WIRE"] = theme["board_wire"]
    globals_dict["BOARD_OUT"] = theme["board_out"]
    globals_dict["BOARD_RIM"] = theme["board_rim"]

def load_settings():
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "darts_settings.json")
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            ui = data.get("ui_theme", DEFAULT_UI_THEME)
            board = data.get("board_theme", DEFAULT_BOARD_THEME)
            rotation = data.get("board_rotation", "6_top")
            return ui, board, rotation
        except Exception:
            return DEFAULT_UI_THEME, DEFAULT_BOARD_THEME, "6_top"
    return DEFAULT_UI_THEME, DEFAULT_BOARD_THEME, "6_top"

def save_settings(ui_theme, board_theme, rotation="6_top"):
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "darts_settings.json")
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump({
                "ui_theme": ui_theme,
                "board_theme": board_theme,
                "board_rotation": rotation
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ----------------------------------------------------------------------
# ШРИФТЫ
# ----------------------------------------------------------------------
FONT_NAME = None
FONT_NAME_CANDIDATES = ["dejavusans", "arial", "notosans", "freesans"]

# ----------------------------------------------------------------------
# ГЕОМЕТРИЯ МИШЕНИ
# ----------------------------------------------------------------------
R_BULL = 0.075
R_OUTER_BULL = 0.187
R_TRIPLE_IN = 0.582
R_TRIPLE_OUT = 0.629
R_DOUBLE_IN = 0.953
R_DOUBLE_OUT = 1.0

SECTOR_ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

# ----------------------------------------------------------------------
# ПРАВИЛА РЕЖИМОВ
# ----------------------------------------------------------------------
DARTS_PER_TURN_DEFAULT = 3

MODE_CLASSIC = "classic"
MODE_TEAMS = "teams"
MODE_SPRINT6 = "sprint6"
MODE_UPGRADES = "upgrades"
MODE_CRICKET = "cricket"
MODE_501 = "501"

MODE_INFO = {
    MODE_CLASSIC: {
        "title": "Обычный",
        "icon": "🎯",
        "desc": "От 2 игроков. Каждый ход — 3 дротика. Играем N раундов, побеждает набравший больше очков.",
        "rounds": 8,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_TEAMS: {
        "title": "Команды",
        "icon": "🤝",
        "desc": "Две команды. Игроки кидают по очереди, очки команды суммируются. 8 раундов.",
        "rounds": 8,
        "min_players": 2,
        "max_players": 8,
        "teams": True,
    },
    MODE_SPRINT6: {
        "title": "Спринт 6х6",
        "icon": "⚡",
        "desc": "6 раундов с нарастающей нагрузкой: раунды 1-2 — по 1 дротику, 3-4 — по 2, 5-6 — по 3.",
        "rounds": 6,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_UPGRADES: {
        "title": "С улучшениями",
        "icon": "✨",
        "desc": "7 раундов. В начале каждого хода выпадает случайное улучшение. Чем дальше — тем мощнее!",
        "rounds": 7,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_CRICKET: {
        "title": "Крикет",
        "icon": "🏏",
        "desc": "Закройте числа 15-20 и булл. Затем зарабатывайте очки, пока соперники не закроют их.",
        "rounds": 15,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
    MODE_501: {
        "title": "501",
        "icon": "🔢",
        "desc": "Начните с 501 и уменьшайте счёт до 0. Перебор отменяет ход. Побеждает первый, кто достигнет 0.",
        "rounds": 20,
        "min_players": 2,
        "max_players": 8,
        "teams": False,
    },
}

def darts_for_round(mode, round_no):
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
