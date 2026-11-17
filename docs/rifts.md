# Rifts — research note for Tyria Finder

Date: 2026-11-17. Sources checked 2026-11-17 (07:04 UTC).
Do NOT rebuild the DLL from this note alone — this is research + design only.

## What rifts are

Rift Hunting, introduced in Secrets of the Obscure (SotO). Rifts are portal
events: activate one, defeat waves of enemies, defeat a champion boss, then
channel the Heart of the Obscure to close it. A new rift then appears
elsewhere on the same map.

- 3 tiers (T1 / T2 / T3). Any map with rift activity has exactly one rift
  per tier. T1 is soloable; T2/T3 need a group.
- Rewards scale with tier, Motivations consumed, and contribution. Essences:
  T1 = Fine, T2 = Masterwork, T3 = Rare Rift Essence. Essences craft
  Legendary Obsidian / Suffused Obsidian armour. Weapon drops: Skyforged
  (Kryptis rifts), Eagle Eye (Titanspawn rifts), Skyscale weapons (all rifts).
- Locating them: Rift Guidance mastery (Heart of the Obscure Research,
  SotO) gives "Scan for Rift" (default keybind J). It points at the nearest
  T1 rift on the current map, or, used on a map with no rifts, shows a
  dialogue with the maps that currently have them.
- Requirements: SotO or Janthir Wilds ownership to interact with a rift;
  Rift Guidance needs SotO story chapter 2 ("Hell Breaks Loose") done.
  Players without the mastery can still join rifts other players start.
- VoE (Sep 2026, "Code of Creation") added the Rift Amplification mastery:
  overcharge rifts and travel straight to the next one.

Sources: Snow Crows, "Rift Hunting Guide"
(https://snowcrows.com/guides/open-world/rift-hunting-guide, updated
2026-03-08); GW2 Wiki, "Rift Hunting" (via wiki API, 2026-11-17);
GuildJen, "Rift Hunting and Convergences Guide"
(https://guildjen.com/rift-hunting-and-convergences-guide/, updated
2026-09-26).

## The three rift types and their always-on maps (11 maps)

These maps ALWAYS have rifts. They do not rotate.

| Type | Maps | Enemies / notes |
|---|---|---|
| Kryptis | Skywatch Archipelago, Amnytas, Inner Nayos | Kryptis demons from the Mists |
| Titanspawn | Lowland Shore, Janthir Syntri, Mistburned Barrens, Bava Nisos | Titanspawn; Mistburned Barrens is the popular T1 XP / spirit-shard farm (two rifts often close together) |
| Castora (VoE) | Shipwreck Strand, Starlit Weald, Eternity's Garden, Leyspring Hollows | Inquest / choya / seer defences, varies by map. Snow Crows (Mar 2026, pre-VoE quarterly updates) lists Inquest rifts only in Shipwreck Strand and Starlit Weald; the wiki template and the official API Weekly Rift Hunting (VoE) category (id 464, achievements 8892/8980/9303/9402) now cover all four Castora maps, so all four are treated as always-on. |

## The weekly rotating maps (3 maps, Kryptis only)

On top of the 11 always-on maps, 3 more maps have Kryptis rifts each week,
drawn from Core Tyria / LWS3 / LWS4 maps on a FIXED, published 11-week
cycle. This is NOT random: the GW2 Wiki template `Template:Weekly_Rift_Hunting`
computes it from an anchor date.

- Formula (from the template): index = 1 + floor((now − 2023-11-05 23:30
  America/Los_Angeles) / 7 days) mod 11. The anchor is Monday 2023-11-06
  07:30 UTC, i.e. the weekly achievement reset. Rotation changes Monday
  07:30 UTC (weekly reset; the template's noinclude note says "Monday at
  00:00 UTC", which is the same boundary expressed loosely — the anchor
  itself is 07:30 UTC).
- Weekly Rift Hunting achievement category (SotO, API id 365): "6 zones are
  available every week: Skywatch Archipelago, Amnytas and Inner Nayos are
  always present plus three other zones in rotation each week."
- Caveat: a 2023 forum thread noted the rotation looked flawed at the time
  (sets repeating out of order, new maps not yet placed). The 11-set table
  below is the wiki template as it stands on 2026-11-17; if ArenaNet ever
  changes the cycle, the baked table goes stale — same caveat as the PSNA
  table. Verify with `/wiki Weekly Rift Hunting` in game.

### The full 11-week cycle (from Template:Weekly_Rift_Hunting, 2026-11-17)

