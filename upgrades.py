# -*- coding: utf-8 -*-
"""
upgrades.py — режим "С улучшениями": определения бонусов и анимация
слот-машины (прокрутка), которая "выпадает" каждому игроку в начале хода.

Улучшения делятся по двум осям:
  • tier (1/2/3)       — сила эффекта. Чем дальше раунд, тем чаще выпадают
                          старшие уровни ("чем дальше в лейт-гейм, тем круче").
  • duration           — "turn" (действует только в этом ходе) или
                          "permanent" (пассивный эффект до конца всей партии,
                          складывается с другими постоянными бонусами).
"""

import random
import pygame
import config as C
import emoji_render


class Upgrade:
    def __init__(self, key, name, desc, tier, duration, color, apply_fn):
        self.key = key
        self.name = name
        self.desc = desc
        self.tier = tier                # 1, 2, 3
        self.duration = duration        # "turn" | "permanent"
        self.color = color
        self.apply_fn = apply_fn        # apply_fn(game, player)

    def apply(self, game, player):
        self.apply_fn(game, player)


# ==========================================================================
# ЭФФЕКТЫ "НА ЭТОТ ХОД"
# ==========================================================================
def _fx_extra_dart(n):
    def fn(game, player):
        player.extra_darts_bonus += n
        player.darts_remaining += n
    return fn


def _fx_multiplier(mult):
    def fn(game, player):
        player.turn_multiplier *= mult
    return fn


def _fx_flat_bonus(n):
    def fn(game, player):
        player.total_score += n
        player.current_round_points += n
        game.floating_texts.append((f"+{n}", player))
    return fn


