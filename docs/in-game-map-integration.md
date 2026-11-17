# In-game map integration — research note

Date: 2026-11-17. Addon: GW2 Waypoint Search v2.0 (Nexus API v6, C++, ImGui 1.80,
MumbleLink). Question from Audrey: "is there any way to integrate this better
into the ingame map?" Research only — no code changed, no DLL rebuilt.

## Short answer

**You cannot inject markers *into* the game's own world-map UI.** There is no
Nexus API, no official GW2 API, and no MumbleLink field for it. **You *can*
draw markers *on top of* the game's world map** — that is exactly what TacO,
Blish HUD Pathing, and TaimiHUD already do, and it is the realistic route for
this addon. It uses only data the game already publishes via MumbleLink, so
it stays inside the addon's existing no-memory-reads rule.

## What the APIs actually expose

### Nexus API v6 (`third_party/nexus/Nexus.h`) — no map API at all

- `NexusLinkData_t`: only screen `Width` / `Height`, UI `Scaling`,
  `IsMoving`, `IsCameraMoving`, `IsGameplay`. No map-open flag, no map
  rectangle, no map zoom/centre, no marker injection.
- `EGameBinds` includes map binds: `GB_MapToggle` (59), `GB_MapFocusPlayer`
  (60), `GB_MapFloorDown/Up` (61/62), `GB_MapZoomIn/Out` (63/64). Nexus can
  press them via `GameBinds_PressAsync` / `GameBinds_InvokeAsync` — i.e. it
  can *open* the map and zoom it, but it cannot centre it on an arbitrary
  point or set a pin.
- Rendering: `GUI_Register(RT_PreRender / RT_Render / RT_PostRender, …)`.
  ImGui drawn in `RT_Render` sits on top of the whole game frame, including
  the world map when it is open. That is the overlay surface.
- `WndProc_SendToGameOnly` and `MinHook_Create` exist in the API, but using
  them to synthesise clicks or hook the game's map code is input
  injection / reverse-engineering (see "Not possible", below).
- Important gotcha in the current code: both `AddonRender()` in
  `src/entry.cpp` and `MapView_Render()` in `src/map_view.cpp` return early
  when `!NexusLink->IsGameplay`. Whether `IsGameplay` goes false while the
  M-key map is open is **unverified** — an overlay that only renders when
  the map is open must be exempted from that gate (or the gate's behaviour
  with the map open must be checked in-world first).

### MumbleLink (`third_party/mumble/Mumble.h`) — the data that makes an overlay possible

`Mumble::Context` already has everything needed to project a waypoint onto
the screen, and this addon already reads part of it
(`Compass.PlayerPosition` for same-map sorting):

- `IsMapOpen : 1` — bit 0 of the UI-state flags. Tells you the world map
  is open. (Also in `docs.rs` `UIState::IS_MAP_OPEN`.)
- `Compass.Width / Height` (uint16, pixels), `Compass.Rotation` (radians),
  `Compass.PlayerPosition` (continent coords), `Compass.Center`
  (continent coords of the map centre), `Compass.Scale` (float).
- `Context.MapID`, `MapType`, `IsCompassTopRight`, `IsCompassRotating`.

This is the same data TacO started using in October 2019, when ArenaNet
added minimap info to MumbleLink: "The minimap's location, panning and
rotation is automatically tracked, and all the markers can be displayed on
there as well" and "The minimap and world map can now display markers and
trails for the current map" (gw2taco.com, Oct 2019). Blish HUD Pathing has
the same model: markers are by default visible "on the minimap (compass),
fullscreen map, and in-game", controlled per-category by
`miniMapVisibility` / `mapVisibility` / `inGameVisibility`, with
`mapDisplaySize` and `scaleonmapwithzoom` (gw2pathing.com, Visibility /
MapDisplaySize docs). Blish's advanced settings even mention tracking the
camera animation on map open/close so fullscreen-map elements hide at the
right moment ("map-trigger-hide-from-camera").

**Unverified from docs alone, needs an in-world check:** the exact
semantics of `Compass.Center` / `Scale` / `Width` / `Height` when the
*fullscreen* map (rather than the minimap) is open — whether they switch
to the fullscreen map's geometry, what the screen centre of the map is,
and the units of `Scale` (pixels per continent unit, presumably, but
unconfirmed). The projection below is therefore stated as a hypothesis
to calibrate, not as proven.

## Ranked options

### 1. Screen-space ImGui overlay on the game's fullscreen map — RECOMMENDED

**Feasibility: possible, low risk, medium work.**

- When `IsMapOpen` is true, draw the dataset's markers (waypoints / POIs /
  vistas, same filters as search, capped per frame as the tile map already
  is) as ImGui shapes in `RT_Render`, on top of the game's map. No
  injection into the game's UI, no new memory reads — only MumbleLink,
  which the addon already uses.