| Set | Map 1 | Map 2 | Map 3 |
|---|---|---|---|
| 1 | Straits of Devastation | Elon Riverlands | Domain of Istan |
| 2 | Sparkfly Fen | Tangled Depths | Sandswept Isles |
| 3 | Bloodtide Coast | Lake Doric | Domain of Vabbi |
| 4 | Frostgorge Sound | Ember Bay | Seitung Province |
| 5 | Iron Marches | Verdant Brink | Bitterfrost Frontier |
| 6 | Mount Maelstrom | Jahai Bluffs | New Kaineng |
| 7 | Malchor's Leap | Bloodstone Fen | Desert Highlands |
| 8 | Fireheart Rise | Dry Top | Auric Basin |
| 9 | Cursed Shore | Southsun Cove | Crystal Oasis |
| 10 | Mount Maelstrom | Lake Doric | Domain of Vabbi |
| 11 | Timberline Falls | Thunderhead Peaks | Echovald Wilds |

### CURRENT week — week of Mon 2026-11-16 to Mon 2026-11-23 (07:30 UTC)

Computed from the formula above (158 weeks elapsed since the anchor):
**Set 5 — Iron Marches, Verdant Brink, Bitterfrost Frontier** (Kryptis rifts).
Next week (from Mon 2026-11-23 07:30 UTC): Set 6 — Mount Maelstrom,
Jahai Bluffs, New Kaineng.

Total maps with rifts this week: 11 always-on + 3 rotating = **14 maps**.

## Current maps with rifts + entry waypoints (verified in data/pois.json)

