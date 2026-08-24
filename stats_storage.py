# -*- coding: utf-8 -*-
"""
stats_storage.py — простая персистентная статистика игроков между запусками
игры. Хранится в JSON-файле рядом со скриптом (darts_stats.json).
"""

import json
import os
import config as C


def _empty_db():
    return {"players": {}, "games_played": 0}


def load_db():
    if not os.path.exists(C.STATS_FILE):
        return _empty_db()
    try:
        with open(C.STATS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "players" not in data:
            return _empty_db()
        return data
    except (json.JSONDecodeError, OSError):
        return _empty_db()


def save_db(db):
    try:
        with open(C.STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # если нет прав на запись — молча пропускаем, игра не должна падать


def record_game(game_manager):
    """Сохраняет результаты завершённой партии в базу статистики."""
    db = load_db()
    db["games_played"] = db.get("games_played", 0) + 1
    is_winner_ids = {id(p) for p in game_manager.winner_players}

    for p in game_manager.players:
        entry = db["players"].setdefault(p.name, {
            "games": 0, "wins": 0, "total_points": 0, "total_throws": 0,
            "best_round_ever": 0, "best_single_ever": 0,
            "bulls": 0, "triples": 0, "doubles": 0,
        })
        entry["games"] += 1
        if id(p) in is_winner_ids:
            entry["wins"] += 1
        entry["total_points"] += p.total_score
        entry["total_throws"] += p.throws_count
        entry["best_round_ever"] = max(entry["best_round_ever"], p.best_round)
        entry["best_single_ever"] = max(entry["best_single_ever"], p.best_single_throw)
        entry["bulls"] += p.bull_count
        entry["triples"] += p.triple_count
        entry["doubles"] += p.double_count

    save_db(db)
    return db


def leaderboard(db=None, limit=10):
    """Топ игроков по среднему очков за дротик (минимум 1 партия)."""
    db = db or load_db()
    rows = []
    for name, e in db["players"].items():
        avg = e["total_points"] / e["total_throws"] if e["total_throws"] else 0
        winrate = 100.0 * e["wins"] / e["games"] if e["games"] else 0
        rows.append({
            "name": name, "games": e["games"], "wins": e["wins"],
            "avg": avg, "winrate": winrate,
            "best_round": e["best_round_ever"], "best_single": e["best_single_ever"],
        })
    rows.sort(key=lambda r: r["avg"], reverse=True)
    return rows[:limit]