def _fx_steal_from_leader(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        leader = max(others, key=lambda p: p.total_score)
        effective = max(0, int(round(n * (1 - leader.perm_shield))))
        steal = min(effective, leader.total_score)
        leader.total_score -= steal
        player.total_score += steal
        player.current_round_points += steal
        game.floating_texts.append((f"-{steal}", leader))
        game.floating_texts.append((f"+{steal}", player))
    return fn


def _fx_weaken_leader(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        leader = max(others, key=lambda p: p.total_score)
        effective = max(0, int(round(n * (1 - leader.perm_shield))))
        loss = min(effective, leader.total_score)
        leader.total_score -= loss
        game.floating_texts.append((f"-{loss}", leader))
    return fn


def _fx_weaken_random_opponent(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player and p.team != player.team]
        if not others:
            others = [p for p in game.players if p is not player]
        if not others:
            return
        target = random.choice(others)
        effective = max(0, int(round(n * (1 - target.perm_shield))))
        loss = min(effective, target.total_score)
        target.total_score -= loss
        game.floating_texts.append((f"-{loss}", target))
    return fn


def _fx_miss_becomes(n):
    def fn(game, player):
        player.miss_floor = max(player.miss_floor, n)
    return fn


def _fx_sabotage_dart(n):
    def fn(game, player):
        others = [p for p in game.players if p is not player and p.team != player.team]
        if not others:
            others = [p for p in game.players if p is not player]
        if not others:
            return
        target = random.choice(others)
        effective = max(0, int(round(n * (1 - target.perm_shield))))
        if effective <= 0:
            game.floating_texts.append(("ЩИТ!", target))
            return
        target.pending_dart_penalty += effective
        game.floating_texts.append((f"-{effective} дрот.", target))
    return fn


def _fx_double_darts_this_turn():
    def fn(game, player):
        extra = player.darts_remaining + player.extra_darts_bonus
        player.extra_darts_bonus += extra
        player.darts_remaining += extra
    return fn


def _fx_copy_best_round():
    def fn(game, player):
        bonus = max(player.best_round, 15)
        player.total_score += bonus
        player.current_round_points += bonus
        game.floating_texts.append((f"+{bonus}", player))
    return fn


# === НОВЫЕ ЭФФЕКТЫ (16 штук) ===
def _fx_earthquake():
    """Все соперники теряют 10% от текущего счёта (минимум 5)."""
    def fn(game, player):
        for target in game.players:
            if target is player:
                continue
            loss = max(5, int(target.total_score * 0.1))
            loss = min(loss, target.total_score)
            target.total_score -= loss
            game.floating_texts.append((f"-{loss}", target))
    return fn


def _fx_curse():
    """Следующий ход случайного соперника будет с множителем x0.5."""
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        target = random.choice(others)
        target.turn_multiplier_penalty = 0.5
        game.floating_texts.append(("Проклят!", target))
    return fn


def _fx_steal_dart():
    """Украсть 1 дротик у лидера."""
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        if not others:
            return
        leader = max(others, key=lambda p: p.total_score)
        leader.pending_dart_penalty += 1
        game.floating_texts.append(("-1 дрот.", leader))
    return fn


def _fx_double_first_throw():
    """Первый бросок в этом ходе дублируется."""
    def fn(game, player):
        player.first_throw_doubled = True
    return fn


def _fx_mirror_shield():
    """Если у игрока украдут очки, вор потеряет столько же."""
    def fn(game, player):
        player.mirror_shield = True
    return fn


def _fx_kamikaze():
    """При промахе в этом ходе все соперники теряют по 3 очка."""
    def fn(game, player):
        player.kamikaze = True
    return fn


def _fx_immunity():
    """Защита от негативных эффектов на 2 хода."""
    def fn(game, player):
        player.negative_effect_immune = 2
    return fn


def _fx_casino_risky():
    """Множитель очков в этом ходе: 0.5, 1.5, 2 или 3."""
    def fn(game, player):
        mult = random.choice([0.5, 1.5, 2.0, 3.0])
        player.turn_multiplier *= mult
        game.floating_texts.append((f"x{mult} 🎰", player))
    return fn


def _fx_lottery():
    """Все, кроме лидера, получают +20; если ты лидер — +15."""
    def fn(game, player):
        others = [p for p in game.players if p is not player]
        leader = max(game.players, key=lambda p: p.total_score)
        for p in game.players:
            if p is player:
                bonus = 15 if p is leader else 20
                p.total_score += bonus
                p.current_round_points += bonus
                game.floating_texts.append((f"+{bonus}", p))
            else:
                bonus = 20
                p.total_score += bonus
                game.floating_texts.append((f"+{bonus}", p))
    return fn


def _fx_snowball():
    """Постоянный: каждый следующий дротик в ходе даёт на 5% больше."""
    def fn(game, player):
        player.snowball = True
    return fn


def _fx_collector():
    """Постоянный: +3 очка за каждый брошенный дротик."""
    def fn(game, player):
        player.collector += 3
    return fn


def _fx_gold_rush():
    """Постоянный: если за ход >50 очков, в следующем ходе +5 пассивно."""
    def fn(game, player):
        player.gold_rush = True
    return fn


def _fx_vampire():
    """Постоянный: если за ход >60 очков, восстанавливает 1 дротик в след. ходе."""
    def fn(game, player):
        player.vampire = True
    return fn


def _fx_clone():
    """Клон: +1 дротик, но с половинным множителем."""
    def fn(game, player):
        player.clone = True
        player.extra_darts_bonus += 1
        player.darts_remaining += 1
        player.turn_multiplier *= 0.5
    return fn

def _fx_flat_bonus_and_dart(bonus, darts):
    """Сразу +bonus очков и +darts дротиков в этом ходе."""
    def fn(game, player):
        player.total_score += bonus
        player.current_round_points += bonus
        player.extra_darts_bonus += darts
        player.darts_remaining += darts
        game.floating_texts.append((f"+{bonus} и +{darts} дрот.", player))
    return fn

def _fx_gravity():
    """Одиночные сектора в этом ходе дают x1.6."""
    def fn(game, player):
        player.gravity = True
    return fn


# ==========================================================================
# ЭФФЕКТЫ "НАВСЕГДА"
# ==========================================================================
def _fx_perm_multiplier(factor):
    def fn(game, player):
        player.perm_multiplier *= factor
    return fn


def _fx_perm_flat_income(n):
    def fn(game, player):
        player.perm_flat_per_turn += n
    return fn


def _fx_perm_miss_floor(n):
    def fn(game, player):
        player.perm_miss_floor = max(player.perm_miss_floor, n)
    return fn


def _fx_perm_extra_dart(n):
    def fn(game, player):
        player.perm_extra_darts += n
    return fn


def _fx_perm_shield(amount):
    def fn(game, player):
        player.perm_shield = min(0.9, player.perm_shield + amount)
    return fn

def _fx_bonus_for_single(n):
    """Следующий бросок в сингл даст на n очков больше."""
    def fn(game, player):
        player.single_bonus = getattr(player, 'single_bonus', 0) + n
    return fn
    
def _fx_flat_bonus_and_dart(bonus, darts):
    """Сразу +bonus очков и +darts дротиков в этом ходе."""
    def fn(game, player):
        player.total_score += bonus
        player.current_round_points += bonus
        player.extra_darts_bonus += darts
        player.darts_remaining += darts
        game.floating_texts.append((f"+{bonus} и +{darts} дрот.", player))
    return fn


def _fx_repeat_best_round():
    """Повторить очки за свой лучший ход (минимум 20)."""
    def fn(game, player):
        bonus = max(player.best_round, 20)
        player.total_score += bonus
        player.current_round_points += bonus
        game.floating_texts.append((f"+{bonus} (повтор)", player))
    return fn


def _fx_weaken_all_players(n):
    """Все соперники теряют по n очков."""
    def fn(game, player):
        for target in game.players:
            if target is player:
                continue
            loss = min(n, target.total_score)
            target.total_score -= loss
            game.floating_texts.append((f"-{loss}", target))
    return fn


def _fx_flat_income_forever(n):
    """+n очков дохода в начале каждого хода (permanent)."""
    def fn(game, player):
        player.perm_flat_per_turn += n
    return fn


def _fx_shield_forever(amount):
    """+amount% щита навсегда (permanent)."""
    def fn(game, player):
        player.perm_shield = min(0.9, player.perm_shield + amount)
    return fn


def _fx_multiplier_turn(mult):
    """Множитель очков только на этот ход."""
    def fn(game, player):
        player.turn_multiplier *= mult
    return fn


def _fx_extra_dart_forever(n):
    """+n дротиков каждый ход до конца игры (permanent)."""
    def fn(game, player):
        player.perm_extra_darts += n
    return fn

# ==========================================================================
# КАТАЛОГ УЛУЧШЕНИЙ (теперь 58 штук)
# ==========================================================================
UPGRADES = [
    # TIER 1 (существующие + новые)
    Upgrade("t1_extra_dart", "Доп. дротик", "Ещё +1 дротик в этом ходе", 1, "turn",
            C.SUCCESS, _fx_extra_dart(1)),
    Upgrade("t1_small_bonus", "Мелкая удача", "Сразу +10 очков", 1, "turn",
            C.ACCENT_2, _fx_flat_bonus(10)),
    Upgrade("t1_poke_leader", "Укол лидеру", "Лидер теряет 5 очков", 1, "turn",
            C.DANGER, _fx_weaken_leader(5)),
    Upgrade("t1_safety_net", "Страховка", "Промахи в этом ходе = 5 очков", 1, "turn",
            (120, 170, 255), _fx_miss_becomes(5)),
    Upgrade("t1_pickpocket", "Мелкий саботаж", "Случайный соперник получит на 1 дротик меньше", 1, "turn",
            C.DANGER, _fx_sabotage_dart(1)),
    Upgrade("t1_echo", "Эхо удачи", "Сразу получи очки, равные лучшему раунду (мин. 15)", 1, "turn",
            C.ACCENT_2, _fx_copy_best_round()),
    Upgrade("t1_steady_hand", "Твёрдая рука", "НАВСЕГДА: промахи = минимум 3 очка", 1, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(3)),
    Upgrade("t1_warmup", "Разминка", "НАВСЕГДА: +2 очка в начале каждого хода", 1, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(2)),
    Upgrade("t1_focus", "Концентрация", "НАВСЕГДА: очки +5% до конца партии", 1, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.05)),
    Upgrade("t1_thick_skin", "Толстая кожа", "НАВСЕГДА: -20% урона от краж и атак", 1, "permanent",
            (150, 200, 255), _fx_perm_shield(0.20)),
    Upgrade("t1_precision", "Точный прицел", "Следующий сингл даст +5 очков", 1, "turn",
            (150, 200, 255), _fx_bonus_for_single(5)),
    Upgrade("t1_quick_start", "Быстрый старт", "Сразу +3 очка и +1 дротик", 1, "turn",
            C.SUCCESS, _fx_flat_bonus_and_dart(3, 1)),
    Upgrade("t1_penny", "Копейка", "НАВСЕГДА: +1 очко дохода в начале хода", 1, "permanent",
            C.ACCENT_2, _fx_flat_income_forever(1)),
    Upgrade("t1_light_shield", "Лёгкий щит", "НАВСЕГДА: +10% защиты от краж", 1, "permanent",
            (150, 200, 255), _fx_shield_forever(0.10)),
    Upgrade("t1_kamikaze", "Камикадзе", "При промахе в этом ходе все соперники теряют по 3 очка", 1, "turn",
            C.DANGER, _fx_kamikaze()),
    Upgrade("t1_lottery", "Лотерея", "Всем игрокам +20 (лидеру +15)", 1, "turn",
            C.ACCENT_2, _fx_lottery()),
    Upgrade("t1_collector", "Коллекционер", "НАВСЕГДА: +3 очка за каждый бросок", 1, "permanent",
            C.ACCENT, _fx_collector()),

    # TIER 2
    Upgrade("t2_double_turn", "Двойной удар", "Все очки этого хода x2", 2, "turn",
            C.ACCENT, _fx_multiplier(2)),
    Upgrade("t2_steal", "Кража", "Забрать 10 очков у лидера", 2, "turn",
            C.DANGER, _fx_steal_from_leader(10)),
    Upgrade("t2_extra_dart2", "Второе дыхание", "Ещё +2 дротика в этом ходе", 2, "turn",
            C.SUCCESS, _fx_extra_dart(2)),
    Upgrade("t2_mid_bonus", "Джекпот-мини", "Сразу +25 очков", 2, "turn",
            C.ACCENT_2, _fx_flat_bonus(25)),
    Upgrade("t2_sabotage2", "Крупный саботаж", "Случайный соперник получит на 2 дротика меньше", 2, "turn",
            C.DANGER, _fx_sabotage_dart(2)),
    Upgrade("t2_double_darts", "Удвоение бросков", "Удвоить количество дротиков в этом ходе", 2, "turn",
            C.SUCCESS, _fx_double_darts_this_turn()),
    Upgrade("t2_nerves", "Стальные нервы", "НАВСЕГДА: промахи = минимум 8 очков", 2, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(8)),
    Upgrade("t2_mindset", "Постоянный настрой", "НАВСЕГДА: очки +12% до конца партии", 2, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.12)),
    Upgrade("t2_coach", "Личный тренер", "НАВСЕГДА: +5 очков в начале каждого хода", 2, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(5)),
    Upgrade("t2_shield", "Щит", "НАВСЕГДА: -50% урона от краж и атак", 2, "permanent",
            (150, 200, 255), _fx_perm_shield(0.30)),
    Upgrade("t2_repeat", "Повтор", "Повторить очки за свой лучший ход (мин. 20)", 2, "turn",
            C.ACCENT, _fx_repeat_best_round()),
    Upgrade("t2_weaken_all", "Волна", "Все соперники теряют по 5 очков", 2, "turn",
            C.DANGER, _fx_weaken_all_players(5)),
    Upgrade("t2_income_boost", "Подъём", "НАВСЕГДА: +8 очков дохода в начале хода", 2, "permanent",
            C.ACCENT_2, _fx_flat_income_forever(8)),
    Upgrade("t2_double_shield", "Двойной щит", "НАВСЕГДА: +20% защиты от краж", 2, "permanent",
            (150, 200, 255), _fx_shield_forever(0.20)),
    Upgrade("t2_curse", "Проклятие", "Следующий ход случайного соперника будет с x0.5", 2, "turn",
            C.DANGER, _fx_curse()),
    Upgrade("t2_steal_dart", "Кража дротика", "Украсть 1 дротик у лидера", 2, "turn",
            C.DANGER, _fx_steal_dart()),
    Upgrade("t2_double_first", "Двойной удар", "Первый бросок в этом ходе дублируется", 2, "turn",
            C.ACCENT, _fx_double_first_throw()),
    Upgrade("t2_mirror", "Зеркальный щит", "Если у тебя украдут очки, вор потеряет столько же", 2, "turn",
            (150, 200, 255), _fx_mirror_shield()),
    Upgrade("t2_immunity", "Невосприимчивость", "Защита от негативных эффектов на 2 хода", 2, "turn",
            C.SUCCESS, _fx_immunity()),
    Upgrade("t2_gravity", "Гравитация", "Синглы в этом ходе дают x1.6", 2, "turn",
            C.ACCENT_2, _fx_gravity()),

    # TIER 3
    Upgrade("t3_triple_turn", "Тройной удар", "Все очки этого хода x3!", 3, "turn",
            C.ACCENT, _fx_multiplier(3)),
    Upgrade("t3_jackpot", "ДЖЕКПОТ", "Сразу +40 очков!", 3, "turn",
            C.ACCENT_2, _fx_flat_bonus(40)),
    Upgrade("t3_crush_leader", "Разгром лидера", "Лидер теряет 20 очков", 3, "turn",
            C.DANGER, _fx_weaken_leader(20)),
    Upgrade("t3_big_steal", "Большая кража", "Забрать 25 очков у лидера", 3, "turn",
            C.DANGER, _fx_steal_from_leader(25)),
    Upgrade("t3_wreck", "Разгром рандома", "Случайный соперник теряет 15 очков", 3, "turn",
            C.DANGER, _fx_weaken_random_opponent(15)),
    Upgrade("t3_double_darts2", "Двойная перезарядка", "Удвоить оставшиеся дротики", 3, "turn",
            C.SUCCESS, _fx_double_darts_this_turn()),
    Upgrade("t3_legend", "Легенда дартса", "НАВСЕГДА: очки +25% до конца партии", 3, "permanent",
            C.ACCENT, _fx_perm_multiplier(1.25)),
    Upgrade("t3_lifetime_income", "Пожизненный доход", "НАВСЕГДА: +10 очков в начале каждого хода", 3, "permanent",
            C.ACCENT_2, _fx_perm_flat_income(10)),
    Upgrade("t3_sniper_perm", "Снайпер", "НАВСЕГДА: промахи = минимум 10 очков", 3, "permanent",
            (120, 170, 255), _fx_perm_miss_floor(10)),
    Upgrade("t3_extra_hand", "Третья рука", "НАВСЕГДА: +1 дротик каждый ход", 3, "permanent",
            C.SUCCESS, _fx_perm_extra_dart(1)),
    Upgrade("t3_mega_mult", "Сверхмножитель", "Все очки этого хода x3.5", 3, "turn",
            C.ACCENT, _fx_multiplier_turn(3.5)),
    Upgrade("t3_mega_income", "Олигарх", "НАВСЕГДА: +20 очков дохода в начале хода", 3, "permanent",
            C.ACCENT_2, _fx_flat_income_forever(20)),
    Upgrade("t3_berserk", "Берсерк", "НАВСЕГДА: +2 дротика каждый ход", 3, "permanent",
            C.SUCCESS, _fx_extra_dart_forever(2)),
    Upgrade("t3_armageddon", "Армагеддон", "Все соперники теряют по 15 очков", 3, "turn",
            C.DANGER, _fx_weaken_all_players(15)),
    Upgrade("t3_earthquake", "Землетрясение", "Все соперники теряют 10% счёта (мин. 5)", 3, "turn",
            C.DANGER, _fx_earthquake()),
    Upgrade("t3_casino", "Казино", "Множитель очков в этом ходе: 0.5, 1.5, 2 или 3", 3, "turn",
            C.ACCENT, _fx_casino_risky()),
    Upgrade("t3_snowball", "Снежный ком", "НАВСЕГДА: каждый следующий дротик в ходе даёт на 5% больше", 3, "permanent",
            C.ACCENT, _fx_snowball()),
    Upgrade("t3_gold_rush", "Золотая лихорадка", "НАВСЕГДА: если ход >50 очков, след. ход +5 пассивно", 3, "permanent",
            C.ACCENT_2, _fx_gold_rush()),
    Upgrade("t3_vampire", "Вампир", "НАВСЕГДА: если ход >60 очков, восстанавливает 1 дротик", 3, "permanent",
            C.DANGER, _fx_vampire()),
    Upgrade("t3_clone", "Клон", "+1 дротик, но множитель x0.5", 3, "turn",
            C.SUCCESS, _fx_clone()),
]

