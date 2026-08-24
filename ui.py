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

    # пульсирующее свечение вокруг панели текущего игрока
    pulse = (math.sin(pygame.time.get_ticks() / 320.0) + 1) / 2
    glow_alpha = int(50 + 90 * pulse)
    glow_pad = 8
    glow_surf = pygame.Surface((rect.width + glow_pad * 2, rect.height + glow_pad * 2), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*p.color, glow_alpha), glow_surf.get_rect(),
                     width=4, border_radius=22)
    surface.blit(glow_surf, (rect.left - glow_pad, rect.top - glow_pad))

    # цветная полоска-акцент игрока
    pygame.draw.rect(surface, p.color, (rect.left, rect.top, rect.width, 8),
                     border_top_left_radius=16, border_top_right_radius=16)

    # ─── ЛЕВАЯ КОЛОНКА ───────────────────────────────────────────────
    left_x = rect.left + pad
    left_w = int(rect.width * 0.58)  # 58% ширины
    y = rect.top + pad + 6

    label = emoji_render.rtext(fonts["small"], "🎯 ХОДИТ СЕЙЧАС", C.TEXT_DIM)
    surface.blit(label, (left_x, y))
    y += label.get_height() + 4

    name_surf = fonts["huge"].render(p.name, True, p.color)
    surface.blit(name_surf, (left_x, y))
    y += name_surf.get_height() + int(pad * 0.4)

    if game.teams_mode:
        team_txt = fonts["small"].render(f"Команда {p.team + 1}", True, C.TEXT_DIM)
        surface.blit(team_txt, (left_x, y))
        y += team_txt.get_height() + 8

    # общий счёт
    score_label = fonts["small"].render("ОБЩИЙ СЧЁТ", True, C.TEXT_DIM)
    surface.blit(score_label, (left_x, y))
    y += score_label.get_height() + 2
    score_surf = fonts["score"].render(str(p.total_score), True, C.TEXT_MAIN)
    surface.blit(score_surf, (left_x, y))
    y += score_surf.get_height() + int(pad * 0.5)

    # индикатор дротиков
    thrown, total = game.darts_thrown_progress()
    dot_r = max(10, int(rect.height * 0.022))
    dot_gap = dot_r * 3
    dx = left_x + dot_r
    dart_label = fonts["small"].render(
        f"ДРОТИКИ: осталось {p.darts_remaining} из {total}", True, C.TEXT_DIM)
    surface.blit(dart_label, (left_x, y))
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

    # активные бонусы хода
    tags = []
    if p.turn_multiplier > 1.001:
        tags.append(f"×{p.turn_multiplier:.2g} очки")
    if p.miss_floor > p.perm_miss_floor:
        tags.append(f"промах = {p.miss_floor}")
    if getattr(p, 'single_bonus', 0) > 0:
        tags.append(f"сингл +{p.single_bonus}")
    if tags:
        tag_label = emoji_render.rtext(fonts["small"], "🔥 В ЭТОМ ХОДЕ: " + ", ".join(tags), C.ACCENT)
        surface.blit(tag_label, (left_x, y))
        y += tag_label.get_height() + 6

    # очки за текущий ход (внизу левой колонки)
    round_label = fonts["medium"].render(f"Очки за этот ход: {p.current_round_points}",
                                          True, C.ACCENT_2)
    surface.blit(round_label, (left_x, rect.bottom - round_label.get_height() - pad))

    # ─── ПРАВАЯ КОЛОНКА ──────────────────────────────────────────────
    right_x = rect.left + int(rect.width * 0.62)
    right_w = rect.right - right_x - pad
    right_y = rect.top + pad + 6

    # раунд и режим
    round_txt = fonts["medium"].render(f"Раунд {game.round_no}/{game.rounds_total}", True, C.TEXT_MAIN)
    surface.blit(round_txt, round_txt.get_rect(topright=(rect.right - pad, right_y)))
    mode_txt = fonts["small"].render(game.info["title"], True, C.TEXT_DIM)
    surface.blit(mode_txt, mode_txt.get_rect(topright=(rect.right - pad, right_y + round_txt.get_height() + 2)))

    right_y += round_txt.get_height() + mode_txt.get_height() + 14

    # постоянные улучшения
    perm_label = emoji_render.rtext(fonts["small"], "♾️ ПОСТОЯННЫЕ УЛУЧШЕНИЯ:", C.ACCENT_2)
    surface.blit(perm_label, (right_x, right_y))
    right_y += perm_label.get_height() + 6

    perm_upgrades = [name for name, dur in p.upgrades_collected if dur == "permanent"]
    if not perm_upgrades:
        no_perm = fonts["tiny"].render("Пока нет", True, C.TEXT_DIM2)
        surface.blit(no_perm, (right_x, right_y))
    else:
        # ограничиваем количество строк, чтобы влезало
        available_height = rect.bottom - pad - right_y - 10
        line_h = fonts["tiny"].get_height() + 3
        max_lines = max(1, available_height // line_h)
        if len(perm_upgrades) > max_lines:
            # показываем последние max_lines, сверху добавляем многоточие
            shown = perm_upgrades[-max_lines:]
            dots = fonts["tiny"].render("…", True, C.TEXT_DIM2)
            surface.blit(dots, (right_x, right_y))
            right_y += dots.get_height() + 3
        else:
            shown = perm_upgrades
        for name in shown:
            bullet = emoji_render.rtext(fonts["tiny"], f"• {name}", C.TEXT_DIM)
            surface.blit(bullet, (right_x + 6, right_y))
            right_y += bullet.get_height() + 3

    # временные эффекты этого хода
    turn_effects = [name for name, dur in p.upgrades_collected if dur == "turn"]
    if turn_effects:
        right_y += 8
        turn_label = emoji_render.rtext(fonts["small"], "⏳ В ЭТОМ ХОДЕ:", C.ACCENT)
        surface.blit(turn_label, (right_x, right_y))
        right_y += turn_label.get_height() + 4
        for name in turn_effects[-3:]:  # показываем максимум 3 последних
            bullet = emoji_render.rtext(fonts["tiny"], f"• {name}", C.ACCENT)
            surface.blit(bullet, (right_x + 6, right_y))
            right_y += bullet.get_height() + 3


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
