# screens/settings.py

import pygame
import config as C
import ui
import emoji_render

class SettingsScreen:
    def __init__(self, app):
        self.app = app
        self.scroll = 0
        self.max_scroll = 500
        self.buttons = {}

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll += -event.y * 40
            self.scroll = max(0, min(self.scroll, self.max_scroll))
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for key, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    self.app.fx.on_button_click(pos, C.ACCENT)
                    if key == "back":
                        self.app.state = "menu"
                    elif key.startswith("ui_theme_"):
                        theme_name = key[9:]
                        C.apply_ui_theme(theme_name)
                        C.save_settings(C.CURRENT_UI_THEME_NAME, C.CURRENT_BOARD_THEME_NAME, C.BOARD_ROTATION)
                        self.app._layout_dirty = True
                        if self.app.dartboard:
                            self.app.dartboard._surface_cache = None
                    elif key.startswith("board_theme_"):
                        theme_name = key[12:]
                        C.apply_board_theme(theme_name)
                        C.save_settings(C.CURRENT_UI_THEME_NAME, C.CURRENT_BOARD_THEME_NAME, C.BOARD_ROTATION)
                        if self.app.dartboard:
                            self.app.dartboard._surface_cache = None
                    elif key.startswith("rotation_"):
                        rotation = key[9:]
                        C.BOARD_ROTATION = rotation
                        C.save_settings(C.CURRENT_UI_THEME_NAME, C.CURRENT_BOARD_THEME_NAME, C.BOARD_ROTATION)
                        if self.app.dartboard:
                            self.app.dartboard._surface_cache = None
                    return True
        return False

    def draw(self, surface):
        self.app._draw_background()
        w, h = surface.get_width(), surface.get_height()

        # Основная панель — ЯВНО передаём цвета
        panel = pygame.Rect(int(w * 0.08), int(h * 0.08), int(w * 0.84), int(h * 0.82))
        ui.draw_panel(surface, panel, bg=C.PANEL_BG, border=C.PANEL_BORDER)

        content_rect = pygame.Rect(panel.left + 20, panel.top + 20,
                                   panel.width - 40, panel.height - 80)

        content_surface = pygame.Surface((content_rect.width, content_rect.height), pygame.SRCALPHA)
        content_surface.fill((0, 0, 0, 0))

        y = -self.scroll
        pad = 20

        title = self.app.fonts["large"].render("Тема интерфейса", True, C.TEXT_MAIN)
        content_surface.blit(title, (pad, y))
        y += title.get_height() + 12

        cols = 3 if w > 1200 else 2 if w > 800 else 1
        card_w = (content_rect.width - pad * (cols + 1)) // cols
        card_h = 70
        gap = 10

        self.buttons = {}

        # UI themes
        for i, theme_key in enumerate(C.UI_THEMES.keys()):
            col = i % cols
            row = i // cols
            x = pad + col * (card_w + gap)
            cy = y + row * (card_h + gap)
            rect = pygame.Rect(x, cy, card_w, card_h)
            theme = C.UI_THEMES[theme_key]
            is_current = (C.CURRENT_UI_THEME_NAME == theme_key)
            border = C.ACCENT if is_current else C.PANEL_BORDER
            bg = C.PANEL_BG_LIGHT if is_current else C.PANEL_BG
            ui.draw_panel(content_surface, rect, bg=bg, border=border)
            name_txt = self.app.fonts["small"].render(theme["name"], True, C.TEXT_MAIN)
            content_surface.blit(name_txt, (rect.left + 12, rect.top + 8))
            colors = [theme["bg_top"], theme["panel_bg"], theme["accent"], theme["text_main"]]
            sw = 18
            sx = rect.left + 12
            sy = rect.bottom - 26
            for c in colors:
                pygame.draw.rect(content_surface, c, (sx, sy, sw, sw), border_radius=4)
                sx += sw + 4
            if is_current:
                check = self.app.fonts["small"].render("✓", True, C.ACCENT)
                content_surface.blit(check, check.get_rect(topright=(rect.right - 10, rect.top + 6)))
            self.buttons[f"ui_theme_{theme_key}"] = rect.move(content_rect.left, content_rect.top)

        y += ((len(C.UI_THEMES) + cols - 1) // cols) * (card_h + gap) + 30

        label_board = self.app.fonts["large"].render("Тема мишени", True, C.TEXT_MAIN)
        content_surface.blit(label_board, (pad, y))
        y += label_board.get_height() + 12

        # Board themes
        for i, theme_key in enumerate(C.BOARD_THEMES.keys()):
            col = i % cols
            row = i // cols
            x = pad + col * (card_w + gap)
            cy = y + row * (card_h + gap)
            rect = pygame.Rect(x, cy, card_w, card_h)
            theme = C.BOARD_THEMES[theme_key]
            is_current = (C.CURRENT_BOARD_THEME_NAME == theme_key)
            border = C.ACCENT if is_current else C.PANEL_BORDER
            bg = C.PANEL_BG_LIGHT if is_current else C.PANEL_BG
            ui.draw_panel(content_surface, rect, bg=bg, border=border)
            name_txt = self.app.fonts["small"].render(theme["name"], True, C.TEXT_MAIN)
            content_surface.blit(name_txt, (rect.left + 12, rect.top + 8))
            colors = [theme["board_black"], theme["board_cream"], theme["board_red"], theme["board_green"]]
            sw = 18
            sx = rect.left + 12
            sy = rect.bottom - 26
            for c in colors:
                pygame.draw.rect(content_surface, c, (sx, sy, sw, sw), border_radius=4)
                sx += sw + 4
            if is_current:
                check = self.app.fonts["small"].render("✓", True, C.ACCENT)
                content_surface.blit(check, check.get_rect(topright=(rect.right - 10, rect.top + 6)))
            self.buttons[f"board_theme_{theme_key}"] = rect.move(content_rect.left, content_rect.top)

        y += ((len(C.BOARD_THEMES) + cols - 1) // cols) * (card_h + gap) + 30

        label_rot = self.app.fonts["large"].render("Поворот мишени", True, C.TEXT_MAIN)
        content_surface.blit(label_rot, (pad, y))
        y += label_rot.get_height() + 12

        rotation_options = [("6_top", "6 сверху"), ("20_top", "20 сверху")]
        for i, (key, name) in enumerate(rotation_options):
            x = pad + i * (200 + 16)
            rect = pygame.Rect(x, y, 200, 44)
            is_current = (C.BOARD_ROTATION == key)
            border = C.ACCENT if is_current else C.PANEL_BORDER
            bg = C.PANEL_BG_LIGHT if is_current else C.PANEL_BG
            ui.draw_panel(content_surface, rect, bg=bg, border=border)
            txt = self.app.fonts["small"].render(name, True, C.TEXT_MAIN)
            content_surface.blit(txt, txt.get_rect(center=rect.center))
            if is_current:
                check = self.app.fonts["small"].render("✓", True, C.ACCENT)
                content_surface.blit(check, check.get_rect(topright=(rect.right - 8, rect.top + 6)))
            self.buttons[f"rotation_{key}"] = rect.move(content_rect.left, content_rect.top)

        self.max_scroll = max(0, y + self.scroll + 60 - content_rect.height)

        original_clip = surface.get_clip()
        surface.set_clip(content_rect)
        surface.blit(content_surface, (content_rect.left, content_rect.top))
        surface.set_clip(original_clip)

        # Скроллбар
        if self.max_scroll > 0:
            track_rect = pygame.Rect(content_rect.right + 10, content_rect.top, 8, content_rect.height)
            pygame.draw.rect(surface, C.PANEL_BG_LIGHT, track_rect, border_radius=4)
            thumb_h = max(30, int(content_rect.height * (content_rect.height / (content_rect.height + self.max_scroll))))
            thumb_y = track_rect.top + int((track_rect.height - thumb_h) * (self.scroll / self.max_scroll))
            thumb_rect = pygame.Rect(track_rect.left, thumb_y, 8, thumb_h)
            pygame.draw.rect(surface, C.ACCENT, thumb_rect, border_radius=4)

        # Кнопка назад
        back_rect = pygame.Rect(w // 2 - 100, panel.bottom + 12, 200, 54)
        ui.Button(back_rect, "⬅️ Назад", self.app.fonts["medium_bold"], style="ghost").draw(surface)
        self.buttons["back"] = back_rect

        self.app.fx.draw_ripples(surface)
