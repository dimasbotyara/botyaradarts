# player.py

class Player:
    def __init__(self, name, color, team=None, index=0):
        self.name = name
        self.color = color
        self.team = team
        self.index = index

        self.total_score = 0
        self.round_scores = []
        self.current_round_points = 0

        # Состояние текущего хода
        self.darts_remaining = 0
        self.darts_total_this_turn = 0
        self.turn_multiplier = 1
        self.extra_darts_bonus = 0
        self.miss_floor = 0
        self.single_bonus = 0

        # Постоянные эффекты
        self.perm_multiplier = 1.0
        self.perm_extra_darts = 0
        self.perm_flat_per_turn = 0
        self.perm_miss_floor = 0
        self.perm_shield = 0.0
        self.pending_dart_penalty = 0

        # Новые поля
        self.turn_multiplier_penalty = 1.0
        self.negative_effect_immune = 0
        self.first_throw_doubled = False
        self.mirror_shield = False
        self.kamikaze = False
        self.snowball = False
        self.snowball_step = 0
        self.collector = 0
        self.gold_rush = False
        self.vampire = False
        self.clone = False
        self.gravity = False
        self.pending_dart_bonus = 0       # вампир
        self.last_turn_above_50 = False   # золотая лихорадка

        # Статистика
        self.throws_count = 0
        self.miss_count = 0
        self.single_count = 0
        self.double_count = 0
        self.triple_count = 0
        self.bull_count = 0
        self.outer_bull_count = 0
        self.best_single_throw = 0
        self.best_round = 0
        self.upgrades_collected = []

        # Cricket
        self.cricket_marks = {num: 0 for num in [15, 16, 17, 18, 19, 20, 25]}
        self.cricket_closed = {num: False for num in [15, 16, 17, 18, 19, 20, 25]}

        # 501
        self.remaining_score = 501
        self.starting_score = 501

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
        return {
            "total_score": self.total_score,
            "round_scores": list(self.round_scores),
            "current_round_points": self.current_round_points,
            "darts_remaining": self.darts_remaining,
            "darts_total_this_turn": self.darts_total_this_turn,
            "turn_multiplier": self.turn_multiplier,
            "extra_darts_bonus": self.extra_darts_bonus,
            "miss_floor": self.miss_floor,
            "single_bonus": self.single_bonus,
            "perm_multiplier": self.perm_multiplier,
            "perm_extra_darts": self.perm_extra_darts,
            "perm_flat_per_turn": self.perm_flat_per_turn,
            "perm_miss_floor": self.perm_miss_floor,
            "perm_shield": self.perm_shield,
            "pending_dart_penalty": self.pending_dart_penalty,
            "turn_multiplier_penalty": self.turn_multiplier_penalty,
            "negative_effect_immune": self.negative_effect_immune,
            "first_throw_doubled": self.first_throw_doubled,
            "mirror_shield": self.mirror_shield,
            "kamikaze": self.kamikaze,
            "snowball": self.snowball,
            "snowball_step": self.snowball_step,
            "collector": self.collector,
            "gold_rush": self.gold_rush,
            "vampire": self.vampire,
            "clone": self.clone,
            "gravity": self.gravity,
            "pending_dart_bonus": self.pending_dart_bonus,
            "last_turn_above_50": self.last_turn_above_50,
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
            "cricket_marks": dict(self.cricket_marks),
            "cricket_closed": dict(self.cricket_closed),
            "remaining_score": self.remaining_score,
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
        self.single_bonus = snap.get("single_bonus", 0)
        self.perm_multiplier = snap.get("perm_multiplier", 1.0)
        self.perm_extra_darts = snap.get("perm_extra_darts", 0)
        self.perm_flat_per_turn = snap.get("perm_flat_per_turn", 0)
        self.perm_miss_floor = snap.get("perm_miss_floor", 0)
        self.perm_shield = snap.get("perm_shield", 0.0)
        self.pending_dart_penalty = snap.get("pending_dart_penalty", 0)
        self.turn_multiplier_penalty = snap.get("turn_multiplier_penalty", 1.0)
        self.negative_effect_immune = snap.get("negative_effect_immune", 0)
        self.first_throw_doubled = snap.get("first_throw_doubled", False)
        self.mirror_shield = snap.get("mirror_shield", False)
        self.kamikaze = snap.get("kamikaze", False)
        self.snowball = snap.get("snowball", False)
        self.snowball_step = snap.get("snowball_step", 0)
        self.collector = snap.get("collector", 0)
        self.gold_rush = snap.get("gold_rush", False)
        self.vampire = snap.get("vampire", False)
        self.clone = snap.get("clone", False)
        self.gravity = snap.get("gravity", False)
        self.pending_dart_bonus = snap.get("pending_dart_bonus", 0)
        self.last_turn_above_50 = snap.get("last_turn_above_50", False)
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
        self.cricket_marks = dict(snap.get("cricket_marks", {}))
        self.cricket_closed = dict(snap.get("cricket_closed", {}))
        self.remaining_score = snap.get("remaining_score", self.remaining_score)