UPGRADES_BY_TIER = {1: [u for u in UPGRADES if u.tier == 1],
                     2: [u for u in UPGRADES if u.tier == 2],
                     3: [u for u in UPGRADES if u.tier == 3]}

TIER_EMOJI = {1: "🌱", 2: "⚡", 3: "💎"}
DURATION_LABEL = {"turn": "⏳ ЭТОТ ХОД", "permanent": "♾️ НАВСЕГДА"}
DURATION_COLOR = {"turn": C.TEXT_DIM, "permanent": C.ACCENT}


def roll_upgrade(round_no, total_rounds):
    progress = 0.0 if total_rounds <= 1 else (round_no - 1) / (total_rounds - 1)
    w1 = 70 - 60 * progress
    w2 = 25 + 10 * progress
    w3 = 5 + 50 * progress
    tier = random.choices([1, 2, 3], weights=[w1, w2, w3], k=1)[0]
    return random.choice(UPGRADES_BY_TIER[tier])


class UpgradeSpinner:
    DURATION_MS = 2200
    CARD_H = 106
    CARD_GAP = 14

    def __init__(self, result_upgrade: Upgrade, on_done=None):
        self.result = result_upgrade
        self.on_done = on_done
        self.start_ticks = pygame.time.get_ticks()
        self.done = False
        reel = [random.choice(UPGRADES) for _ in range(22)]
        reel.append(result_upgrade)
        self.reel = reel
        self.finished_hold = 0

    def update(self):
        if self.done:
            self.finished_hold += 1

    def progress(self):
        elapsed = pygame.time.get_ticks() - self.start_ticks
        t = min(1.0, elapsed / self.DURATION_MS)
        if t >= 1.0 and not self.done:
            self.done = True
            if self.on_done:
                self.on_done(self.result)
        return t

    @staticmethod
    def _ease_out_cubic(t):
        return 1 - (1 - t) ** 3

    def draw(self, surface, center_rect: pygame.Rect, font_title, font_desc, font_tag):
        t = self.progress()
        eased = self._ease_out_cubic(t)

        n = len(self.reel)
        total_h = n * (self.CARD_H + self.CARD_GAP)
        final_offset = total_h - (self.CARD_H + self.CARD_GAP) * 0.5 - center_rect.height / 2
        offset = eased * final_offset

        clip = surface.get_clip()
        surface.set_clip(center_rect)

        pygame.draw.rect(surface, C.PANEL_BG, center_rect, border_radius=18)
        pygame.draw.rect(surface, C.ACCENT, center_rect, 3, border_radius=18)

        y = center_rect.top - offset
        for card in self.reel:
            card_rect = pygame.Rect(center_rect.left + 16, int(y),
                                     center_rect.width - 32, self.CARD_H)
            if card_rect.bottom > center_rect.top - 20 and card_rect.top < center_rect.bottom + 20:
                self._draw_card(surface, card_rect, card, font_title, font_desc, font_tag)
            y += self.CARD_H + self.CARD_GAP

        fade_h = 60
        top_fade = pygame.Surface((center_rect.width, fade_h), pygame.SRCALPHA)
        top_fade.fill((*C.PANEL_BG, 235))
        surface.blit(top_fade, (center_rect.left, center_rect.top))
        bottom_fade = pygame.Surface((center_rect.width, fade_h), pygame.SRCALPHA)
        bottom_fade.fill((*C.PANEL_BG, 235))
        surface.blit(bottom_fade, (center_rect.left, center_rect.bottom - fade_h))

        mid_y = center_rect.centery
        pygame.draw.polygon(surface, C.ACCENT, [
            (center_rect.left - 4, mid_y - 14),
            (center_rect.left - 4, mid_y + 14),
            (center_rect.left + 14, mid_y),
        ])
        pygame.draw.polygon(surface, C.ACCENT, [
            (center_rect.right + 4, mid_y - 14),
            (center_rect.right + 4, mid_y + 14),
            (center_rect.right - 14, mid_y),
        ])

        surface.set_clip(clip)

    def _draw_card(self, surface, rect, card: Upgrade, font_title, font_desc, font_tag):
        pygame.draw.rect(surface, C.PANEL_BG_LIGHT, rect, border_radius=12)
        pygame.draw.rect(surface, card.color, rect, 3, border_radius=12)
        tier_tag = emoji_render.rtext(font_tag, f"{TIER_EMOJI.get(card.tier, '')} УРОВЕНЬ {card.tier}", card.color)
        surface.blit(tier_tag, (rect.left + 16, rect.top + 8))
        dur_label = DURATION_LABEL.get(card.duration, "")
        dur_color = DURATION_COLOR.get(card.duration, C.TEXT_DIM)
        dur_tag = emoji_render.rtext(font_tag, dur_label, dur_color)
        surface.blit(dur_tag, dur_tag.get_rect(topright=(rect.right - 14, rect.top + 8)))
        title = emoji_render.rtext(font_title, card.name, C.TEXT_MAIN)
        surface.blit(title, (rect.left + 16, rect.top + 32))
        desc = font_desc.render(card.desc, True, C.TEXT_DIM)
        surface.blit(desc, (rect.left + 16, rect.top + 66))