CRITICAL honesty point: rifts spawn RANDOMLY on a map, one per tier, and
move when closed. There is NO published "rift start waypoint" per map, and
no waypoint in this table is a rift spawn point. Each waypoint below is a
sensible central / main-entry waypoint for its map, verified to exist in
`data/pois.json` (3,773 entries) with the exact name and chat link shown.
The addon must say so in the UI ("rifts spawn randomly — use Scan for
Rift once you're there"), or users will go to the waypoint expecting a
rift to be there.

| Map | Rift type | Entry waypoint (central / main entry — judgement pick, NOT a rift spawn) | Chat link |
|---|---|---|---|
| Skywatch Archipelago | Kryptis, always | Astral Ward Encampment Waypoint | [&BA4OAAA=] |
| Amnytas | Kryptis, always | Bastion of the Natural Waypoint | [&BDQOAAA=] |
| Inner Nayos | Kryptis, always | Astral Ward Camp Waypoint | [&BGYOAAA=] |
| Lowland Shore | Titanspawn, always | Harvest Den Waypoint | [&BK4OAAA=] |
| Janthir Syntri | Titanspawn, always | Stricken Plains Waypoint | [&BCoPAAA=] |
| Mistburned Barrens | Titanspawn, always | Alliance Staging Ground | [&BFAPAAA=] |
| Bava Nisos | Titanspawn, always | Mantle's Arrival Waypoint | [&BGEPAAA=] |
| Shipwreck Strand | Castora, always | Hullgarden Pier Waypoint | [&BMwPAAA=] |
| Starlit Weald | Castora, always | Foothold Bivouac Waypoint | [&BMAPAAA=] |
| Eternity's Garden | Castora, always | Pilgrim's Rest Waypoint | [&BPwPAAA=] |
| Leyspring Hollows | Castora, always | Hall of Assemblage Waypoint | [&BDYQAAA=] |
| Iron Marches | Kryptis, rotating — THIS WEEK (Set 5) | Brandwatch Encampment Waypoint | [&BOkBAAA=] |
| Verdant Brink | Kryptis, rotating — THIS WEEK (Set 5) | Jaka Itzel Waypoint | [&BOAHAAA=] |
| Bitterfrost Frontier | Kryptis, rotating — THIS WEEK (Set 5) | Koda's Welcome Waypoint | [&BIEJAAA=] |

All 14 waypoints verified in `data/pois.json` on 2026-11-17. No map is
missing a waypoint. Mistburned Barrens has only ONE waypoint in the
dataset (Alliance Staging Ground), so that pick is unambiguous. Verdant
Brink / Jaka Itzel is already tagged (flax etc.); no existing entry has a
"rift" tag — the only "rift" strings in `data/tags.json` are unrelated
("Tribulation Rift Scaffolding" JP, etc.), so rift tags are a clean add.

Note: Verdant Brink has two "Shipwreck Peak Waypoint" entries in the
dataset with different codes ([&BN4HAAA=] and [&BMAHAAA=]) — unrelated to
rifts, but worth a look by whoever next touches the dataset.

## What could NOT be verified / is not a live feed

- The CURRENT rotating 3 could not be confirmed from the live GW2 API:
  `/v2/achievements/daily` and `/v2/achievements/daily/tomorrow` both
  return HTTP 503 ("API not active") as of 2026-11-17, and the static
  `/v2/achievements/categories` + `/v2/achievements` endpoints list ALL
  possible weekly incursion achievements (SotO cat. 365: 7044, 7064, 7072,
  7075, 7078, 7655; JW cat. 423: 8201, 8257, 8571, 8766; VoE cat. 464:
  8892, 8980, 9303, 9402), not which are active this week. The wiki
  template formula above is the source for "this week = Set 5" — it is
  computed, not fetched live, and should be spot-checked in game
  (Weekly Rift Hunting panel, or Scan for Rift on a map with no rifts).
- The wiki "Rift Hunting" page itself returned HTTP 403 via browser.open
  on 2026-11-17; the same content was fetched successfully via the wiki
  API (`api.php?action=query&prop=revisions…`), which is the source used
  here. GuildJen's guide page was bot-blocked ("One moment, please…");
  its search snippets were used only to corroborate the always-on maps.
- No live in-game check was possible from this VM. Audrey (or her
  in-game check) is the final verification for Set 5.

## Proposed UI design (for the build, not built here)

Placement: third section in the "today / this week" stack, directly under
Daily Pact Supply Network Agents and Map Bonuses. Same visual language as
the PSNA section (gold header, small schedule note underneath, clean rows).

Header: "Rifts This Week" (gold), with a small note underneath:
"Resets Monday 07:30 UTC. Rifts spawn randomly on each map — use Scan
for Rift keybind once you're there."

Layout — two groups, so the 14 maps don't become a wall of text:

1. "Rotating this week — Kryptis" (highlighted, 3 rows):
   Iron Marches / Verdant Brink / Bitterfrost Frontier.
2. "Always available" (11 rows, grouped by type, collapsible if the
   window gets too tall):
   - Kryptis: Skywatch Archipelago, Amnytas, Inner Nayos
   - Titanspawn: Lowland Shore, Janthir Syntri, Mistburned Barrens,
     Bava Nisos
   - Castora: Shipwreck Strand, Starlit Weald, Eternity's Garden,
     Leyspring Hollows

Each row: map name + rift type (small, muted). Clicking a row copies its
entry waypoint chat code only — consistent with search results and with
the PSNA "Copy daily list" pattern. Do NOT copy a sentence with the map
name + code in one click (that would be a different pattern from the rest
of the addon); the row label already shows the map name.

Do NOT add a "Copy all rift maps" button: 14 codes would be far over the
199-char GW2 chat limit.

Search tags (add to `data/tags.json`, validated via
`tools/apply_tags.py`): tag each entry waypoint above with "rift",
"rifts", "rift hunting", plus its type phrase — "kryptis rift",
"titanspawn rift", "castora rift" / "inquest rift" as appropriate — so
searching "rift", "kryptis rift" or a map name also finds the entry
waypoint. Tags must stay hidden from result lines (v1.8.1 rule).

Currency: BAKE the 11-set table above into the code, exactly like PSNA:
compute the week index from the system clock using the template formula
(anchor 2023-11-06 07:30 UTC, 11-week cycle, mod 11). No network fetch,
works offline. Add the caveat in README/code comments (not in the visible
UI): if ArenaNet changes the cycle, the table goes stale — verify with
`/wiki Weekly Rift Hunting`.

## Sources

- Snow Crows, Rift Hunting Guide, https://snowcrows.com/guides/open-world/rift-hunting-guide (updated 2026-03-08)
- GW2 Wiki, "Rift Hunting" and "Weekly Rift Hunting" + Template:Weekly_Rift_Hunting, via wiki API api.php (2026-11-17)
- GW2 Wiki, "Rift" (Living World Season 4 feature — a DIFFERENT thing: Kralkatorrik rifts in Jahai Bluffs / Thunderhead Peaks; do not confuse with Rift Hunting)
- GuildJen, Rift Hunting and Convergences Guide, https://guildjen.com/rift-hunting-and-convergences-guide/ (updated 2026-09-26; page itself bot-blocked, snippets used)
- Official GW2 API, api.guildwars2.com/v2/achievements/categories + /v2/achievements (2026-11-17): Weekly Rift Hunting categories 365 (SotO), 423 (JW), 464 (VoE); /v2/achievements/daily returned HTTP 503
- Tyria Finder dataset: ~/workspace/gw2-waypoint-search/data/pois.json (3,773 entries), data/tags.json (310 tagged entries at time of check — other tag work in progress, count may move)