- Projection (to calibrate in-world):
  `screen = map_screen_centre + R(Rotation) * (poi_continent - Compass.Center) * Compass.Scale`
  where `map_screen_centre` is the on-screen centre of the open map
  (approx. `NexusLink.Width/2, Height/2` for the fullscreen map, to be
  verified), `R` is the compass rotation (likely 0 / north-up on the
  fullscreen map; it matters on the minimap), and `poi_continent` is the
  `(x, y)` already in `data/pois.json`. Only draw markers on the current
  continent and within the visible rect; hide when the map closes
  (Blish fades markers while in map view / on close for the same reason).
- Clicks: put an invisible ImGui button over each marker. Clicking copies
  its `[&...]` chat link (same as search / tile map). ImGui captures the
  click, so it should not also click through to the game's map underneath
  — but click-through / pass-through behaviour must be tested in-world,
  and markers must not block normal map panning/zooming when you miss
  them.
- Risks: calibration (if `Center`/`Scale` semantics differ from the
  hypothesis, markers will be offset — same class of problem as the v2.0
  tile-math calibration, fixable with one constant / one formula tweak);
  the `IsGameplay` gate noted above; floor handling (MumbleLink gives no
  floor, so markers from other floors of the same map will plot at their
  floor-1 continent coords, as in the v2.0 tile map); clutter at
  continent zoom (cap + filter, as the tile map does).
- Work: one new file (e.g. `src/map_overlay.cpp`), reuse `pois_data.h`
  and the existing copy-to-clipboard code, a toggle in Options, and an
  in-world calibration pass. No tile downloads, no new dataset.

### 2. Same projection on the minimap / compass — POSSIBLE, HARDER

Same maths as option 1, same MumbleLink fields, but the minimap's screen
rectangle is not exposed anywhere: its position (bottom-right by default,
top-right if `IsCompassTopRight`), size (`Compass.Width/Height` in
pixels, times UI scale), and rotation must be inferred from
`NexusLink.Width/Height/Scaling`. It is also small, so markers clutter
fast and are hard to click. TacO/Blish do it, so it is proven possible —
but it is fiddlier than the fullscreen map and less useful for Audrey's
use (finding a waypoint to go to), so it ranks below option 1. Do it
after option 1, reusing the same projection code.

### 3. One-click "open the game's map at this waypoint" — PARTIAL ONLY

- What works today: copy `[&...]`, paste in chat (Ctrl+V), send, click
  the link — the game opens its map centred on that point. That is the
  game's own behaviour and needs no addon.
- What Nexus can add: `GameBinds_PressAsync(GB_MapToggle)` can open the
  map programmatically, and `GB_MapFocusPlayer` / `GB_MapZoomIn/Out`
  can move it — but there is **no bind or API to centre the map on an
  arbitrary waypoint**, and no way to hand the game a chat link except
  through the chat box.
- Automating the paste-and-click (synthesising keystrokes / mouse
  events via `WndProc_SendToGameOnly`) would be gameplay automation:
  fragile (needs chat focus, Enter, then a click on the link at the
  right moment) and a ToS risk. **Not recommended.** Keep the manual
  copy → paste → click flow, and make option 1 the thing that removes
  the need for it.

### 4. Export the dataset as a .taco pack for TaimiHUD / Blish / TacO — POSSIBLE, LOW RISK, NO NEXUS CODE

- TacO/Blish/Taimi marker packs already show markers on the fullscreen
  map, minimap, and in-game by default (`mapVisibility` /
  `miniMapVisibility` / `inGameVisibility` = 1). Exporting
  `data/pois.json` (+ tags) as a `.taco` would make Audrey's waypoints
  appear on the game's map *inside TaimiHUD*, which she already runs.
- Catch: TacO markers use per-map in-game coordinates
  (`map_id` + x/y/z), not continent coords, so each entry must be
  converted via `/v2/maps` (`map_rect` / `continent_rect`) — a
  data-generation job, not a guess. Also: TaimiHUD does not run Lua, so
  no scripted behaviour; and Taimi's own Data Sources tab is currently
  buggy for some packs (see the addon's earlier TaimiHUD issue #46
  notes), though a manually copied `.taco` works for Pathing packs.
- This is the best *interim* route if option 1 stalls, and it
  complements it rather than replacing it. It does not need a DLL
  change at all.

### 5. Set the game's personal waypoint pin programmatically — NOT POSSIBLE (legitimately)

- The personal waypoint is set by the player with Alt+click on the
  map/minimap (Shift+click pings, Shift+click on a waypoint inserts its
  chat link). There is no Nexus, MumbleLink, or official API call to
  set it, read it, or move it.
