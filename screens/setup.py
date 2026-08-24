# screens/setup.py
import pygame
import config as C
import ui
import emoji_render

class SetupScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = {}

    def draw(self, surface):
        self.app._draw_background()
        w, h = surface.get_width(), surface.get_height()
        info = C.MODE_INFO[self.app.mode]

        title = emoji_render.rtext(self.app.fonts["large"], f"{info['icon']} Настройка: {info['title']}", C.ACCENT)
        surface.blit(title, title.get_rect(center=(w // 2, int(h * 0.08))))

        panel = pygame.Rect(int(w * 0.2), int(h * 0.16), int(w * 0.6), int(h * 0.66))
        ui.draw_panel(surface, panel)

        pad = int(panel.width * 0.05)
        y = panel.top + pad

        self.buttons = {}
        if info["min_players"] != info["max_players"]:
            cnt_label = self.app.fonts["medium"].render(
                f"Количество игроков: {self.app.setup_player_count}", True, C.TEXT_MAIN)
            surface.blit(cnt_label, (panel.left + pad, y))
            minus_rect = pygame.Rect(panel.right - pad - 160, y - 6, 70, 44)
            plus_rect = pygame.Rect(panel.right - pad - 80, y - 6, 70, 44)
            ui.Button(minus_rect, "-", self.app.fonts["medium_bold"]).draw(surface)
            ui.Button(plus_rect, "+", self.app.fonts["medium_bold"]).draw(surface)
            self.buttons["count_minus"] = minus_rect
            self.buttons["count_plus"] = plus_rect
            y += 60

        input_h = max(40, int(h * 0.05))
        input_w = int(panel.width * 0.5) if not info["teams"] else int(panel.width * 0.38)
        for i, ti in enumerate(self.app.setup_inputs):
            ti.rect = pygame.Rect(panel.left + pad, y, input_w, input_h)
            ti.font = self.app.fonts["medium"]
            ti.draw(surface)
            if info["teams"]:
                team_rect = pygame.Rect(ti.rect.right + 16, y, panel.width - pad * 2 - input_w - 16, input_h)
                team_color = C.TEAM_COLORS[self.app.setup_teams[i]]
                pygame.draw.rect(surface, C.PANEL_BG_LIGHT, team_rect, border_radius=10)
                pygame.draw.rect(surface, team_color, team_rect, 2, border_radius=10)
                team_txt = self.app.fonts["small"].render(f"Команда {self.app.setup_teams[i] + 1} (клик — сменить)",
                                                        True, team_color)
                surface.blit(team_txt, team_txt.get_rect(center=team_rect.center))
                self.buttons[f"team_{i}"] = team_rect
            y += input_h + 14

        if self.app.setup_error:
            err = self.app.fonts["small"].render(self.app.setup_error, True, C.DANGER)
            surface.blit(err, (panel.left + pad, panel.bottom - pad - err.get_height() - 60))

        start_rect = pygame.Rect(panel.centerx - 140, panel.bottom - pad - 50, 280, 50)
        back_rect = pygame.Rect(panel.left + pad, panel.bottom - pad - 50, 140, 50)
        ui.Button(start_rect, "▶️ Начать игру", self.app.fonts["medium_bold"], style="accent").draw(surface)
        ui.Button(back_rect, "⬅️ Назад", self.app.fonts["medium_bold"], style="ghost").draw(surface)
        self.buttons["start"] = start_rect
        self.buttons["back"] = back_rect

    def handle_event(self, event):
        # Обработка текстовых полей
        for ti in self.app.setup_inputs:
            ti.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for key, rect in self.buttons.items():
                if not rect.collidepoint(pos):
                    continue
                if key == "count_plus":
                    info = C.MODE_INFO[self.app.mode]
                    if self.app.setup_player_count < info["max_players"]:
                        self.app.setup_player_count += 1
                        self.app._build_setup_inputs()
                elif key == "count_minus":
                    info = C.MODE_INFO[self.app.mode]
                    if self.app.setup_player_count > info["min_players"]:
                        self.app.setup_player_count -= 1
                        self.app._build_setup_inputs()
                elif key.startswith("team_"):
                    idx = int(key.split("_")[1])
                    self.app.setup_teams[idx] = 1 - self.app.setup_teams[idx]
                elif key == "start":
                    self.app._try_start_game()
                elif key == "back":
                    self.app.state = "menu"
                return True
        return False
