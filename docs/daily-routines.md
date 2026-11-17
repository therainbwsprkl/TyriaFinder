# Daily routines — what else is PSNA-like?

Research note, 2026-11-17. Research only — no code changed, no DLL rebuilt.
Question from Audrey: are there other daily routine things like the daily
PSNA that could be incorporated? Answer honestly if there are none.

## Short answer

Yes, a couple — but PSNA was the main one. It is the only daily I found
with **both** a fixed published rotation **and** a different location
every day. The only other fixed-cycle daily is Daily Fractals, and all
fractals go through one door, so the waypoint value is a list, not a
hunt. Everything else is either already covered by existing tags, a
timer rather than a location, random / API-driven with no baked-in
cycle, or weekly rather than daily.

## What PSNA was, for comparison

- 6 agents, one per region, fixed 7-day weekday cycle, locations change
  at 08:00 UTC. 40 unique locations, all verified against the dataset.
- Baked-in table + system UTC clock, no network fetch, no API key.
- A "Copy daily list" button works because today's set is exactly 6
  chat codes (71 chars, fits the 199-char chat limit).

A candidate only counts as "PSNA-like" if it clears the same bar:
fixed rotation, fixed locations, verifiable waypoints.

## Ranked feasible candidates

### 1. Daily Fractals — BEST next daily, with one unverified anchor

- What: 3 daily fractals + 3 recommended fractals, new set every day
  at 00:00 UTC. Instabilities are random, but the fractal sets are on
  a **fixed 15-day rotation** (MetaBattle / wiki).
  - Set 1: Solid Ocean, Underground Facility, Urban Battleground
  - Set 2: Aetherblade, Chaos, Nightmare
  - Set 3: Cliffside, Molten Boss, Siren's Reef
  - Set 15: Snowblind, Thaumanova Reactor, Aquatic Ruins
  - (Full 15-set table is in MetaBattle's Fractals introduction guide;
    recommended fractals have their own 15-day table.)
- Location: **all fractals enter through one portal** — Fort Marriner
  Waypoint, Lion's Arch `[&BDAEAAA=]` — already tagged ("fractals" →
  Fort Marriner, v1.3). BUY-4373 (daily discounted encryption keys,
  30/day) is inside Mistlock Observatory, same entry point.
- Fit: same model as PSNA — a baked-in 15-day table + UTC date, a
  `daily fractals` intercept returning today's 3 names, and a copy
  list that is really just the one waypoint (the value is naming the
  3 fractals, not finding a place).
- **Gap — do not build until this is closed:** the rotation sets are
  published, but I did **not** find a published anchor date (which
  calendar date is Set 1). Without an anchor, the table cannot tell
  you which set is today's. The anchor would have to come from the
  live API (`/v2/achievements/daily`) or by observing the in-game
  daily for 1–2 days and back-calculating. That API endpoint returned
  HTTP 503 / "API not active" when checked 2026-11-17, so it cannot
  be relied on right now.
- Value for Audrey: high — she does fractals. Effort: low once the
  anchor is known; medium if it needs live verification.
- Note: completing a T4 daily also grants the lower-tier rewards, so
  the list is 3 names, not 9.

### 2. Daily Ley-Line Anomaly — fixed clock, two waypoints still unverified

- What: Legendary Ley-Line Anomaly spawns every 2 hours, rotating
  through 3 maps on a fixed 6-hour cycle, and gives a Mystic Coin
  once a day. Times (UTC, from the wiki):
  - Timberline Falls: 00:20, 06:20, 12:20, 18:20
  - Iron Marches: 02:20, 08:20, 14:20, 20:20
  - Gendarran Fields: 04:20, 10:20, 16:20, 22:20
- Location: Gendarran Fields is already tagged (Provern Shore
  `[&BOQAAAA=]`, v1.3). Timberline Falls and Iron Marches staging
  waypoints were **not** verified in v1.3/v1.4 and still are not.
- Fit: pure clock arithmetic from the system UTC clock — a "next
  anomaly" lookup (which map, what time, which waypoint) needs no
  network and no table. No daily list to copy; it's a next-spawn
  question, not a 6-code list.
- Value: medium — a daily Mystic Coin is a real routine, and Audrey
  already farms / does events. Effort: low-medium (verify the two
  missing waypoints first).

### 3. Faction Provisioners — NOT a rotation, but a real daily list