- Simulating Alt+click at projected screen coordinates would be input
  injection (see option 3). **Do not do it.**

### 6. Hook the game's map rendering / read game memory for map state — NOT POSSIBLE SAFELY

- Nexus exposes `MinHook_Create`, and some addons do read game memory
  (e.g. Reffect states openly that it does), but hooking the game's map
  UI to inject markers would be reverse-engineering the client: it
  breaks on every game patch, risks crashes, and is the far side of
  ArenaNet's third-party policy from the MumbleLink-only approach this
  addon uses. It also violates the project's own standing rule (no
  game-memory reads except MumbleLink / Nexus APIs). **Do not do it.**

### 7. Make the addon's own tile map feel more like the game map — CHEAP COMPLEMENT

- No projection calibration needed: when `IsMapOpen` becomes true,
  auto-show the v2.0 tile map and sync its centre/zoom to
  `Compass.Center` / `Compass.Scale` (converted to the tile map's
  zoom). It is still a separate window, not on the game's map, but it
  removes the "press M, then press Alt+Shift+M" double step. Small
  work, low risk, and a useful fallback if option 1's screen projection
  proves fiddly in-world.

## Recommended next step

1. **Calibration first (small, safe, no DLL ship):** add temporary
   logging to a debug build that records, once a second,
   `IsMapOpen`, `Compass.Width/Height/Rotation/Center/Scale`,
   `PlayerPosition`, `MapID`, and `NexusLink.Width/Height/Scaling/
   IsGameplay` — with the map closed, with the minimap only, and with
   the fullscreen map open at several zooms/pans. That single log
   answers: (a) whether `Center`/`Scale` switch to the fullscreen map
   when it opens, (b) the scale units, (c) whether `IsGameplay` goes
   false with the map open, and (d) the fullscreen map's screen centre.
2. **Then implement option 1** (`src/map_overlay.cpp`): render only
   when `IsMapOpen`, project with the calibrated formula, cap markers,
   click-to-copy, toggle in Options, exempt from the `IsGameplay` gate
   only while the map is open.
3. **After that:** option 2 (minimap) reusing the same projection,
   and/or option 4 (.taco export) if Audrey wants the markers inside
   TaimiHUD as well. Option 7 (auto-show + sync the tile map) can be
   done alongside option 1 as a fallback.

## Sources

- Raidcore Nexus API v6, `third_party/nexus/Nexus.h` (in repo):
  `NexusLinkData_t`, `EGameBinds` (`GB_MapToggle` etc.),
  `GameBinds_PressAsync`, `GUI_Register(RT_Render)`,
  `WndProc_SendToGameOnly`, `MinHook_Create`.
- MumbleLink, `third_party/mumble/Mumble.h` (in repo): `Context.IsMapOpen`,
  `Compass.Width/Height/Rotation/PlayerPosition/Center/Scale`,
  `Context.MapID`.
- GW2 Toolbelt GW2ML docs — `MumbleLink.Context`: `getMapCenterX/Y`,
  `getMapScale`, `getCompassWidth/Height/Rotation`, `UIState.isMapOpen`:
  https://gw2toolbelt.github.io/GW2ML/3.0.1/api/com.gw2tb.gw2ml/com/gw2tb/gw2ml/MumbleLink.Context.html
- GW2 TacO, "Minimap and World Map Support" (Oct 2019) — MumbleLink
  minimap data added by ArenaNet; markers/trails on minimap and full
  map; `mapDisplaySize`, `miniMapVisibility`, `mapVisibility`,
  `inGameVisibility`: https://www.gw2taco.com/2019/10/?m=1
- GW2 Pathing docs — Visibility (`miniMapVisibility` / `mapVisibility` /
  `inGameVisibility`, default visible on minimap, fullscreen map, and
  in-game): https://gw2pathing.com/docs/marker-dev/attributes/visibility/
  ; MapDisplaySize / ScaleOnMapWithZoom:
  https://gw2pathing.com/docs/marker-dev/attributes/ (via
  blish-hud/Pathing wiki); Advanced settings,
  `map-trigger-hide-from-camera`:
  https://gw2pathing.com/docs/usage/advanced-settings/
- ArenaNet, Policy: Third-Party Programs — no program giving an
  unintended/unfair advantage or automating gameplay; no review/approval
  of any third-party program, use at own risk:
  https://help.guildwars2.com/hc/en-us/articles/360013625034-Policy-Third-Party-Programs
- Current addon state: `README.md` (v2.0 tile map, `IsGameplay` gates in
  `src/entry.cpp:454` and `src/map_view.cpp:614`), `src/map_view.cpp`
  (tile projection `pixel = coord * 2^(zoom - MAX_ZOOM)` — the same
  continent-coordinate system the overlay projection would use).
