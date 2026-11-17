# Daily Activities — research + tags (2026-11-17)

> **REMOVED in v1.10.4 (2026-11-17, Audrey: "Actually remove the daily activity").**
> The whole Daily Activity section is gone from Tyria Finder, and the
> "daily activity" umbrella tags are removed from `data/tags.json`
> (baked tags now 335 entries / 2,761 phrases). The four individual
> activities keep their own name tags ("crab toss", "keg brawl",
> "sanctum sprint", "southsun survival", "aspect arena", "moa racing").
> Everything below is the historical research record of the v1.9–v1.10.3
> section — kept so the work is not lost if Audrey ever asks for it back.
> Backstory: Havoc's Heir (Edinna's location) is a paid lounge, reachable
> only with a Captain's Airship Pass — Audrey first asked to re-route via
> Lion's Arch, then to drop Edinna's name, then to remove the section
> altogether. No Lion's Arch replacement was ever verified to a named NPC +
> waypoint from a citable source, so none was invented.

## The daily activity (Daily Activity Participation)

One activity per day, from a rotation of **four**, via the access NPCs
**Edinna Linhoft** (Havoc's Heir airship, Gendarran Fields) or **Kouris**
(historical — Vigil Keep, Gendarran Fields, 2014; Edinna is the current one).
Talking to Edinna teleports you to today's activity, whatever it is.
Reset: **00:00 UTC** daily.

Sources:
- GW2 Wiki (mirror) — Edinna Linhoft: "Edinna Linhoft is on the Havoc's
  Heir airship in Gendarran Fields and grants access to the daily activity."
  "There are currently four activities in rotation: Keg Brawl, Crab Toss,
  Sanctum Sprint, and Southsun Survival."
- GW2 Wiki (mirror) — Daily: "Speak with Kouris or Edinna Linhoft to gain
  access: Keg Brawl / Crab Toss (active) / Sanctum Sprint / Southsun Survival.
  Some holiday based activities also grant credit to this achievement."
- Official API: `GET /v2/achievements/daily` returns `{"text": "API not active"}`
  (checked 2026-11-17) — no live source for today's activity.

## The four, and where to go

| Activity | Where | Access / NPC | Waypoint tagged | Confidence |
|---|---|---|---|---|
| Crab Toss | Southsun Cove, Sawtooth Bay | Karlotta, north of Privateer's Moorage POI | Camp Karka Waypoint `[&BNcGAAA=]` | Medium-high — nearest waypoint by dataset coordinates to Privateer's Moorage `[&BNYGAAA=]` (470 units; Pearl Islet 527, close second). Straight-line, not a published "closest waypoint" statement. |
| Keg Brawl | Hoelbrak, Lake Mourn (NW) | Brewer NPC, NW corner of Hoelbrak | Hero's Compass Waypoint `[&BJADAAA=]` | **Medium** — no published source names a nearest waypoint. Hero's Compass is the westernmost Hoelbrak waypoint in dataset coordinates; Lake Mourn is in NW Hoelbrak. |
| Sanctum Sprint | Labyrinthine Cliffs | Aspect Master, near Zephyr Sanctum entrance, just south of Sky Docks Waypoint | Sky Docks Waypoint `[&BB0HAAA=]` | High — Festival of the Four Winds wiki activities table: "Closest waypoint: Sky Docks Waypoint". Only playable during Festival of the Four Winds, or on its daily-activity day via Edinna. |
| Southsun Survival | Labyrinthine Cliffs (arena in Southsun Cove) | Evon Gnashblade at Bazaar Docks | Bazaar Docks Waypoint `[&BBwHAAA=]` | High-medium — wiki: "located in Labyrinthine Cliffs and accessed through the Evon Gnashblade at Bazaar Docks". |
| (access) Daily Activity — REMOVED in v1.10.4 | Gendarran Fields, Havoc's Heir | Edinna Linhoft | Lionbridge Waypoint `[&BJsDAAA=]` | **Medium** — no published source names Lionbridge as nearest. It is the Vigil Keep / Havoc's Heir area waypoint. Was tagged so "daily activity" / "edinna linhoft" returns a way to reach Edinna and be teleported to today's activity. Tag removed in v1.10.4; Lionbridge Waypoint itself is still in the dataset as a real waypoint, just untagged. |

Tags added (this task): "crab toss", "keg brawl", "sanctum sprint",
"southsun survival", "aspect arena", "daily activity", "activity",
"daily activity participation", "edinna linhoft", plus "moa racing" (below).
**v1.10.4: "daily activity", "activity", "daily activity participation"
and "edinna linhoft" are removed again** — the four activity-name tags stay.
Search spot-checks (tags in `data/pois.json` after `apply_tags.py`):
"crab toss" → 1 (Camp Karka), "keg brawl" → 1 (Hero's Compass),
"sanctum sprint" → 1 (Sky Docks), "southsun survival" → 1 (Bazaar Docks),
"daily activity" → 5 (all four + Lionbridge), "aspect arena" → 1 (Sky Docks),
"moa racing" → 1 (Farshore).

## Rotation — NOT bakeable (honest verdict)

No reliable fixed rotation could be verified, so **today's activity cannot
be computed offline and must NOT be baked in**:

- Two old forum claims conflict. (1) 2013, 7-day: Crab Toss, Sanctum Sprint,
  Southsun Survival, Crab Toss, Sanctum Sprint, Southsun Survival, Keg Brawl,
  repeat. (2) 2014, 6-day, anchored "6 Sept = Keg Brawl" (year unstated):
  0 Sanctum Sprint, 1 Southsun Survival, 2 Crab Toss, 3 Keg Brawl,
  4 Southsun Survival, 5 Keg Brawl, 6 Crab Toss. Neither has a verified
  anchor date that survives to 2026, and neither is corroborated by the
  current wiki.
- The current GW2 Wiki Daily page no longer publishes an activity rotation
  (the historical Daily achievements were replaced by Wizard's Vault in
  Aug 2023). The Edinna Linhoft mirror page's "current daily activity"
  note is a stale crawl snapshot (crawled Apr 2026, showing Sanctum Sprint).
- The official daily API is inactive (see above).
- A 2015 forum note says the rotation "is somehow synced up to the wiz
  vault daily rotation" — unverified, and not a usable formula.

**Today's activity (Mon 2026-11-16 / Tue 2026-11-17) is therefore UNKNOWN
from public sources.** It can only be determined in-game: talk to Edinna
Linhoft, or check the Daily Activity Participation objective.

### Proposed UI (for the builder, not built here)

Do NOT add a "Today's activity is X" line — it would be a guess.
Instead, add a small static section under the daily sections:

> **Daily Activity** — resets 00:00 UTC. Talk to Edinna Linhoft on the
> Havoc's Heir (Gendarran Fields) — she teleports you to today's game.
> [Go to Edinna →] (copies Lionbridge Waypoint `[&BJsDAAA=]`)
> Today's game is one of: Crab Toss · Keg Brawl · Sanctum Sprint ·
> Southsun Survival.

That is honest, never goes stale, and still gives the user a one-click
way to the access NPC. Searching any activity name already returns its
direct location waypoint (see table above).

## Other activities — full list, and what was NOT tagged

The wiki's Activity achievement category lists, in addition to the four
above: **Belcher's Bluff, Costume Brawl, Aspect Arena** (tagged, see above),
plus festival-only activities.

- **Belcher's Bluff** — permanent drinking minigame, but it has **six**
  Masters of Om in six places, not one location: Maddie (Divinity's Reach),
  Berddi (Rata Sum), Caiwyn the Corsair (The Grove), Adnul Irongut
  (Hoelbrak), Graster Beakerbane (Black Citadel), Poyaqui (Labyrinthine
  Cliffs, then Lion's Arch). No single waypoint is correct. **Not tagged.**
  A future pass could tag each master to its city waypoint, but the nearest
  waypoint for each master was not verified in this pass.
- **Costume Brawl** — no fixed location; it is played anywhere with costume
  brawl skills (e.g. Ghostly Owl Feather, 147 karma). **Not tagged** —
  there is nothing to waypoint to.
- **Aspect Arena** — Labyrinthine Cliffs, Sky Docks Waypoint (see above).
  Festival of the Four Winds only. Tagged.
- **Moa Racing** — Farshore Ward, Lion's Arch, speak to Tigg. Tagged to
  Farshore Waypoint `[&BDMEAAA=]` (medium confidence, **seasonal only**):
  removed from the permanent game with Escape from Lion's Arch (2014),
  returns only during Dragon Bash.
- **Dragon Ball** — Dragon Bash festival activity, Lion's Arch. No verified
  nearest waypoint found in this pass. **Not tagged.**
- **Festival activities generally** (Wintersday Snowball Fight, Halloween
  mini-games, etc.) — seasonal, no fixed daily rotation. Not in scope;
  tag individually if Audrey asks for one by name.

## Validation

## v1.10.4 removal validation

- `tools/apply_tags.py`: pass — "tagged 335 entries in data/pois.json
  (2761 tag phrases)".
- `tools/test_search.py`: **186/186 pass** — "daily activity", "edinna"
  and "edinna linhoft" now return 0 results; "crab toss" / "keg brawl" /
  "sanctum sprint" / "southsun survival" still return their own waypoints.
- DLL: v1.10.4.0, sha256 `d6ce4cd7893deeb2d88e82f987a28d09014200596f72e071b449c1569e0c5583`.

## Validation (original, v1.9)

- `tools/apply_tags.py`: pass — "tagged 336 entries in data/pois.json
  (2773 tag phrases)". (Baseline when this task started was 310 entries /
  2,390 phrases; a parallel guild-missions / mount-races sweep was editing
  `tags.json` at the same time and brought it to 333 entries before this
  task's 3 new entries landed. This task added 3 new entries + 3 extensions
  = 23 new phrases of its own.)
- `tools/test_search.py`: **149/149 pass**.
- No DLL rebuilt (per task instructions).
