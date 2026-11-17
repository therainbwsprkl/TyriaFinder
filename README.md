# Tyria Finder

Current version: **v1.11.0** — signature `FIND` (`0x46494E44`), updates via GitHub releases.

A Nexus addon for Guild Wars 2. Find anything in Tyria and copy its chat link with one click.

Press **Alt+Shift+W** (or the gold pin in the Nexus QuickAccess bar) to open the search window. Type a place, resource, boss, event, or region, click a result, and its `[&...]` chat code is copied to your clipboard — paste it in game chat with Ctrl+V.

## What it finds

- **3,773 entries** from the official Guild Wars 2 API: 983 waypoints, 2,237 points of interest, and 553 vistas, across 169 maps
- **335 keyword-tagged entries** (2,761 phrases), so you can search by what you're looking for, not just by name:
  - Gathering and materials — flax, quartz, rich orichalcum, poultry, moa, skelk, and more
  - World bosses, metas, dungeons, raids, strikes, and event timers
  - Jumping puzzles (67), adventures, mini dungeons (22/22), and collections
  - Services — Mystic Forge, Trading Post, bank, crafting stations, merchants, laurel merchants
  - Guild missions (Rush, Challenge, Puzzle) and mount races
  - Regions and expansion maps
    
Results are sorted with same-map results first, so the closest match to where you are shows up at the top.

## Daily info

When the search box is empty, the window shows three sections:

- **Daily Pact Supply Network Agents** — today's 6 agents, in order, with a **Copy daily list** button that copies all 6 chat codes as one line (71 characters, fits in chat). Locations change at 08:00 UTC / 00:00 PST. Search `daily psna` or `psna tuesday` for a specific day.
- **Map Bonus Rewards — Week N** — the top 5 Central Tyria maps for the current week, ranked by the value of their bonus track. Click a row to copy its entry waypoint. The week is computed from the date (rotates Thursdays at 20:00 UTC, 8-week cycle). 
- **Rifts This Week** — the 3 rotating rift maps for the current week (11-week cycle), plus the 11 always-available rift maps grouped by type. Rifts spawn randomly on each map, so use your Scan for Rift keybind once you're there.

## Install

This addon is not in the Nexus Library yet. To install it manually:

1. Download `TyriaFinder.dll` from the [latest release](https://github.com/therainbwsprkl/TyriaFinder/releases/latest).
2. Copy it — just the one file — into `<Guild Wars 2>\addons\`.
3. Launch the game, open Nexus with Ctrl+O, and enable **Tyria Finder** under Installed.
4. Press Alt+Shift+W to open it.

To update, replace the DLL with the new version. Don't run two copies at once — remove the old DLL first.

## Building from source

Requires CMake and a C++17 compiler.

**On Linux (cross-compile for Windows with MinGW):**

```sh
sudo apt install cmake g++-mingw-w64-x86-64
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-x86_64.cmake
cmake --build build --config Release
```

The DLL is at `build/TyriaFinder.dll`. It is statically linked, so it loads on a plain Windows PC with no MinGW installed.

**On Windows (MSVC):**

```sh
cmake -S . -B build
cmake --build build --config Release
```

## How it works

- The dataset (`data/pois.json`) comes from the official Guild Wars 2 API. Tags live in `data/tags.json` and are merged into the dataset with `tools/apply_tags.py` — a tag can only attach to a place that already exists in the API data, it can never invent a waypoint.
- Search is offline and runs entirely in the addon. There are no network calls and no game-memory access — the only live data is your current map and position, read through MumbleLink, which is how the same-map sorting works.
- Run `python3 tools/test_search.py` to check the search against the dataset (186 cases).

e Nexus API are bundled under `third_party/` with their own licenses.
