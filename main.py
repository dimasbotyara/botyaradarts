# -*- coding: utf-8 -*-
"""
main.py — точка входа. Управляет окном, экранами (меню -> настройка ->
игра -> итоги -> настройки) и связывает вместе dartboard.py, game.py, ui.py,
upgrades.py, stats_storage.py.

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
STATE_SETTINGS = "settings"


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

        # Применяем сохранённые темы (интерфейс и мишень)
        ui_theme, board_theme = C.load_settings()
        C.apply_ui_theme(ui_theme)
        C.apply_board_theme(board_theme)

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

        # Кнопка статистики (правая верхняя)
        lb_rect = pygame.Rect(w - int(w * 0.22) - pad, int(h * 0.02), int(w * 0.22), int(h * 0.05))
        ui.draw_panel(self.screen, lb_rect, bg=C.PANEL_BG_LIGHT, border=C.ACCENT_2)
        lb_txt = emoji_render.rtext(self.fonts["small"], "📊 Статистика игроков", C.ACCENT_2)
        self.screen.blit(lb_txt, lb_txt.get_rect(center=lb_rect.center))
        self.buttons["leaderboard"] = lb_rect

        # Кнопка настроек (левее статистики)
        settings_rect = pygame.Rect(lb_rect.left - int(w * 0.22) - 10, int(h * 0.02),
                                    int(w * 0.22), int(h * 0.05))
        ui.draw_panel(self.screen, settings_rect, bg=C.PANEL_BG_LIGHT, border=C.ACCENT)
        settings_txt = emoji_render.rtext(self.fonts["small"], "⚙️ Настройки", C.ACCENT)
        self.screen.blit(settings_txt, settings_txt.get_rect(center=settings_rect.center))
        self.buttons["settings"] = settings_rect

        self.fx.draw_ripples(self.screen)

    def _handle_menu_click(self, pos):
        for key, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.fx.on_button_click(pos, C.ACCENT)
                if key == "leaderboard":
                    self.leaderboard_rows = stats_storage.leaderboard()
                    self.state = STATE_LEADERBOARD
                    return
                elif key == "settings":
                    self.state = STATE_SETTINGS
                    return
                elif key.startswith("mode_"):
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
    # SETTINGS
    # ------------------------------------------------------------------
    def _draw_settings(self):
        self._draw_background()
        w, h = self.screen.get_width(), self.screen.get_height()
        title = emoji_render.rtext(self.fonts["title"], "⚙️ Настройки", C.ACCENT)
        self.screen.blit(title, title.get_rect(center=(w // 2, int(h * 0.10))))

        # Панель с настройками
        panel = pygame.Rect(int(w * 0.1), int(h * 0.18), int(w * 0.8), int(h * 0.70))
        ui.draw_panel(self.screen, panel)

        pad = 24
        y = panel.top + pad

        # ======= ТЕМА ИНТЕРФЕЙСА =======
        label_ui = self.fonts["large"].render("Тема интерфейса", True, C.TEXT_MAIN)
        self.screen.blit(label_ui, (panel.left + pad, y))
        y += label_ui.get_height() + 12

        ui_names = list(C.UI_THEMES.keys())
        cols = 3 if w > 1200 else 2 if w > 800 else 1
        card_w = (panel.width - pad * (cols + 1)) // cols
        card_h = 70
        gap = 10
        self.buttons.clear()
        for i, theme_key in enumerate(ui_names):
            col = i % cols
            row = i // cols
            x = panel.left + pad + col * (card_w + gap)
            cy = y + row * (card_h + gap)
            rect = pygame.Rect(x, cy, card_w, card_h)
            theme = C.UI_THEMES[theme_key]
            is_current = (C.CURRENT_UI_THEME_NAME == theme_key)
            border = C.ACCENT if is_current else C.PANEL_BORDER
            bg = C.PANEL_BG_LIGHT if is_current else C.PANEL_BG
            ui.draw_panel(self.screen, rect, bg=bg, border=border)
            name_txt = self.fonts["small"].render(theme["name"], True, C.TEXT_MAIN)
            self.screen.blit(name_txt, (rect.left + 12, rect.top + 8))
            colors = [theme["bg_top"], theme["panel_bg"], theme["accent"], theme["text_main"]]
            sw = 18
            sx = rect.left + 12
            sy = rect.bottom - 26
            for c in colors:
                pygame.draw.rect(self.screen, c, (sx, sy, sw, sw), border_radius=4)
                sx += sw + 4
            if is_current:
                check = self.fonts["small"].render("✓", True, C.ACCENT)
                self.screen.blit(check, check.get_rect(topright=(rect.right - 10, rect.top + 6)))
            self.buttons[f"ui_theme_{theme_key}"] = rect

        y += ((len(ui_names) + cols - 1) // cols) * (card_h + gap) + 20

        # ======= ТЕМА МИШЕНИ =======
        label_board = self.fonts["large"].render("Тема мишени", True, C.TEXT_MAIN)
        self.screen.blit(label_board, (panel.left + pad, y))
        y += label_board.get_height() + 12

        board_names = list(C.BOARD_THEMES.keys())
        for i, theme_key in enumerate(board_names):
            col = i % cols
            row = i // cols
            x = panel.left + pad + col * (card_w + gap)
            cy = y + row * (card_h + gap)
            rect = pygame.Rect(x, cy, card_w, card_h)
            theme = C.BOARD_THEMES[theme_key]
            is_current = (C.CURRENT_BOARD_THEME_NAME == theme_key)
            border = C.ACCENT if is_current else C.PANEL_BORDER
            bg = C.PANEL_BG_LIGHT if is_current else C.PANEL_BG
            ui.draw_panel(self.screen, rect, bg=bg, border=border)
            name_txt = self.fonts["small"].render(theme["name"], True, C.TEXT_MAIN)
            self.screen.blit(name_txt, (rect.left + 12, rect.top + 8))
            colors = [theme["board_black"], theme["board_cream"], theme["board_red"], theme["board_green"]]
            sw = 18
            sx = rect.left + 12
            sy = rect.bottom - 26
            for c in colors:
                pygame.draw.rect(self.screen, c, (sx, sy, sw, sw), border_radius=4)
                sx += sw + 4
            if is_current:
                check = self.fonts["small"].render("✓", True, C.ACCENT)
                self.screen.blit(check, check.get_rect(topright=(rect.right - 10, rect.top + 6)))
            self.buttons[f"board_theme_{theme_key}"] = rect

        # Место под будущие настройки
        future_y = panel.bottom - pad - 60
        future_label = self.fonts["small"].render("Другие настройки появятся позже…", True, C.TEXT_DIM2)
        self.screen.blit(future_label, (panel.left + pad, future_y))

        # Кнопка назад
        back_rect = pygame.Rect(w // 2 - 100, panel.bottom + 24, 200, 54)
        ui.Button(back_rect, "⬅️ Назад", self.fonts["medium_bold"], style="ghost").draw(self.screen)
        self.buttons["back"] = back_rect

        self.fx.draw_ripples(self.screen)

    def _handle_settings_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for key, rect in self.buttons.items():
                if rect.collidepoint(pos):
                    if key == "back":
                        self.fx.on_button_click(pos, C.ACCENT_2)
                        self.state = STATE_MENU
                    elif key.startswith("ui_theme_"):
                        theme_name = key[9:]  # len("ui_theme_") == 9
                        self.fx.on_button_click(pos, C.ACCENT)
                        C.apply_ui_theme(theme_name)
                        C.save_settings(C.CURRENT_UI_THEME_NAME, C.CURRENT_BOARD_THEME_NAME)
                        self._layout_dirty = True
                    elif key.startswith("board_theme_"):
                        theme_name = key[12:]  # len("board_theme_") == 12
                        self.fx.on_button_click(pos, C.ACCENT)
                        C.apply_board_theme(theme_name)
                        C.save_settings(C.CURRENT_UI_THEME_NAME, C.CURRENT_BOARD_THEME_NAME)
                        if self.dartboard:
                            self.dartboard._surface_cache = None
                    return

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
                elif self.state == STATE_SETTINGS:
                    self._handle_settings_event(event)

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
            elif self.state == STATE_SETTINGS:
                self._draw_settings()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().run()
