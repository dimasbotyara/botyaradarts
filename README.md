# 🎯 Darts — Home Scoreboard

A full-featured Pygame application for keeping score in darts with a large, "TV-friendly" interface. Connect your laptop to a TV, go fullscreen (`F11`), and play with friends by clicking on the dartboard instead of typing numbers manually.

## Installation & Launch

```bash
pip install -r requirements.txt
python app.py
```

Requires Python 3.9+ and `pygame >= 2.1`. Pillow is needed for colored emoji in the UI (see the Emoji section below). Without it, the game still works fine — emoji will be neatly removed from texts instead of being shown as ugly square placeholders.

## 🎮 Controls

- **Mouse click on the dartboard** — throw a dart (zones: single, triple, double, bull 25, bullseye 50).
- **F11** — toggle fullscreen (great for TV projection).
- **Esc** — exit fullscreen / quit from main menu.
- On-screen buttons: **New Game**, **Undo** (works for multiple throws in a row), **Skip Turn**.

## 🎯 Game Modes

| Mode | Rules |
|---|---|
| **Classic** | 2–8 players, 3 darts per turn, 8 rounds. Highest total score wins. |
| **Teams** | Two teams (2–8 players), alternating turns, team scores are summed. |
| **Sprint 6×6** | 6 rounds with progressive difficulty: rounds 1–2 — 1 dart per turn, 3–4 — 2 darts, 5–6 — 3 darts. |
| **Upgrades** | 7 rounds. Before each turn, a slot-machine animation picks a random upgrade. Effects can be **temporary** (extra darts, score multipliers, stealing points, opponent sabotage) or **permanent** (passive multipliers, extra dart each turn, passive income, shield). 42 different upgrades across 3 tiers — the further into the game, the more powerful they become. |
| **Cricket** | Close numbers 15–20 and the bull. Once closed, subsequent hits score points until opponents close them too. 15 rounds. |
| **501** | Start at 501 and subtract points each dart. Bust (going below 0) cancels the turn. First to reach exactly 0 wins. 20 rounds. |

Rules are “home-style” — no complicated official finish rules (double-out, checkout). Just score points and have fun!

## 🎨 Themes & Customization

The game supports **separate UI themes** and **dartboard themes**:

- UI themes: custom (default), dark, light, Catppuccin Mocha/Latte, Dracula, Nord, Gruvbox Dark, Solarized Dark/Light, One Dark.
- Board themes: custom, classic, inverted, neon, wood.
- **Board rotation**: choose which sector is at the top — **6** or **20** (custom default: 6 on top).

All settings are stored in `darts_settings.json` and can be changed in **Settings** (⚙️) from the main menu.

## 📊 Statistics

After each game, results are saved to `darts_stats.json`. The main menu has a **📊 Player Statistics** button showing leaderboards by average points per dart, win rate, best round, and best single throw.

## ✨ Visual Effects

Each hit spawns particles and a pulsing ring at the impact point. Color depends on the zone (bull — red/gold, triple — gold, double — teal). Bullseye and triples add a screen flash and floating callouts ("BULL! 50", "TRIPLE 20!") with a pop animation. Big turns trigger special callouts: "🔥 MAXIMUM!" (150+ points) or "⚡ ON FIRE!" (100+). Buttons ripple on click, current player panel glows softly. Victory screen features confetti in winner colors.

All effects live in `fx.py` — easy to tweak without touching game logic.

## 😀 Emoji Rendering

Pygame itself cannot render colored emoji. The project includes `emoji_render.py` which uses Pillow and system color emoji fonts (e.g., `NotoColorEmoji.ttf` on Linux, `Apple Color Emoji` on macOS, `Segoe UI Emoji` on Windows) to display them properly. If no suitable font is found, it silently falls back to removing emoji from text — no crashes, no ugly squares.

## 📁 Project Structure

```
app.py               — main application class and game loop
screens/             — menu, setup, game, end, leaderboard, settings screens
config.py            — constants, themes, mode rules
dartboard.py         — dartboard rendering and hit detection
player.py            — player model and statistics
game.py              — turn order, scoring, undo, game modes, winner
upgrades.py          — upgrade definitions and slot-machine animation
fx.py                — visual effects (particles, flashes, callouts, confetti)
emoji_render.py      — colored emoji rendering via Pillow
ui.py                — buttons, inputs, panels, scoreboard
stats_storage.py     — persistent JSON statistics
```

## 🖥️ Screen Customization

In `config.py` (or via in-game Settings):

- `DEFAULT_WIDTH` / `DEFAULT_HEIGHT` — starting window size.
- `BOARD_PANEL_RATIO` — portion of the screen occupied by the dartboard (default 0.42).
- `MODE_INFO[...]["rounds"]` — number of rounds per mode.
- UI/board themes — see `UI_THEMES` and `BOARD_THEMES` dictionaries.

## 🚀 Launch Scripts

For convenience, launch scripts are included:

- **Windows CMD**: `run.bat`
- **Windows PowerShell**: `run.ps1`
- **Linux/macOS**: `run.sh`

They automatically activate the `.venv` if present, then run `app.py`. If no `.venv` is found, they print bilingual instructions (RU/EN) on how to create it.

Enjoy the game! 🔥🎯
