# -*- coding: utf-8 -*-
"""
game.py — мозг игры: очередность ходов, начисление очков, режимы,
undo/skip, определение победителя.
"""

import config as C
from player import Player
from upgrades import roll_upgrade


class GameManager:
    def __init__(self, mode, player_names, team_of=None, dartboard=None):
        self.mode = mode
        self.info = C.MODE_INFO[mode]
        self.rounds_total = self.info.get("rounds", 0)
        self.teams_mode = self.info.get("teams", False)
        self.dartboard = dartboard

        # Для режима улучшений можно задать своё количество раундов
        if mode == C.MODE_UPGRADES and hasattr(C, 'custom_upgrade_rounds'):
            self.rounds_total = C.custom_upgrade_rounds
            self.info["rounds"] = C.custom_upgrade_rounds

        self.players = []
        for i, name in enumerate(player_names):
            team = team_of[i] if team_of else None
            color = C.TEAM_COLORS[team] if (self.teams_mode and team is not None) \
                else C.PLAYER_COLORS[i % len(C.PLAYER_COLORS)]
            p = Player(name, color, team=team, index=i)
            if mode == C.MODE_501:
                p.remaining_score = 501
                p.starting_score = 501
                p.total_score = 501
            self.players.append(p)

        self.turn_order = self._build_turn_order()
        self.turn_pointer = 0
        self.round_no = 1
        self.game_over = False
        self.winner_players = []
        self.winner_team = None

        self.undo_stack = []
        self.last_hits = []
        self.floating_texts = []
        self.awaiting_upgrade = False

        self._start_turn(first=True)

    def _build_turn_order(self):
        n = len(self.players)
        if not self.teams_mode:
            return list(range(n))
        by_team = {}
        for i, p in enumerate(self.players):
            by_team.setdefault(p.team, []).append(i)
        order = []
        max_len = max(len(v) for v in by_team.values())
        teams_sorted = sorted(by_team.keys())
        for k in range(max_len):
            for t in teams_sorted:
                if k < len(by_team[t]):
                    order.append(by_team[t][k])
        return order

    @property
    def current_player(self):
        return self.players[self.turn_order[self.turn_pointer]]

    @property
    def darts_per_turn_base(self):
        if self.mode == C.MODE_SPRINT6:
            return C.darts_for_round(self.mode, self.round_no)
        return C.DARTS_PER_TURN_DEFAULT

    def _start_turn(self, first=False):
        p = self.current_player

        # Проклятие
        if p.turn_multiplier_penalty != 1.0:
            p.turn_multiplier = p.perm_multiplier * p.turn_multiplier_penalty
            p.turn_multiplier_penalty = 1.0
        else:
            p.turn_multiplier = p.perm_multiplier

        # Невосприимчивость
        if p.negative_effect_immune > 0:
            p.negative_effect_immune -= 1

        # Вампир: если в прошлый ход >60, даём +1 дротик
        if p.vampire and p.pending_dart_bonus > 0:
            p.extra_darts_bonus += p.pending_dart_bonus
            p.pending_dart_bonus = 0

        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus - p.pending_dart_penalty
        p.darts_remaining = max(1, base)
        p.pending_dart_penalty = 0
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        p.miss_floor = p.perm_miss_floor
        p.single_bonus = 0
        p.snowball_step = 0
        p.first_throw_doubled = False
        p.mirror_shield = False
        p.kamikaze = False
        p.clone = False
        p.gravity = False
        p.current_round_points = 0
        self.last_hits = []

        # Пассивный доход
        if p.perm_flat_per_turn and self.mode != C.MODE_501:
            p.total_score += p.perm_flat_per_turn
            p.current_round_points += p.perm_flat_per_turn
            self.floating_texts.append((f"+{p.perm_flat_per_turn}", p))

        # Золотая лихорадка: если в прошлый ход было >50, +5 сейчас
        if p.gold_rush and p.last_turn_above_50:
            p.total_score += 5
            p.current_round_points += 5
            self.floating_texts.append(("+5 золото", p))
            p.last_turn_above_50 = False

        if self.mode == C.MODE_UPGRADES:
            self.awaiting_upgrade = True
        else:
            self.awaiting_upgrade = False

    def roll_upgrade_for_current(self):
        return roll_upgrade(self.round_no, self.rounds_total)

    def apply_upgrade(self, upgrade):
        p = self.current_player
        income_before = p.perm_flat_per_turn
        upgrade.apply(self, p)
        p.upgrades_collected.append((upgrade.name, upgrade.duration))

        if upgrade.duration == "permanent":
            p.turn_multiplier = p.perm_multiplier
            p.miss_floor = max(p.miss_floor, p.perm_miss_floor)
            income_delta = p.perm_flat_per_turn - income_before
            if income_delta > 0:
                p.total_score += income_delta
                p.current_round_points += income_delta
                self.floating_texts.append((f"+{income_delta}", p))

        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus
        p.darts_remaining = max(1, base)
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        self.awaiting_upgrade = False

    def snapshot(self):
        return {
            "players": [p.snapshot() for p in self.players],
            "turn_pointer": self.turn_pointer,
            "round_no": self.round_no,
            "game_over": self.game_over,
            "last_hits": list(self.last_hits),
            "awaiting_upgrade": self.awaiting_upgrade,
        }

    def _push_undo(self):
        self.undo_stack.append(self.snapshot())
        if len(self.undo_stack) > C.UNDO_STACK_LIMIT:
            self.undo_stack.pop(0)

    def can_undo(self):
        return len(self.undo_stack) > 0

    def undo(self):
        if not self.undo_stack:
            return
        snap = self.undo_stack.pop()
        for p, ps in zip(self.players, snap["players"]):
            p.restore(ps)
        self.turn_pointer = snap["turn_pointer"]
        self.round_no = snap["round_no"]
        self.game_over = snap["game_over"]
        self.last_hits = list(snap["last_hits"])
        self.awaiting_upgrade = snap["awaiting_upgrade"]
        self.winner_players = []
        self.winner_team = None

    def throw(self, pos):
        if self.game_over or self.awaiting_upgrade or not self.dartboard:
            return None
        p = self.current_player
        if p.darts_remaining <= 0:
            return None

        hit = self.dartboard.hit_test(pos)
        self._push_undo()

        if self.mode == C.MODE_CRICKET:
            self._handle_cricket_throw(p, hit, pos)
        elif self.mode == C.MODE_501:
            self._handle_501_throw(p, hit, pos)
        else:
            points = self._calculate_points(p, hit)
            p.total_score += points
            p.current_round_points += points
            p.register_throw(points, hit.ring)
            p.darts_remaining -= 1
            self.last_hits.append((pos, p.color))

            # Двойной удар (первый бросок дублируется)
            if p.first_throw_doubled and p.throws_count == 1:
                p.total_score += points
                p.current_round_points += points
                p.register_throw(points, hit.ring)
                self.floating_texts.append(("Дубль!", p))
                p.first_throw_doubled = False

            # Камикадзе: промах = соперники теряют по 3
            if p.kamikaze and hit.ring == "miss":
                for target in self.players:
                    if target is not p:
                        loss = min(3, target.total_score)
                        target.total_score -= loss
                        self.floating_texts.append((f"-{loss}", target))
                p.kamikaze = False

            # Снежный ком: каждый следующий дротик +5%
            if p.snowball:
                p.snowball_step += 1
                if p.snowball_step > 1:
                    p.turn_multiplier *= 1.05

            # Коллекционер: +3 очка за каждый бросок
            if p.collector > 0:
                p.total_score += p.collector
                p.current_round_points += p.collector
                self.floating_texts.append((f"+{p.collector}", p))

            if points != hit.points:
                self.floating_texts.append((f"+{points}", p))

        if p.darts_remaining <= 0:
            self._end_turn()

        return hit

    def _calculate_points(self, p, hit):
        """Возвращает очки за бросок с учётом всех множителей."""
        points = hit.points
        if hit.ring == "miss" and p.miss_floor > 0:
            points = p.miss_floor
        if hit.ring == "single" and p.single_bonus > 0:
            points += p.single_bonus
            p.single_bonus = 0
        if p.gravity and hit.ring == "single":
            points = int(points * 1.6)
        points = int(round(points * p.turn_multiplier))
        return points

    def _handle_cricket_throw(self, player, hit, pos):
        value = hit.value
        ring = hit.ring
        if ring in ("single", "double", "triple") and value in (15, 16, 17, 18, 19, 20):
            marks = 1 if ring == "single" else 2 if ring == "double" else 3
            self._add_cricket_marks(player, value, marks, hit.points)
        elif ring in ("bull", "outer_bull"):
            marks = 1 if ring == "outer_bull" else 2
            self._add_cricket_marks(player, 25, marks, hit.points)
        else:
            pass

        player.register_throw(hit.points, ring)
        player.darts_remaining -= 1
        self.last_hits.append((pos, player.color))

    def _add_cricket_marks(self, player, number, marks, points):
        if not player.cricket_closed[number]:
            player.cricket_marks[number] += marks
            if player.cricket_marks[number] >= 3:
                player.cricket_marks[number] = 3
                player.cricket_closed[number] = True
        else:
            player.total_score += points
            player.current_round_points += points
            self.floating_texts.append((f"+{points}", player))

    def _handle_501_throw(self, player, hit, pos):
        points = hit.points
        if hit.ring == "miss" and player.miss_floor > 0:
            points = player.miss_floor
        if hit.ring == "single" and player.single_bonus > 0:
            points += player.single_bonus
            player.single_bonus = 0

        player.remaining_score -= points
        if player.remaining_score < 0:
            player.remaining_score += points
            self.floating_texts.append(("Перебор!", player))
        elif player.remaining_score == 0:
            player.register_throw(points, hit.ring)
            player.darts_remaining -= 1
            self.last_hits.append((pos, player.color))
            self._finish_game()
            return
        else:
            player.register_throw(points, hit.ring)
            player.darts_remaining -= 1
            self.last_hits.append((pos, player.color))

        player.total_score = player.remaining_score

    def skip_turn(self):
        if self.game_over or self.awaiting_upgrade:
            return
        self._push_undo()
        p = self.current_player
        p.darts_remaining = 0
        self._end_turn()

    def _end_turn(self):
        p = self.current_player
        # Проверяем условия для золотой лихорадки и вампира
        if p.current_round_points > 50:
            p.last_turn_above_50 = True
        else:
            p.last_turn_above_50 = False
        if p.vampire and p.current_round_points > 60:
            p.pending_dart_bonus = 1
        else:
            p.pending_dart_bonus = 0

        p.finish_round()
        self.turn_pointer += 1
        if self.turn_pointer >= len(self.turn_order):
            self.turn_pointer = 0
            self.round_no += 1
            if self.mode == C.MODE_CRICKET and self.round_no > self.rounds_total:
                self._finish_game()
                return
            elif self.mode == C.MODE_501 and self.round_no > self.rounds_total:
                self._finish_game()
                return
            elif self.mode not in (C.MODE_CRICKET, C.MODE_501) and self.round_no > self.rounds_total:
                self._finish_game()
                return
        self._start_turn()

    def _finish_game(self):
        self.game_over = True
        if self.teams_mode:
            totals = {}
            for p in self.players:
                totals[p.team] = totals.get(p.team, 0) + p.total_score
            best = max(totals.values())
            self.winner_team = [t for t, v in totals.items() if v == best]
            self.winner_players = [p for p in self.players if p.team in self.winner_team]
        elif self.mode == C.MODE_CRICKET:
            best_closed = max(sum(p.cricket_closed.values()) for p in self.players)
            best_score = max(p.total_score for p in self.players
                             if sum(p.cricket_closed.values()) == best_closed)
            self.winner_players = [p for p in self.players
                                   if sum(p.cricket_closed.values()) == best_closed
                                   and p.total_score == best_score]
        elif self.mode == C.MODE_501:
            if any(p.remaining_score == 0 for p in self.players):
                self.winner_players = [p for p in self.players if p.remaining_score == 0]
            else:
                min_remaining = min(p.remaining_score for p in self.players)
                self.winner_players = [p for p in self.players if p.remaining_score == min_remaining]
        else:
            best = max(p.total_score for p in self.players)
            self.winner_players = [p for p in self.players if p.total_score == best]

    def team_totals(self):
        totals = {}
        for p in self.players:
            totals[p.team] = totals.get(p.team, 0) + p.total_score
        return totals

    def players_sorted(self):
        if self.mode == C.MODE_CRICKET:
            return sorted(self.players,
                          key=lambda p: (-sum(p.cricket_closed.values()), -p.total_score))
        elif self.mode == C.MODE_501:
            return sorted(self.players, key=lambda p: p.remaining_score)
        return sorted(self.players, key=lambda p: p.total_score, reverse=True)

    def darts_thrown_progress(self):
        p = self.current_player
        total = max(p.darts_total_this_turn, 1)
        thrown = total - p.darts_remaining
        return thrown, total
