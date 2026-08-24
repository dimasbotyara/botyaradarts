# -*- coding: utf-8 -*-
"""
game.py — «мозг» игры: очередность ходов, начисление очков, режимы,
undo/skip, определение победителя. Не знает ничего про pygame-рисование
(за исключением того, что хранит координаты точек попаданий для отрисовки
на мишени) — вся отрисовка в ui.py / main.py.
"""

import config as C
from player import Player
from upgrades import roll_upgrade


class GameManager:
    def __init__(self, mode, player_names, team_of=None, dartboard=None):
        """
        mode: одна из config.MODE_*
        player_names: список имён игроков по порядку хода
        team_of: список int (0/1) той же длины, что player_names, для режима "teams"; иначе None
        """
        self.mode = mode
        self.info = C.MODE_INFO[mode]
        self.rounds_total = self.info["rounds"]
        self.teams_mode = self.info["teams"]
        self.dartboard = dartboard

        self.players = []
        for i, name in enumerate(player_names):
            team = team_of[i] if team_of else None
            color = C.TEAM_COLORS[team] if (self.teams_mode and team is not None) \
                else C.PLAYER_COLORS[i % len(C.PLAYER_COLORS)]
            self.players.append(Player(name, color, team=team, index=i))

        self.turn_order = self._build_turn_order()
        self.turn_pointer = 0
        self.round_no = 1
        self.game_over = False
        self.winner_players = []
        self.winner_team = None

        self.undo_stack = []
        self.last_hits = []          # [(pos, color), ...] точки текущего хода
        self.floating_texts = []     # [(text, player), ...] для короткой анимации
        self.awaiting_upgrade = False  # True пока не применили улучшение и не начали ход

        self._start_turn(first=True)

    # ------------------------------------------------------------------
    def _build_turn_order(self):
        n = len(self.players)
        if not self.teams_mode:
            return list(range(n))
        # интерлив команд: T0p0, T1p0, T0p1, T1p1, ...
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
        return C.darts_for_round(self.mode, self.round_no)

    # ------------------------------------------------------------------
    def _start_turn(self, first=False):
        p = self.current_player
        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus - p.pending_dart_penalty
        p.darts_remaining = max(1, base)
        p.pending_dart_penalty = 0
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        p.turn_multiplier = p.perm_multiplier
        p.miss_floor = p.perm_miss_floor
        p.current_round_points = 0
        self.last_hits = []

        # пассивный доход очков от постоянных улучшений — начисляется
        # автоматически в начале каждого хода, до самих бросков
        if p.perm_flat_per_turn:
            p.total_score += p.perm_flat_per_turn
            p.current_round_points += p.perm_flat_per_turn
            self.floating_texts.append((f"+{p.perm_flat_per_turn}", p))

        if self.mode == C.MODE_UPGRADES:
            self.awaiting_upgrade = True
        else:
            self.awaiting_upgrade = False

    def roll_upgrade_for_current(self):
        """Вызывается UI перед началом хода в режиме 'С улучшениями'."""
        return roll_upgrade(self.round_no, self.rounds_total)

    def apply_upgrade(self, upgrade):
        p = self.current_player
        income_before = p.perm_flat_per_turn
        upgrade.apply(self, p)
        p.upgrades_collected.append((upgrade.name, upgrade.duration))

        # постоянные улучшения могли поднять perm_multiplier/perm_miss_floor/доход —
        # применяем их сразу к текущему ходу, т.к. игрок ещё не бросал дротики
        if upgrade.duration == "permanent":
            p.turn_multiplier = p.perm_multiplier
            p.miss_floor = max(p.miss_floor, p.perm_miss_floor)
            income_delta = p.perm_flat_per_turn - income_before
            if income_delta > 0:
                p.total_score += income_delta
                p.current_round_points += income_delta
                self.floating_texts.append((f"+{income_delta}", p))

        # применение улучшения могло изменить extra_darts_bonus/perm_extra_darts —
        # пересчитаем итоговое число дротиков на этот ход
        base = self.darts_per_turn_base + p.perm_extra_darts + p.extra_darts_bonus
        p.darts_remaining = max(1, base)
        p.extra_darts_bonus = 0
        p.darts_total_this_turn = p.darts_remaining
        self.awaiting_upgrade = False

    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    def throw(self, pos):
        """Бросок дротика мышкой по координате pos на мишени."""
        if self.game_over or self.awaiting_upgrade or not self.dartboard:
            return None
        p = self.current_player
        if p.darts_remaining <= 0:
            return None

        hit = self.dartboard.hit_test(pos)
        self._push_undo()

        points = hit.points
        if hit.ring == "miss" and p.miss_floor > 0:
            points = p.miss_floor
        points = int(round(points * p.turn_multiplier))

        p.total_score += points
        p.current_round_points += points
        p.register_throw(points, hit.ring)
        p.darts_remaining -= 1
        self.last_hits.append((pos, p.color))

        if points != hit.points:
            self.floating_texts.append((f"+{points}", p))

        if p.darts_remaining <= 0:
            self._end_turn()

        return hit

    def skip_turn(self):
        """Пропустить оставшиеся дротики текущего хода без начисления очков."""
        if self.game_over or self.awaiting_upgrade:
            return
        self._push_undo()
        p = self.current_player
        p.darts_remaining = 0
        self._end_turn()

    def _end_turn(self):
        p = self.current_player
        p.finish_round()
        self.turn_pointer += 1
        if self.turn_pointer >= len(self.turn_order):
            self.turn_pointer = 0
            self.round_no += 1
            if self.round_no > self.rounds_total:
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
        else:
            best = max(p.total_score for p in self.players)
            self.winner_players = [p for p in self.players if p.total_score == best]

    # ------------------------------------------------------------------
    def team_totals(self):
        """dict: team_index -> суммарный счёт (только для teams_mode)."""
        totals = {}
        for p in self.players:
            totals[p.team] = totals.get(p.team, 0) + p.total_score
        return totals

    def players_sorted(self):
        return sorted(self.players, key=lambda p: p.total_score, reverse=True)

    def darts_thrown_progress(self):
        """(брошено, всего) дротиков в текущем ходе — для UI."""
        p = self.current_player
        total = max(p.darts_total_this_turn, 1)
        thrown = total - p.darts_remaining
        return thrown, total
