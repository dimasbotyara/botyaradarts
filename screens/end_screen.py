# screens/end_screen.py

import pygame
import config as C
import ui
import emoji_render
from game import GameManager
import stats_storage

class EndScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = {}

    def draw(self, surface):
        self.app._draw_background()
        w, h = surface.get_width(), surface.get_height()
        game = self.app.game

        if not self.app.confetti_spawned:
            colors = [p.color for p in (game.winner_players or game.players)] or [C.ACCENT, C.ACCENT_2]
            self.app.fx.spawn_confetti(w, colors)
            self.app.confetti_spawned = True

        if game.teams_mode:
            if len(game.winner_team) > 1:
                winner_txt = "🤝 Ничья между командами " + " и ".join(str(t + 1) for t in game.winner_team) + "!"
            else:
                winner_txt = f"🏆 Победила команда {game.winner_team[0] + 1}! 🎉"
        else:
            names = ", ".join(p.name for p in game.winner_players)
            winner_txt = f"🏆 Победитель: {names}! 🎉" if len(game.winner_players) == 1 else f"🤝 Ничья: {names}!"

        title = emoji_render.rtext(self.app.fonts["title"], winner_txt, C.ACCENT)
        surface.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))

        panel = pygame.Rect(int(w * 0.15), int(h * 0.18), int(w * 0.7), int(h * 0.62))
        ui.draw_panel(surface, panel)

        pad = 24
        y = panel.top + pad
        cols_x = [panel.left + pad, panel.left + int(panel.width * 0.34),
                  panel.left + int(panel.width * 0.52), panel.left + int(panel.width * 0.70),
                  panel.left + int(panel.width * 0.86)]
        headers = ["Игрок", "Очки", "Ср/дротик", "Точность", "Лучший ход"]
        for hx, htext in zip(cols_x, headers):
            hs = self.app.fonts["small"].render(htext, True, C.TEXT_DIM)
            surface.blit(hs, (hx, y))
        y += 30
        pygame.draw.line(surface, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 2)
        y += 10

        medals = ["🥇 ", "🥈 ", "🥉 "]
        for rank, p in enumerate(game.players_sorted()):
            row_color = p.color
            name_display = (medals[rank] if rank < 3 else "") + p.name
            vals = [name_display, str(p.total_score), f"{p.average_per_dart:.1f}",
                    f"{p.accuracy_percent:.0f}%", str(p.best_round)]
            for hx, v in zip(cols_x, vals):
                if hx == cols_x[0]:
                    vs = emoji_render.rtext(self.app.fonts["medium"], v, row_color)
                else:
                    vs = self.app.fonts["medium"].render(v, True, C.TEXT_MAIN)
                surface.blit(vs, (hx, y))
            y += int(self.app.fonts["medium"].get_height() * 1.6)

        if game.mode == C.MODE_UPGRADES and y < panel.bottom - pad - 20:
            pygame.draw.line(surface, C.PANEL_BORDER, (panel.left + pad, y), (panel.right - pad, y), 1)
            y += 10
            perm_header = emoji_render.rtext(self.app.fonts["small"], "♾️ Постоянные улучшения за партию:", C.ACCENT_2)
            surface.blit(perm_header, (panel.left + pad, y))
            y += perm_header.get_height() + 4
            for p in game.players_sorted():
                if y > panel.bottom - pad - 20:
                    break
                perm_names = [name for name, dur in p.upgrades_collected if dur == "permanent"]
                line = f"{p.name}: " + (", ".join(perm_names) if perm_names else "—")
                ls = emoji_render.rtext(self.app.fonts["tiny"], line, p.color)
                surface.blit(ls, (panel.left + pad, y))
                y += ls.get_height() + 3

        self.buttons = {}
        again_rect = pygame.Rect(w // 2 - 220, panel.bottom + 24, 200, 54)
        menu_rect = pygame.Rect(w // 2 + 20, panel.bottom + 24, 200, 54)
        ui.Button(again_rect, "🔁 Ещё раз", self.app.fonts["medium_bold"], style="accent").draw(surface)
        ui.Button(menu_rect, "🏠 В меню", self.app.fonts["medium_bold"], style="ghost").draw(surface)
        self.buttons["again"] = again_rect
        self.buttons["to_menu"] = menu_rect

        self.app.fx.draw_confetti(surface)
        self.app.fx.draw_ripples(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for key, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    self.app.fx.on_button_click(pos, C.ACCENT)
                    if key == "again":
                        names = [p.name for p in self.app.game.players]
                        team_of = [p.team for p in self.app.game.players] if self.app.game.teams_mode else None
                        layout = self.app._compute_layout()
                        self.app.dartboard.set_rect(layout["board"])
                        self.app.game = GameManager(self.app.mode, names, team_of=team_of, dartboard=self.app.dartboard)
                        self.app.stats_recorded = False
                        self.app.active_floats = []
                        self.app.confetti_spawned = False
                        self.app.state = "game"
                    elif key == "to_menu":
                        self.app.state = "menu"
                    return True
        return False
