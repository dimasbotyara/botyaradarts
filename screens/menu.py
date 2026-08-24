# screens/menu.py

import pygame
import config as C
import ui
import emoji_render
import stats_storage

class MenuScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = {}

    def draw(self, surface):
        self.app._draw_background()
        w, h = surface.get_width(), surface.get_height()
        title = emoji_render.rtext(self.app.fonts["title"], "🎯 ДАРТС — Домашний счёт", C.ACCENT)
        surface.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))
        sub = emoji_render.rtext(self.app.fonts["medium"], "Выберите режим игры 👇", C.TEXT_DIM)
        surface.blit(sub, sub.get_rect(center=(w // 2, int(h * 0.16))))

        modes = list(C.MODE_INFO.keys())
        cols = 3 if w > 1200 else 2 if w > 800 else 1
        rows = (len(modes) + cols - 1) // cols
        pad = int(w * 0.03)
        area_top = int(h * 0.22)
        area_bottom = int(h * 0.88)
        card_w = (w - pad * (cols + 1)) // cols
        card_h = min(int((area_bottom - area_top - pad * (rows - 1)) / rows), int(h * 0.28))

        self.buttons = {}
        for i, mode_key in enumerate(modes):
            col = i % cols
            row = i // cols
            x = pad + col * (card_w + pad)
            y = area_top + row * (card_h + pad)
            rect = pygame.Rect(x, y, card_w, card_h)
            info = C.MODE_INFO[mode_key]
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            bg = C.PANEL_BG_LIGHT if hovered else C.PANEL_BG
            ui.draw_panel(surface, rect, bg=bg, border=C.ACCENT if hovered else C.PANEL_BORDER)

            title_s = emoji_render.rtext(self.app.fonts["large"], f"{info['icon']} {info['title']}", C.ACCENT)
            surface.blit(title_s, (rect.left + 20, rect.top + 16))
            lines = ui.render_text_wrapped(self.app.fonts["small"], info["desc"], C.TEXT_DIM, rect.width - 40)
            ly = rect.top + 16 + title_s.get_height() + 12
            for line in lines:
                surface.blit(line, (rect.left + 20, ly))
                ly += line.get_height() + 4

            rounds_txt = self.app.fonts["tiny"].render(
                f"Раундов: {info['rounds']}  •  Игроков: {info['min_players']}-{info['max_players']}",
                True, C.TEXT_DIM2)
            surface.blit(rounds_txt, (rect.left + 20, rect.bottom - rounds_txt.get_height() - 14))

            self.buttons[f"mode_{mode_key}"] = rect

        # Кнопка статистики
        lb_rect = pygame.Rect(w - int(w * 0.22) - pad, int(h * 0.02), int(w * 0.22), int(h * 0.05))
        ui.draw_panel(surface, lb_rect, bg=C.PANEL_BG_LIGHT, border=C.ACCENT_2)
        lb_txt = emoji_render.rtext(self.app.fonts["small"], "📊 Статистика игроков", C.ACCENT_2)
        surface.blit(lb_txt, lb_txt.get_rect(center=lb_rect.center))
        self.buttons["leaderboard"] = lb_rect

        # Кнопка настроек
        settings_rect = pygame.Rect(lb_rect.left - int(w * 0.22) - 10, int(h * 0.02),
                                    int(w * 0.22), int(h * 0.05))
        ui.draw_panel(surface, settings_rect, bg=C.PANEL_BG_LIGHT, border=C.ACCENT)
        settings_txt = emoji_render.rtext(self.app.fonts["small"], "⚙️ Настройки", C.ACCENT)
        surface.blit(settings_txt, settings_txt.get_rect(center=settings_rect.center))
        self.buttons["settings"] = settings_rect

        self.app.fx.draw_ripples(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for key, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    self.app.fx.on_button_click(pos, C.ACCENT)
                    if key == "leaderboard":
                        self.app.leaderboard_rows = stats_storage.leaderboard()
                        self.app.state = "leaderboard"
                    elif key == "settings":
                        self.app.state = "settings"
                    elif key.startswith("mode_"):
                        self.app.mode = key[5:]
                        info = C.MODE_INFO[self.app.mode]
                        self.app.setup_player_count = info["min_players"]
                        self.app._build_setup_inputs()
                        self.app.setup_error = ""
                        self.app.state = "setup"
                    return True
        return False
