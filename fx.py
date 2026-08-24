# -*- coding: utf-8 -*-
"""
fx.py — система визуальных эффектов ("сочность" интерфейса): частицы при
попадании дротика, пульсирующее кольцо на месте удара, вспышка экрана на
крутых попаданиях, всплывающий текст-коллаут ("БУЛ!", "TRIPLE!"), рябь на
кнопках при клике и конфетти на экране победы.

Всё живёт в EffectsManager — main.py просто зовёт update(dt)/draw(...) раз
в кадр и spawn_* при нужных событиях.
"""

import math
import random
import pygame
import config as C
import emoji_render


# ==========================================================================
# ЧАСТИЦЫ (взрыв при попадании дротика)
# ==========================================================================
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "radius", "gravity")

    def __init__(self, x, y, vx, vy, life, color, radius, gravity=260):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.radius = radius
        self.gravity = gravity

    def update(self, dt):
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * t)
        r = max(1, int(self.radius * (0.4 + 0.6 * t)))
        if alpha <= 0 or r <= 0:
            return
        d = r * 2 + 2
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), r)
        surface.blit(s, (self.x - d // 2, self.y - d // 2))


class ParticleBurst:
    """Управляет коллекцией частиц-искр, разлетающихся из точки попадания."""

    def __init__(self):
        self.particles = []

    def spawn(self, pos, color, count=16, speed_range=(70, 260),
              life_range=(0.35, 0.8), radius_range=(2, 5), gravity=260):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(*life_range)
            radius = random.uniform(*radius_range)
            self.particles.append(Particle(pos[0], pos[1], vx, vy, life, color, radius, gravity))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


# ==========================================================================
# ПУЛЬСИРУЮЩЕЕ КОЛЬЦО (на месте попадания дротика)
# ==========================================================================
class RingPulse:
    def __init__(self, pos, color, max_radius=70, duration=0.5, start_radius=6, width=4):
        self.pos = pos
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.start_radius = start_radius
        self.width = width
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        radius = self.start_radius + (self.max_radius - self.start_radius) * t
        alpha = int(255 * (1 - t))
        if alpha <= 0:
            return
        d = int(radius * 2 + self.width * 2 + 4)
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), int(radius), self.width)
        surface.blit(s, (self.pos[0] - d // 2, self.pos[1] - d // 2))


class RingPulseManager:
    def __init__(self):
        self.rings = []

    def spawn(self, pos, color, **kw):
        self.rings.append(RingPulse(pos, color, **kw))

    def update(self, dt):
        for r in self.rings:
            r.update(dt)
        self.rings = [r for r in self.rings if r.alive]

    def draw(self, surface):
        for r in self.rings:
            r.draw(surface)


# ==========================================================================
# ВСПЫШКА ЭКРАНА (на бул/трипл/джекпот)
# ==========================================================================
class ScreenFlash:
    def __init__(self, color, alpha0=110, duration=0.22):
        self.color = color
        self.alpha0 = alpha0
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        alpha = int(self.alpha0 * (1 - t))
        if alpha <= 0:
            return
        w, h = surface.get_width(), surface.get_height()
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surface.blit(s, (0, 0))


class ScreenFlashManager:
    def __init__(self):
        self.flashes = []

    def spawn(self, color, **kw):
        self.flashes.append(ScreenFlash(color, **kw))

    def update(self, dt):
        for f in self.flashes:
            f.update(dt)
        self.flashes = [f for f in self.flashes if f.alive]

    def draw(self, surface):
        for f in self.flashes:
            f.draw(surface)


# ==========================================================================
# ВСПЛЫВАЮЩИЙ ТЕКСТ-КОЛЛАУТ ("БУЛ!", "TRIPLE!", "180!") — с поп-эффектом
# ==========================================================================
class Callout:
    def __init__(self, text, color, pos, duration=0.95, base_size=1.0):
        self.text = text
        self.color = color
        self.pos = pos
        self.duration = duration
        self.base_size = base_size
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface, font):
        t = min(1.0, self.age / self.duration)
        # поп-эффект: быстро растёт до 1.15, потом плавно садится к 1.0, в конце тухнет
        if t < 0.25:
            scale = self._ease_out_back(t / 0.25) * 1.15
        elif t < 0.7:
            local = (t - 0.25) / 0.45
            scale = 1.15 - 0.15 * local
        else:
            scale = 1.0
        alpha = 255 if t < 0.7 else int(255 * (1 - (t - 0.7) / 0.3))
        y_off = -40 * t

        base_surf = emoji_render.rtext(font, self.text, self.color)
        w, h = base_surf.get_size()
        scale = max(0.05, scale * self.base_size)
        scaled = pygame.transform.smoothscale(base_surf, (max(1, int(w * scale)), max(1, int(h * scale))))
        scaled.set_alpha(max(0, alpha))
        rect = scaled.get_rect(center=(self.pos[0], self.pos[1] + y_off))
        surface.blit(scaled, rect)

    @staticmethod
    def _ease_out_back(t):
        c1 = 1.70158
        c3 = c1 + 1
        t = max(0.0, min(1.0, t))
        return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


class CalloutManager:
    def __init__(self):
        self.callouts = []

    def spawn(self, text, color, pos, **kw):
        self.callouts.append(Callout(text, color, pos, **kw))

    def update(self, dt):
        for c in self.callouts:
            c.update(dt)
        self.callouts = [c for c in self.callouts if c.alive]

    def draw(self, surface, font):
        for c in self.callouts:
            c.draw(surface, font)


# ==========================================================================
# РЯБЬ НА КНОПКАХ (тактильный отклик клика)
# ==========================================================================
class Ripple:
    def __init__(self, pos, color, max_radius=55, duration=0.35):
        self.pos = pos
        self.color = color
        self.max_radius = max_radius
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt

    @property
    def alive(self):
        return self.age < self.duration

    def draw(self, surface):
        t = min(1.0, self.age / self.duration)
        radius = self.max_radius * (0.2 + 0.8 * t)
        alpha = int(160 * (1 - t))
        if alpha <= 0:
            return
        d = int(radius * 2 + 4)
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (d // 2, d // 2), int(radius))
        surface.blit(s, (self.pos[0] - d // 2, self.pos[1] - d // 2))


class RippleManager:
    def __init__(self):
        self.ripples = []

    def spawn(self, pos, color, **kw):
        self.ripples.append(Ripple(pos, color, **kw))

    def update(self, dt):
        for r in self.ripples:
            r.update(dt)
        self.ripples = [r for r in self.ripples if r.alive]

    def draw(self, surface):
        for r in self.ripples:
            r.draw(surface)


# ==========================================================================
# КОНФЕТТИ (экран победы)
# ==========================================================================
class ConfettiPiece:
    __slots__ = ("x", "y", "vx", "vy", "size", "color", "angle", "spin", "life", "max_life")

    def __init__(self, x, y, vx, vy, size, color, angle, spin, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.angle = angle
        self.spin = spin
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.vy += 60 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.spin * dt
        self.life -= dt

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * min(1.0, t * 2.2))
        s = pygame.Surface((self.size, self.size * 2), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        rotated = pygame.transform.rotate(s, self.angle)
        surface.blit(rotated, rotated.get_rect(center=(self.x, self.y)))


class ConfettiSystem:
    def __init__(self):
        self.pieces = []

    def spawn(self, width, colors, count=140, y0=-20):
        for _ in range(count):
            x = random.uniform(0, width)
            y = random.uniform(y0 - 200, y0)
            vx = random.uniform(-40, 40)
            vy = random.uniform(40, 140)
            size = random.uniform(6, 12)
            color = random.choice(colors)
            angle = random.uniform(0, 360)
            spin = random.uniform(-220, 220)
            life = random.uniform(2.5, 4.5)
            self.pieces.append(ConfettiPiece(x, y, vx, vy, size, color, angle, spin, life))

    def update(self, dt):
        for p in self.pieces:
            p.update(dt)
        self.pieces = [p for p in self.pieces if p.alive]

    def draw(self, surface):
        for p in self.pieces:
            p.draw(surface)

    def clear(self):
        self.pieces = []


# ==========================================================================
# МЕНЕДЖЕР ВСЕХ ЭФФЕКТОВ
# ==========================================================================
RING_HIT_COLORS = {
    "bull": (255, 90, 90),
    "outer_bull": (255, 150, 90),
    "triple": C.ACCENT,
    "double": C.ACCENT_2,
    "single": (200, 205, 215),
    "miss": (110, 115, 130),
}


class EffectsManager:
    def __init__(self):
        self.particles = ParticleBurst()
        self.rings = RingPulseManager()
        self.flashes = ScreenFlashManager()
        self.callouts = CalloutManager()
        self.ripples = RippleManager()
        self.confetti = ConfettiSystem()

    def update(self, dt):
        self.particles.update(dt)
        self.rings.update(dt)
        self.flashes.update(dt)
        self.callouts.update(dt)
        self.ripples.update(dt)
        self.confetti.update(dt)

    # --------------------------------------------------------------
    def on_hit(self, pos, hit, player_color):
        """Спавнит подходящий набор эффектов под конкретное попадание дротика."""
        ring = hit.ring
        color = RING_HIT_COLORS.get(ring, player_color)

        if ring == "miss":
            self.particles.spawn(pos, color, count=8, speed_range=(40, 120),
                                  life_range=(0.25, 0.45), radius_range=(1.5, 3))
            self.rings.spawn(pos, color, max_radius=34, duration=0.35, width=3)
            return

        # чем ценнее попадание — тем мощнее эффект
        big = ring in ("bull", "triple")
        count = 28 if big else (18 if ring in ("outer_bull", "double") else 12)
        self.particles.spawn(pos, color, count=count,
                              speed_range=(90, 300) if big else (60, 200),
                              life_range=(0.4, 0.9), radius_range=(2, 6 if big else 4.5))
        self.rings.spawn(pos, color, max_radius=90 if big else 55,
                          duration=0.55 if big else 0.4, width=5 if big else 3)

        if ring == "bull":
            self.flashes.spawn((255, 80, 80), alpha0=90, duration=0.22)
            self.callouts.spawn("🎯 БУЛ! 50", (255, 210, 90), pos, duration=1.0, base_size=1.15)
        elif ring == "triple":
            self.flashes.spawn(C.ACCENT, alpha0=55, duration=0.18)
            self.callouts.spawn(f"TRIPLE {hit.value}!", C.ACCENT, pos, duration=0.85)
        elif ring == "outer_bull":
            self.callouts.spawn("25!", (255, 170, 110), pos, duration=0.7, base_size=0.85)
        elif ring == "double":
            self.callouts.spawn(f"DOUBLE {hit.value}!", C.ACCENT_2, pos, duration=0.7, base_size=0.85)

    def on_big_turn(self, pos, total_points):
        """Особый коллаут за суперсильный ход (сумма очков за ход)."""
        if total_points >= 150:
            self.flashes.spawn(C.ACCENT, alpha0=130, duration=0.3)
            self.callouts.spawn(f"🔥 МАКСИМАЛКА! {total_points}", C.ACCENT, pos, duration=1.3, base_size=1.3)
        elif total_points >= 100:
            self.callouts.spawn(f"⚡ ОГОНЬ! {total_points}", C.ACCENT_2, pos, duration=1.0, base_size=1.05)

    def on_button_click(self, pos, color=None):
        self.ripples.spawn(pos, color or C.ACCENT)

    def spawn_confetti(self, width, colors):
        self.confetti.spawn(width, colors)

    def clear_confetti(self):
        self.confetti.clear()

    # --------------------------------------------------------------
    def draw_board_layer(self, surface):
        """Частицы + кольца + коллауты — рисуются поверх мишени."""
        self.particles.draw(surface)
        self.rings.draw(surface)

    def draw_callouts(self, surface, font):
        self.callouts.draw(surface, font)

    def draw_ripples(self, surface):
        self.ripples.draw(surface)

    def draw_flashes(self, surface):
        self.flashes.draw(surface)

    def draw_confetti(self, surface):
        self.confetti.draw(surface)