- What: ~9+ fixed vendors across Tyria (6 in major cities + 3 in
  Heart of Maguuma maps, plus Wizard's Tower / WvW). Trade specific
  crafted items / map materials for Provisioner Tokens, daily caps
  (up to ~33 tokens/day), used for legendary crafting. Vendors do
  **not** move — the daily part is the trade cap, not the location.
- Location: fixed, so every vendor has one verified waypoint (e.g.
  Lion's Arch Skritt Trader — Commodore's Quarter Waypoint
  `[&BAwEAAA=]`; Wizard's Tower — Tower Courtyard Waypoint
  `[&BB8OAAA=]`, per GuildJen). None of these are tagged in the addon
  yet — this is a genuinely new static set, not a duplicate.
- Fit: static tags ("provisioner", "faction provisioner") + a
  copy-list of all vendor waypoints, exactly like the PSNA list but
  with no day logic. No rotation table needed.
- Value: medium-high **if** Audrey is working toward a legendary;
  low if she is not. Effort: medium (verify ~9–12 vendor waypoints
  against the dataset; the items each vendor wants change per tab
  and are not waypoint-relevant).
- Caveat: some vendors are weekly-capped, some have no daily limit
  (Wizard's Tower), and some trade for items that are themselves
  daily-gated — the list would be locations only, not a shopping list.

### 4. Daily Convergences / Eye of the North public instances — timing, not location

- What: public Convergences open every 3 hours (Outer Nayos :30,
  Mount Balrior :00, Nexus of Eternity on its own schedule), plus
  Eye of the North public instances (Dragonstorm, Twisted Marionette,
  Battle for Lion's Arch, Tower of Nightmares) every 2 hours.
  Daily completion rewards; weekly achievement tracks exist too.
- Location: already tagged — Convergences → Tower Courtyard
  (Wizard's Tower) in v1.3; Mount Balrior portal is at Harvest Den
  Waypoint, Lowland Shore `[&BK4OAAA=]`, also in the dataset.
  The daily value would be a timer ("next public convergence is
  X at HH:MM"), not a new waypoint.
- Value: low-medium. Effort: low for a timer, but it is a different
  feature (a clock) from waypoint search.

## Already covered — do not double-count these as new

- **World bosses / timed metas:** all 23 boss waypoints + 15–17 meta
  staging waypoints are tagged. The "daily" part is just the
  once-per-day bonus chest (reset 00:00 UTC) and the fixed spawn
  times — a timer feature, not a new location set.
- **Strikes:** all 3 hubs tagged (Eye of the North, Arborstone,
  Tower Courtyard). The daily part is the Priority Strike (see below).
- **Dungeons:** all 8 entrances tagged. Dungeon path rewards reset
  daily, but the location does not change.
- **Jumping puzzles / mini dungeons:** all tagged; their chests reset
  daily. There is a "Daily Jumping Puzzle" achievement, but which JP
  it names today is API-driven — I found no published fixed cycle
  for it, so it cannot be baked in like PSNA.
- **Gathering:** flax / rich nodes / quartz / wood already tagged
  multi-spot. Rich nodes reset per character per day, but their
  locations do not rotate.
- **Dive Master:** already tagged (36/38 goggles); no daily rotation.
- **Region search:** searching a region (e.g. "Ascalon", "Kryta")
  already returns everything in it — this covers most
  region-level daily objectives (see below).

## NOT feasible (honestly) — and why

- **Daily PvE achievements / Wizard's Vault dailies / Daily
  Completionist:** the daily pool is random / drawn from a large
  set, and the objectives are region-level, not point-level
  ("complete events in Ascalon", "view a vista in Kryta", "defeat
  a world boss", "complete a meta event in Cantha"). There is no
  fixed cycle to bake in. The only source for today's set is the
  live API (`/v2/achievements/daily`), which returned HTTP 503 /
  "API not active" when checked 2026-11-17 — and even with it,
  mapping an achievement to a single waypoint would usually be a
  guess (a region, not a spot). Region search already answers
  these: search the region name.
- **Daily Priority Strike (IBS + EoD):** one strike per day per
  expansion, rotates daily — but I found **no published fixed
  cycle** for it. The source is the wiki's "Today's Priority
  Strike Mission" table, which is itself API-driven, and the
  `/v2/achievements/daily` endpoint above. All IBS strikes are
  entered from Eye of the North and all EoD strikes from
  Arborstone, both already tagged — so even if the daily name
  were fetched, it would add a name, not a waypoint.
- **Daily Raid Bounties:** pool draws from the combined raid /
  strike roster (February 2026 unification, per dailyreset.games);
  no fixed cycle found, and raid wings are already tagged to
  Bloodcoast Ward.
- **Living World daily categories (LWS3, LWS4, IBS, Champions,
  Drizzlewood, Bjora, Grothmar, etc.):** rotating daily
  achievements per map (e.g. "Daily Jahai Bluffs Displaced Tower
  Jumping Puzzle", "Daily Soaring Copse Jumping Puzzle"). Each
  individual objective is already tagged by name (the JP /
  adventure / event it names). Which one is today's is API-driven,
  not a published cycle.
- **Daily crafting / time-gated recipes** (Charged Quartz Crystal,
  Lump of Mithrillium, etc.): no location — crafting stations are
  already tagged. Nothing to add.
- **Home instance / guild hall / homestead gathering:** nodes are
  account-specific unlocks, in instanced housing with no public
  waypoint in the dataset. Not addable as waypoint tags.
- **Daily login rewards / laurels:** no location at all.
- **Map Bonus Rewards:** an 8-week cycle, rotating Thursdays
  20:00 UTC — this is **weekly**, not daily, and the reward is
  earned by doing events on that map. Region/map search already
  covers "go to this map". A weekly map-bonus lookup would be a
  separate weekly feature, not a daily one, and would need the
  8-week anchor verified the same way as fractals.
- **Awakened Invasion:** rotates weekly across Core Tyria maps;
  sources say "see wiki for current location" — no fixed waypoint
  published, not bakeable.
- **Weekly things that feel daily:** weekly raids (wings already
  tagged), weekly strikes / Emissary Chest (Eye of the North,
  already tagged), weekly convergences, weekly rift hunting
  (SotO/VoE maps rotate weekly). All weekly, all already
  location-covered.

## Honest recommendation

1. **Next daily feature, if any: Daily Fractals** — but only after
   the 15-day anchor is verified (one in-game check of today's 3
   fractals against the published sets, or a working API read).
   It is the only other fixed-cycle daily, and Audrey does
   fractals. The build would be a `daily fractals` intercept +
   today's 3 names, all pointing at Fort Marriner.
2. **Then, if she wants it: Ley-Line Anomaly next-spawn** — verify
   the Timberline Falls and Iron Marches staging waypoints, then a
   clock-based "next anomaly: <map> at HH:MM, waypoint <code>".
3. **Then, only if she is doing legendaries: Faction Provisioners**
   as a static tagged list + copy list.
4. **Do not build:** a generic "today's dailies" feature driven by
   `/v2/achievements/daily` — the endpoint was unavailable when
   checked, the objectives are mostly region-level, and the addon
   would be guessing waypoints for most of them. Region search
   already does the useful part of that job.

Bottom line: PSNA was the main one. There are two real follow-ups
(fractals, ley-line), one conditional static list (provisioners),
and the rest is either already covered or not honestly buildable
as a baked-in daily.

## Sources

- MetaBattle, "Introduction Guide — Fractals of the Mists"
  (15-day daily + recommended rotation tables)
  https://metabattle.com/wiki/Guide:Introduction_to_Fractals
- GW2 Wiki, "Legendary Ley-Line Anomaly" (2-hour / 6-hour rotation,
  Timberline 00:20/06:20/12:20/18:20, Iron Marches
  02:20/08:20/14:20/20:20, Gendarran 04:20/10:20/16:20/22:20)
  https://wiki.guildwars2.com/wiki/Legendary_Ley-Line_Anomaly
- GuildJen, "How to Get Provisioner Tokens in Guild Wars 2"
  (fixed vendor locations, daily/weekly caps)
  https://guildjen.com/how-to-get-provisioner-tokens-in-guild-wars-2/
- GuildJen, "Convergence: Outer Nayos Guide" (public windows every
  3h at :30) and ProjektDyad, "Mount Balrior Convergence"
  (Harvest Den Waypoint `[&BK4OAAA=]`, every 3h at :00)
- Cellofrag GW2 Event Timer (wiki v5.4 schedule data, retrieved
  2026-11-17) https://cellofrag.com/guild-wars-2-event-timers
- Tyria Pulse, world-boss timer + daily-reset explainers
  (quarter-hour core rotation, 00:00 UTC reset)
  https://tyriapulse.vercel.app/articles/gw2-world-boss-timer
- dailyreset.games, GW2 checklist (61 daily / 33 weekly items,
  verified for Visions of Eternity)
  https://www.dailyreset.games/games/guild-wars-2/checklist/
- gw2treasures Achievements page (Daily categories listed; "Daily"
  and "Daily Strike Mission" noted as not available in the API)
  https://en.gw2treasures.com/achievement
- Official API check, 2026-11-17: `GET
  https://api.guildwars2.com/v2/achievements/daily` returned
  "API not active" (curl) and HTTP 503 (browser fetch) — do not
  rely on it until re-checked; not retried.
- Wiki "Strike Mission" page (Priority Strike table is API-driven;
  no fixed cycle published) — via wiki.guildwars-2.ru mirror.
- Addon state: `~/workspace/gw2-waypoint-search/README.md` (v1.7)
  and `data/COVERAGE.md` — existing tag counts and coverage used
  for the "already covered" section.
