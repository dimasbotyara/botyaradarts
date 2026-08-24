# -*- coding: utf-8 -*-
"""
dartboard.py — отрисовка мишени и определение результата клика мышкой.
"""

import math
import pygame
import config as C


class HitResult:
    __slots__ = ("value", "multiplier", "points", "label", "ring")

    def __init__(self, value, multiplier, label, ring):
        self.value = value
        self.multiplier = multiplier
        self.points = value * multiplier if ring not in ("bull", "outer_bull") else value
        self.label = label
        self.ring = ring

    def __repr__(self):
        return f"<Hit {self.label} = {self.points}>"


class Dartboard:
    def __init__(self, rect: pygame.Rect):
        self.set_rect(rect)
        self._surface_cache = None
        self._cache_key = None

    def set_rect(self, rect: pygame.Rect):
        self.rect = pygame.Rect(rect)
        self.cx = self.rect.centerx
        self.cy = self.rect.centery
        self.radius = int(min(self.rect.width, self.rect.height) * 0.47)
        self._surface_cache = None

    def hit_test(self, pos):
        dx = pos[0] - self.cx
        dy = pos[1] - self.cy
        dist = math.hypot(dx, dy)
        r = dist / self.radius if self.radius > 0 else 999

        if r > C.R_DOUBLE_OUT:
            return HitResult(0, 1, "МИМО", "miss")
        if r <= C.R_BULL:
            return HitResult(50, 1, "БУЛ 50", "bull")
        if r <= C.R_OUTER_BULL:
            return HitResult(25, 1, "25", "outer_bull")

        angle = math.degrees(math.atan2(dx, -dy))
        angle = (angle + 360) % 360

        # Учитываем поворот мишени
        if C.BOARD_ROTATION == "6_top":
            angle = (angle + 90) % 360
        # если "20_top" — ничего не добавляем

        sector_index = int(((angle + 9) % 360) // 18)
        value = C.SECTOR_ORDER[sector_index]

        if C.R_TRIPLE_IN < r <= C.R_TRIPLE_OUT:
            return HitResult(value, 3, f"T{value}", "triple")
        if C.R_DOUBLE_IN < r <= C.R_DOUBLE_OUT:
            return HitResult(value, 2, f"D{value}", "double")
        return HitResult(value, 1, f"{value}", "single")

    def draw(self, surface, hover_pos=None, last_hits=None):
        cache_key = (self.rect.width, self.rect.height, self.rect.topleft)
        if self._surface_cache is None or self._cache_key != cache_key:
            self._build_static_surface()
            self._cache_key = cache_key

        surface.blit(self._surface_cache, self.rect.topleft)

        if hover_pos:
            hit = self.hit_test(hover_pos)
            if hit.ring != "miss":
                self._draw_hover_highlight(surface, hit)

        if last_hits:
            for pos, color in last_hits:
                pygame.draw.circle(surface, (255, 255, 255), pos, 9)
                pygame.draw.circle(surface, color, pos, 6)
                pygame.draw.circle(surface, (20, 20, 20), pos, 9, 2)

    def _build_static_surface(self):
        size = (self.rect.width, self.rect.height)
        surf = pygame.Surface(size, pygame.SRCALPHA)
        cx = self.rect.width // 2
        cy = self.rect.height // 2
        R = self.radius

        # Начальный угол в зависимости от поворота
        if C.BOARD_ROTATION == "6_top":
            offset_deg = -90
        else:
            offset_deg = 0

        pygame.draw.circle(surf, C.BOARD_RIM, (cx, cy), int(R * 1.09))
        pygame.draw.circle(surf, C.BOARD_OUT, (cx, cy), int(R * C.R_DOUBLE_OUT) + 4)

        n = len(C.SECTOR_ORDER)
        for i, value in enumerate(C.SECTOR_ORDER):
            start_deg = offset_deg + i * 18 - 9
            self._draw_sector_wedge(surf, cx, cy, R, start_deg, 18, i)

        for frac in (C.R_TRIPLE_IN, C.R_TRIPLE_OUT, C.R_DOUBLE_IN, C.R_DOUBLE_OUT):
            pygame.draw.circle(surf, C.BOARD_WIRE, (cx, cy), int(R * frac), 1)

        pygame.draw.circle(surf, C.BOARD_YELLOW, (cx, cy), int(R * C.R_OUTER_BULL))
        pygame.draw.circle(surf, C.BOARD_BLACK, (cx, cy), int(R * C.R_BULL))
        pygame.draw.circle(surf, C.BOARD_WIRE, (cx, cy), int(R * C.R_OUTER_BULL), 1)

        for i in range(n):
            deg = offset_deg + i * 18 - 9
            rad = math.radians(deg)
            x2 = cx + math.sin(rad) * R * C.R_DOUBLE_OUT
            y2 = cy - math.cos(rad) * R * C.R_DOUBLE_OUT
            x1 = cx + math.sin(rad) * R * C.R_OUTER_BULL
            y1 = cy - math.cos(rad) * R * C.R_OUTER_BULL
            pygame.draw.line(surf, C.BOARD_WIRE, (x1, y1), (x2, y2), 1)

        font = pygame.font.SysFont(_pick_font(), max(14, int(R * 0.11)), bold=True)
        label_r = R * 1.02
        shadow_offset = 2
        for i, value in enumerate(C.SECTOR_ORDER):
            deg = offset_deg + i * 18
            rad = math.radians(deg)
            lx = cx + math.sin(rad) * label_r
            ly = cy - math.cos(rad) * label_r
            shadow = font.render(str(value), True, (0, 0, 0))
            surf.blit(shadow, shadow.get_rect(center=(lx + shadow_offset, ly + shadow_offset)))
            text = font.render(str(value), True, C.TEXT_MAIN)
            surf.blit(text, text.get_rect(center=(lx, ly)))

        self._surface_cache = surf

    def _draw_sector_wedge(self, surf, cx, cy, R, start_deg, span_deg, index):
        is_alt = index % 2 == 0
        single_color = C.BOARD_CREAM if is_alt else C.BOARD_BLACK
        special_color = C.BOARD_YELLOW if is_alt else C.BOARD_RED

        rings = [
            (C.R_OUTER_BULL, C.R_TRIPLE_IN, single_color),
            (C.R_TRIPLE_IN, C.R_TRIPLE_OUT, special_color),
            (C.R_TRIPLE_OUT, C.R_DOUBLE_IN, single_color),
            (C.R_DOUBLE_IN, C.R_DOUBLE_OUT, special_color),
        ]
        for r_in, r_out, color in rings:
            self._draw_ring_wedge(surf, cx, cy, R * r_in, R * r_out, start_deg, span_deg, color)

    @staticmethod
    def _draw_ring_wedge(surf, cx, cy, r_in, r_out, start_deg, span_deg, color):
        steps = 6
        pts = []
        for s in range(steps + 1):
            deg = start_deg + span_deg * s / steps
            rad = math.radians(deg)
            pts.append((cx + math.sin(rad) * r_out, cy - math.cos(rad) * r_out))
        for s in range(steps + 1):
            deg = start_deg + span_deg * (steps - s) / steps
            rad = math.radians(deg)
            pts.append((cx + math.sin(rad) * r_in, cy - math.cos(rad) * r_in))
        if len(pts) >= 3:
            pygame.draw.polygon(surf, color, pts)

    def _draw_hover_highlight(self, surface, hit: HitResult):
        color = C.ACCENT if hit.ring in ("double", "triple") else (255, 255, 255)
        surface_rect = self.rect
        pygame.draw.rect(surface, color, surface_rect, 3, border_radius=int(self.radius * 0.05))


_FONT_CHOSEN = None

def _pick_font():
    global _FONT_CHOSEN
    if _FONT_CHOSEN:
        return _FONT_CHOSEN
    available = pygame.font.get_fonts()
    for cand in C.FONT_NAME_CANDIDATES:
        if cand in available:
            _FONT_CHOSEN = cand
            return cand
    _FONT_CHOSEN = pygame.font.get_default_font()
    return _FONT_CHOSEN
