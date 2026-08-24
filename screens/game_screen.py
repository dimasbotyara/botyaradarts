# screens/game_screen.py

import pygame
import config as C
import ui
import emoji_render
from upgrades import UpgradeSpinner
from game import GameManager
import stats_storage

class GameScreen:
    def __init__(self, app):
        self.app = app
        self.buttons = {}

    def draw(self, surface):
        self.app._draw_background()
        layout = self.app._compute_layout()
        if self.app.dartboard.rect != layout["board"]:
            self.app.dartboard.set_rect(layout["board"])
        self.app._build_game_buttons(layout)

        hover = None
        if self.app.dartboard.rect.collidepoint(pygame.mouse.get_pos()) and not self.app.game.awaiting_upgrade:
            hover = pygame.mouse.get_pos()
        self.app.dartboard.draw(surface, hover_pos=hover, last_hits=self.app.game.last_hits)
        self.app.fx.draw_board_layer(surface)

        ui.draw_player_panel(surface, layout["player_panel"], self.app.game, self.app.fonts)
        ui.draw_scoreboard(surface, layout["scoreboard"], self.app.game, self.app.fonts)

        for b in self.buttons.values():
            b.draw(surface)
        self.app.fx.draw_ripples(surface)

        self.app._draw_floating_texts()
        self.app.fx.draw_callouts(surface, self.app.fonts["large"])
        self.app.fx.draw_flashes(surface)

        if self.app.game.mode == C.MODE_UPGRADES and self.app.game.awaiting_upgrade:
            self._draw_upgrade_spinner(surface, layout)

        if self.app.game.game_over:
            if not self.app.stats_recorded:
                stats_storage.record_game(self.app.game)
                self.app.stats_recorded = True
            self.app.state = "end"

    def _draw_upgrade_spinner(self, surface, layout):
        w, h = surface.get_width(), surface.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((5, 5, 8, 190))
        surface.blit(overlay, (0, 0))

        p = self.app.game.current_player
        name_txt = emoji_render.rtext(self.app.fonts["large"], f"🎁 {p.name}, твоё улучшение…", p.color)
        surface.blit(name_txt, name_txt.get_rect(center=(w // 2, int(h * 0.22))))

        panel_w = min(560, int(w * 0.4))
        panel_h = int(h * 0.42)
        panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
        panel_rect.center = (w // 2, h // 2)

        if self.app.spinner is None:
            result = self.app.game.roll_upgrade_for_current()
            self.app.spinner = UpgradeSpinner(result)

        self.app.spinner.draw(surface, panel_rect, self.app.fonts["large"], self.app.fonts["small"], self.app.fonts["tiny"])

        if self.app.spinner.done:
            self.app.spinner_hold_ms += self.app.clock.get_time()
            hint = emoji_render.rtext(self.app.fonts["small"], "👉 Клик, чтобы продолжить", C.TEXT_DIM)
            surface.blit(hint, hint.get_rect(center=(w // 2, panel_rect.bottom + 40)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.app.game.mode == C.MODE_UPGRADES and self.app.game.awaiting_upgrade:
                if self.app.spinner and self.app.spinner.done and self.app.spinner_hold_ms > 150:
                    self.app.game.apply_upgrade(self.app.spinner.result)
                    self.app.spinner = None
                    self.app.spinner_hold_ms = 0
                return True
            for key, btn in self.buttons.items():
                if btn.rect.collidepoint(pos):
                    self.app.fx.on_button_click(pos, C.ACCENT if key != "skip" else C.DANGER)
                    if key == "new_game":
                        self.app.state = "menu"
                    elif key == "undo":
                        self.app.game.undo()
                    elif key == "skip":
                        self.app.game.skip_turn()
                    return True
            if self.app.dartboard.rect.collidepoint(pos):
                thrower = self.app.game.current_player
                rounds_before = len(thrower.round_scores)
                hit = self.app.game.throw(pos)
                if hit is not None:
                    self.app.fx.on_hit(pos, hit, thrower.color)
                    if len(thrower.round_scores) > rounds_before:
                        self.app.fx.on_big_turn(pos, thrower.round_scores[-1])
                layout = self.app._compute_layout()
                self.app._spawn_floats_from_game(layout)
        return False
