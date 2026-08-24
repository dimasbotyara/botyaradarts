# app.py

import sys
import pygame

import config as C
from dartboard import Dartboard
from game import GameManager
import ui
import stats_storage
import emoji_render
import fx

from screens.menu import MenuScreen
from screens.setup import SetupScreen
from screens.game_screen import GameScreen
from screens.end_screen import EndScreen
from screens.leaderboard import LeaderboardScreen
from screens.settings import SettingsScreen


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

        # Применяем сохранённые темы и поворот
        ui_theme, board_theme, rotation = C.load_settings()
        C.apply_ui_theme(ui_theme)
        C.apply_board_theme(board_theme)
        C.BOARD_ROTATION = rotation

        self.font_name = pick_font_name()
        self.fonts = {}
        self._rebuild_fonts()

        self.state = "menu"  # "menu", "setup", "game", "end", "leaderboard", "settings"
        self.mode = None
        self.game = None
        self.dartboard = None
        self.fx = fx.EffectsManager()
        self.confetti_spawned = False

        # setup-экран
        self.setup_player_count = 2
        self.setup_inputs = []
        self.setup_teams = []
        self.setup_error = ""

        # игровой экран
        self.spinner = None
        self.spinner_hold_ms = 0
        self.active_floats = []
        self.stats_recorded = False

        self.leaderboard_rows = []

        self.buttons = {}
        self._layout_dirty = True

        # Экраны
        self.screens = {
            "menu": MenuScreen(self),
            "setup": SetupScreen(self),
            "game": GameScreen(self),
            "end": EndScreen(self),
            "leaderboard": LeaderboardScreen(self),
            "settings": SettingsScreen(self),
        }

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

    def _compute_layout(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        board_w = int(w * C.BOARD_PANEL_RATIO)
        margin = int(h * 0.025)

        board_rect = pygame.Rect(margin, margin, board_w - margin * 2, h - margin * 2)
        side = min(board_rect.width, board_rect.height)
        board_rect = pygame.Rect(0, 0, side, side)
        board_rect.center = (margin + (board_w - margin * 2) // 2, h // 2)

        right_x = board_w
        right_w = w - board_w - margin
        player_panel = pygame.Rect(right_x, margin, right_w, int(h * 0.46))
        scoreboard = pygame.Rect(right_x, player_panel.bottom + margin,
                                  right_w, int(h * 0.32))
        buttons_area = pygame.Rect(right_x, scoreboard.bottom + margin,
                                    right_w, h - scoreboard.bottom - margin * 2)
        return {"board": board_rect, "player_panel": player_panel,
                "scoreboard": scoreboard, "buttons": buttons_area}

    def _build_game_buttons(self, layout):
        self.buttons = {}
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

    def _build_setup_inputs(self):
        self.setup_inputs = []
        self.setup_teams = []
        for i in range(self.setup_player_count):
            ti = ui.TextInput((0, 0, 10, 10), self.fonts["medium"], text=f"Игрок {i + 1}",
                               placeholder=f"Игрок {i + 1}", max_len=14)
            self.setup_inputs.append(ti)
            self.setup_teams.append(i % 2)

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
        self.state = "game"

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

    def _draw_background(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        ui.draw_vertical_gradient(self.screen, (0, 0, w, h), C.BG_TOP, C.BG_BOTTOM)

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
                        elif self.state == "menu":
                            self.running = False

                # Передаём событие текущему экрану
                self.screens[self.state].handle_event(event)

            # Обновление текстовых полей
            for ti in self.setup_inputs:
                ti.update(dt)

            self.fx.update(dt / 1000.0)

            # Отрисовка текущего экрана
            self.screens[self.state].draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
