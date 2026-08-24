# -*- coding: utf-8 -*-
"""
player.py — модель игрока и его статистики в рамках одной партии.
"""


class Player:
    def __init__(self, name, color, team=None, index=0):
        self.name = name
        self.color = color
        self.team = team          # None или индекс команды (0/1)
        self.index = index

        self.total_score = 0
        self.round_scores = []    # список очков за каждый завершённый раунд
        self.current_round_points = 0

        # состояние текущего хода (сбрасывается после хода)
        self.darts_remaining = 0
        self.darts_total_this_turn = 0  # сколько дротиков положено в этом ходе (для UI)
        self.turn_multiplier = 1        # эффект улучшений: множитель очков за ход
        self.extra_darts_bonus = 0      # эффект улучшений: доп. дротики
        self.miss_floor = 0             # эффект улучшений: промах засчитывается как N очков
        self.single_bonus = 0           # бонус к очкам за следующее попадание в сингл (одноразовый)

        # ПОСТОЯННЫЕ (пассивные) эффекты — действуют до конца всей партии,
        # накапливаются при выпадении улучшений с duration="permanent"
        self.perm_multiplier = 1.0      # постоянный множитель очков (стакается умножением)
        self.perm_extra_darts = 0       # доп. дротики каждый ход до конца игры
        self.perm_flat_per_turn = 0     # пассивный доход очков в начале каждого хода
        self.perm_miss_floor = 0        # промахи навсегда считаются как минимум N очков
        self.perm_shield = 0.0          # доля (0..0.9) снижения урона от краж/атак соперников
        self.pending_dart_penalty = 0   # временный "минус дротик" от чужой диверсии (на след. ход)

        # статистика на партию
        self.throws_count = 0
        self.miss_count = 0
        self.single_count = 0
        self.double_count = 0
        self.triple_count = 0
        self.bull_count = 0
        self.outer_bull_count = 0
        self.best_single_throw = 0
        self.best_round = 0
        self.upgrades_collected = []    # список (name, duration) — для истории партии

    def register_throw(self, hit_points, ring):
        self.throws_count += 1
        if ring == "miss":
            self.miss_count += 1
        elif ring == "single":
            self.single_count += 1
        elif ring == "double":
            self.double_count += 1
        elif ring == "triple":
            self.triple_count += 1
        elif ring == "bull":
            self.bull_count += 1
        elif ring == "outer_bull":
            self.outer_bull_count += 1
        if hit_points > self.best_single_throw:
            self.best_single_throw = hit_points

    def finish_round(self):
        self.round_scores.append(self.current_round_points)
        if self.current_round_points > self.best_round:
            self.best_round = self.current_round_points
        self.current_round_points = 0

    @property
    def average_per_dart(self):
        if self.throws_count == 0:
            return 0.0
        return self.total_score / self.throws_count

    @property
    def accuracy_percent(self):
        if self.throws_count == 0:
            return 0.0
        hits = self.throws_count - self.miss_count
        return 100.0 * hits / self.throws_count

    def snapshot(self):
        """Лёгкий словарь-снимок для undo (без ссылок на изменяемые вложенные списки)."""
        return {
            "total_score": self.total_score,
            "round_scores": list(self.round_scores),
            "current_round_points": self.current_round_points,
            "darts_remaining": self.darts_remaining,
            "darts_total_this_turn": self.darts_total_this_turn,
            "turn_multiplier": self.turn_multiplier,
            "extra_darts_bonus": self.extra_darts_bonus,
            "miss_floor": self.miss_floor,
            "single_bonus": self.single_bonus,   # новое поле
            "perm_multiplier": self.perm_multiplier,
            "perm_extra_darts": self.perm_extra_darts,
            "perm_flat_per_turn": self.perm_flat_per_turn,
            "perm_miss_floor": self.perm_miss_floor,
            "perm_shield": self.perm_shield,
            "pending_dart_penalty": self.pending_dart_penalty,
            "throws_count": self.throws_count,
            "miss_count": self.miss_count,
            "single_count": self.single_count,
            "double_count": self.double_count,
            "triple_count": self.triple_count,
            "bull_count": self.bull_count,
            "outer_bull_count": self.outer_bull_count,
            "best_single_throw": self.best_single_throw,
            "best_round": self.best_round,
            "upgrades_collected": list(self.upgrades_collected),
        }

    def restore(self, snap):
        self.total_score = snap["total_score"]
        self.round_scores = list(snap["round_scores"])
        self.current_round_points = snap["current_round_points"]
        self.darts_remaining = snap["darts_remaining"]
        self.darts_total_this_turn = snap.get("darts_total_this_turn", self.darts_remaining)
        self.turn_multiplier = snap["turn_multiplier"]
        self.extra_darts_bonus = snap["extra_darts_bonus"]
        self.miss_floor = snap.get("miss_floor", 0)
        self.single_bonus = snap.get("single_bonus", 0)   # новое поле
        self.perm_multiplier = snap.get("perm_multiplier", 1.0)
        self.perm_extra_darts = snap.get("perm_extra_darts", 0)
        self.perm_flat_per_turn = snap.get("perm_flat_per_turn", 0)
        self.perm_miss_floor = snap.get("perm_miss_floor", 0)
        self.perm_shield = snap.get("perm_shield", 0.0)
        self.pending_dart_penalty = snap.get("pending_dart_penalty", 0)
        self.throws_count = snap["throws_count"]
        self.miss_count = snap["miss_count"]
        self.single_count = snap["single_count"]
        self.double_count = snap["double_count"]
        self.triple_count = snap["triple_count"]
        self.bull_count = snap["bull_count"]
        self.outer_bull_count = snap["outer_bull_count"]
        self.best_single_throw = snap["best_single_throw"]
        self.best_round = snap["best_round"]
        self.upgrades_collected = list(snap["upgrades_collected"])
