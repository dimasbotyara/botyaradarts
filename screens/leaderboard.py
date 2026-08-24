# screens/leaderboard.py

import pygame
import config as C
import ui
import emoji_render
import stats_storage

class LeaderboardScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = {}

    def draw(self, surface):
        self.app._draw_background()
        w, h = surface.get_width(), surface.get_height()
        title = emoji_render.rtext(self.app.fonts["title"], "📊 Статистика игроков", C.ACCENT_2)
        surface.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))

        panel = pygame.Rect(int(w * 0.12), int(h * 0.2), int(w * 0.76), int(h * 0.62))
        ui.draw_panel(surface, panel)

        if not self.app.leaderboard_rows:
            empty = self.app.fonts["medium"].render("Пока нет сыгранных партий.", True, C.TEXT_DIM)
            surface.blit(empty, empty.get_rect(center=panel.center))
        else:
            pad = 24
            cols_x = [panel.left + pad, panel.left + int(panel.width * 0.30),
                      panel.left + int(panel.width * 0.45), panel.left + int(panel.width * 0.60),
                      panel.left + int(panel.width * 0.76), panel.left + int(panel.width * 0.90)]
            headers = ["Игрок", "Партий", "Побед", "Ср/дротик", "Лучший ход", "Лучший бросок"]
            y = panel.top + pad
            for hx, htext in zip(cols_x, headers):
                hs = self.app.fonts["small"].render(htext, True, C.TEXT_DIM)
                surface.blit(hs, (hx, y))
            y += 30
            pygame.draw.line(surface, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 2)
            y += 10
            for row in self.app.leaderboard_rows:
                vals = [row["name"], str(row["games"]), f'{row["wins"]} ({row["winrate"]:.0f}%)',
                        f'{row["avg"]:.1f}', str(row["best_round"]), str(row["best_single"])]
                for hx, v in zip(cols_x, vals):
                    vs = self.app.fonts["medium"].render(v, True, C.TEXT_MAIN)
                    surface.blit(vs, (hx, y))
                y += int(self.app.fonts["medium"].get_height() * 1.6)

        self.buttons = {}
        back_rect = pygame.Rect(w // 2 - 100, panel.bottom + 24, 200, 54)
        ui.Button(back_rect, "⬅️ Назад", self.app.fonts["medium_bold"], style="ghost").draw(surface)
        self.buttons["back"] = back_rect
        self.app.fx.draw_ripples(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buttons.get("back") and self.buttons["back"].collidepoint(event.pos):
                self.app.fx.on_button_click(event.pos, C.ACCENT_2)
                self.app.state = "menu"
                return True
        return False
