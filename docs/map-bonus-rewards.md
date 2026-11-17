# Map Bonus Rewards — design note for Tyria Finder

Date researched: 2026-11-17 (Mon). Current week at time of writing: **Week 4, Thu 12 Nov 20:00 UTC – Thu 19 Nov 20:00 UTC**.

Sources: GW2 Wiki "Map bonus reward" (https://wiki.guildwars2.com/wiki/Map_bonus_reward — text fetch was a stale July 2025 cache, Week 8, so all week numbers below were cross-checked against the live GW TODOBOX weekly page, https://gw-todo.vercel.app/weekly, crawled 2026-11-17 07:04 UTC, which independently says "Week 4"), wiki "Map bonus reward/profit" (https://wiki.guildwars2.com/wiki/Map_bonus_reward/profit — also stale-cached, use `/wiki mbrp` in-game for live values), GW2 forums (map-reward explainers, 8-week cycle, Thursday rotation).

## How Map Bonus Rewards work

- Completing events, jumping puzzles, and mini-dungeons in a PvE map earns points on that map's reward track (account-based; full event participation = 100 points).
- A reward is given every 200 points, up to 8,000 points / 40 rewards, then the track resets and starts again. Roughly one reward per two events.
- Every 20th (and 40th) reward gives 10× the current item — so the track's **common reward** (the item repeated most often, usually the 200-point reward) dominates the total value.
- Pact Scout's Mapping Materials (PSMM, bought daily from the PSNA agents — the section already in the addon) grant 200 points each in Central Tyria zones, with no diminishing returns. So a full 40-step track = 40 PSMM. This is why the PSNA section and this section belong together: PSNA tells you where to buy the materials, this section tells you which map to spend them in.
- Character-based diminishing returns apply to event-earned points; PSMM is not affected.

## Rotation / reset — FIXED, bakeable like PSNA

- **Reward tracks change every week at Thursday 20:00 UTC.** (Wiki "Map bonus reward", Mechanics; also GW2 forum guide "Taking Advantage of Map Bonus Rewards".)
- **There is an eight-week cycle of reward tracks.** Week 1's rewards are the same as Week 9's, etc.
- This is a **fixed, published rotation** — each Central Tyria map has a fixed Week 1–8 table on its own wiki page (e.g. Harathi Hinterlands, Kessex Hills, Cursed Shore, Frostgorge Sound). It is NOT random and does NOT need a live fetch to know *which items* a map gives in a given week.
- Anchor (from the wiki page, July 2025): the week Thu 24 Jul – Thu 31 Jul 2025 was **Central Tyria Week 8** (HoT Week 6 — HoT runs on its own offset, see below).
- Counting forward in 7-day steps from that anchor: Thu 12 Nov 2026 = **Central Tyria Week 4**, next rotation Thu 19 Nov 2026 20:00 UTC = Week 5. This matches GW TODOBOX live ("Week 4", Malchor's Leap highest) — two independent sources agree, so the week number is verified, not just computed.
- Week-number formula for the builder (same pattern as the PSNA weekday table): `weeks_since_anchor = floor((current_utc_thursday_20:00 - 2025-07-24T20:00Z) / 7 days)`, `central_week = ((8 - 1 + weeks_since_anchor) mod 8) + 1`. Use UTC, Thursday 20:00 boundary — before 20:00 UTC on a Thursday it is still the old week.

## What "best maps" means — and the honest limit

- "Best" = most gold from selling all 40 rewards on the Trading Post, after the 15% TP tax. The wiki's `/wiki mbrp` page and GW TODOBOX compute this live from TP prices.
- **The reward tracks are fixed, but the ranking is NOT.** It depends on live TP prices, which move hourly. A ranking baked into the addon is a snapshot: correct at build time, and usually stable for days (T6 material prices move slowly), but it can drift. It must be labelled with its date and re-checked weekly — or the addon must fetch live TP prices, which it currently does not do (Tyria Finder is offline, no network access; adding a live fetch is a bigger change and changes the Raidcore network-access disclosure).
- Recommended approach: bake the **fixed 8-week reward tracks** (which items each map gives, Week 1–8) + compute the current week at runtime + show the **top 5 for the current week from a build-time profit snapshot, date-stamped** (e.g. "Week 4 — ranked 17 Nov 2026"). Add a one-line pointer: "Prices move — check /wiki mbrp in-game for live values." Do NOT present the ranking as live.

## Current week — Week 4 (Thu 12 Nov – Thu 19 Nov 2026, 20:00 UTC)

Live profit ranking from GW TODOBOX (crawled 2026-11-17 07:04 UTC, live TP + vendor values, full 40-step / 8,000-point track). Values are per full track, not per event.

| Rank | Map | Top rewards in Week 4 track | TP list (net) | Instant sell |
|---|---|---|---|---|
| 1 | **Malchor's Leap** | 44× Shiny Bauble, 5× Destroyer Lodestone, 4× Glob of Ectoplasm, 5× Destroyer Core | 17g 37s 19c | 17.04g |
| 2 | **Frostgorge Sound** | 44× Vicious Claw, 7× Corrupted Lodestone, 2× Pile of Crystalline Dust, 3× Corrupted Core, 2× Pile of Incandescent Dust | 12g 20s 10c | 10.55g |
| 3 | **Southsun Cove** | 44× Armored Scale, 7× Crystal Lodestone, 4× Karka Shell, 3× Crystal Core | 10g 62s 41c | 9.59g |
| 4 | **Cursed Shore** | 44× Vial of Powerful Blood, 5× Molten Lodestone, 5× Molten Core, 4× Obsidian Shard (account-bound) | 9g 23s 30c | 8.50g |
| 5 | **Fireheart Rise** | 44× Vicious Fang, 4× Glacial Lodestone, 2× Pile of Crystalline Dust, 2× Pile of Incandescent Dust, 6× Glacial Core | 7g 45s 54c | 7.03g |

Cross-checks against the wiki per-map Week 4 columns (search snippets, wiki tables):
- Cursed Shore Week 4: common reward Vial of Powerful Blood, plus Molten Lodestone at 600 points, Giant Eye at 1,000 points — matches.
- Frostgorge Sound Week 4: common reward Vicious Claw, Corrupted Lodestone at 600 points — matches.
- Southsun Cove Week 4: common reward Armored Scale, Crystal Lodestone — matches (GW TODOBOX; wiki table confirms Armored Scale as the Week 4 common).
- Fireheart Rise Week 4: common reward Vicious Fang, Glacial Core at 600 points — matches.
- Malchor's Leap Week 4: common reward is Shiny Bauble (vendor junk, ~30s each × 44 = ~13g 20s of the total) — that is why it tops the list this week despite the "junk" name; the Destroyer Lodestones / Ectoplasm are the bonus on top. Do not let the name mislead: 44 × ~30s is real gold.

For context, the highest-profit map in the entire 8-week cycle (live, same source): **Week 8: Fireheart Rise, 18g 11s 77c** — so Week 4's Malchor's Leap (17.37g) is close to the cycle best.

Why Malchor's Leap wins this week, in one line: its common reward is 44 Shiny Baubles (vendor junk worth ~30s each), which alone is ~13g, plus Destroyer Lodestones and Ectoplasm.

## Waypoint verification (all 5 verified in data/pois.json)

No waypoint or chat code was invented. Each map below has a suggested entry waypoint — a central, well-known hub in the dataset. These are *suggested* entry points, not wiki-published "start waypoints" like the PSNA agents; label them as such in the UI ("Go to" / entry waypoint), and tag them with `map bonus` phrases in tags.json in the build so searching the map name returns them.

| Map | Suggested entry waypoint | Chat code | In dataset? | Notes |
|---|---|---|---|---|
| Malchor's Leap | Pagga's Waypoint | `[&BKYCAAA=]` | Yes — already tagged elder wood / rich orichalcum / gathering | Central north hub; also Waste Hollows `[&BKgCAAA=]` is a PSNA spot |
| Frostgorge Sound | Earthshake Waypoint | `[&BHoCAAA=]` | Yes — already tagged Claw of Jormag / world boss / rich orichalcum | Claw of Jormag hub, central |
| Southsun Cove | Pearl Islet Waypoint | `[&BNUGAAA=]` | Yes — already tagged Karka Queen / world boss / PSNA (Lady Derwena, Friday) | Central hub, Karka Queen nearby |
| Cursed Shore | Penitent Waypoint | `[&BBkDAAA=]` | Yes — in dataset, currently untagged | Central, near the Penitent / Shelter temple events |
| Fireheart Rise | The Citadel of Flame Waypoint | `[&BEAFAAA=]` | Yes — already tagged rich mithril / Citadel of Flame dungeon | Central dungeon hub |

All five maps have 13–18 waypoints each in the dataset (Malchor's Leap 13, Frostgorge Sound 16, Southsun Cove 6, Cursed Shore 13, Fireheart Rise 18), so there was no shortage of verified waypoints — the picks above are the central hubs. No best map is missing a verified waypoint.

## Scope: Central Tyria only (for now)

- The rotating 8-week tracks, and the profit ranking, apply to **Central Tyria** maps (20 maps on the wiki's Central Tyria table). Those are the ones with a weekly-changing, gold-valued track.
- **Heart of Thorns** maps also have week numbers (HoT Week 2 this week, by the same anchor arithmetic: July 2025 was HoT Week 6), but their rewards are mostly map currencies / caches / slivers (Verdant Brink, Auric Basin, Tangled Depths, Dragon's Stand), not a gold-profit track — do not rank them against Central Tyria on gold.
- **Path of Fire, End of Dragons, Secrets of the Obscure, LWS3/4, Icebrood Saga** maps have fixed (non-rotating) bonus tracks — mostly map currency / writs / volatile magic — so there is no weekly "best map" to show for them. Do not include them in this section.
- So the section is: Central Tyria, top 5, current week. That matches what "best maps for the map bonuses" means in practice.

## Proposed UI design (under the Daily PSNA section)

Placement: directly under the Daily Pact Supply Network Agents section, same window, separated by the same thin divider the PSNA section uses. Keep the window from getting cluttered: this section is a compact list, not a second search box.

Suggested layout (following the v1.8.1 polish rules — no exposed counts, no dev/test language, no `tag:` text):

```
Map Bonus Rewards — Week 4
Best Central Tyria maps this week · resets Thu 20:00 UTC
  1. Malchor's Leap — Shiny Bauble   [Go →]
  2. Frostgorge Sound — Vicious Claw  [Go →]
  3. Southsun Cove — Armored Scale   [Go →]
  4. Cursed Shore — Powerful Blood     [Go →]
  5. Fireheart Rise — Vicious Fang     [Go →]

v1.10.2: NO prices are shown in the addon any more (Audrey's ask) — no gold values, no price footer. The ranking ORDER is still the 17 Nov 2026 snapshot order; the gold values that produced it live only in the baked tables below, not in the UI.
```

- Header: gold, same style as the PSNA header. "Map Bonus Rewards — Week 4" (week number computed at runtime from the UTC date, Thursday 20:00 boundary).
- Sub-line (small, muted): "Best Central Tyria maps this week · resets Thu 20:00 UTC".
- Each row: rank, map name, the week's common / headline reward (short name only — "Shiny Bauble", "Vicious Claw", "Armored Scale", "Powerful Blood", "Vicious Fang"). v1.10.2: NO gold value shown. No per-reward counts, no "44×" — that is internal detail.
- Click a row (or a small "Go" affordance on the row) → copies the entry waypoint's chat code, exactly like clicking a search result. No separate copy string with the map name — the waypoint code is the useful part, and it keeps the behaviour consistent with the rest of the addon. (If a copy string is wanted, use the same pattern as the rest of the addon: just the `[&...]` code.)
- Footer: none since v1.10.2 (was "Prices from 17 Nov 2026 — check /wiki mbrp for live values." — removed with the prices).
- Do NOT show: the full 40-reward list per map, per-reward counts, instant-sell vs TP-list both (pick TP-list net, one number), or any "entries / tags" counts.
- Window size: the section adds ~6 short lines; if the window grows, keep the search box + results as the dominant area — this section is a compact header block like PSNA, not a second results list.

## Build data needed (for the builder)

1. Week-number function: UTC date → Central Tyria week 1–8, Thursday 20:00 UTC boundary, anchor Thu 24 Jul 2025 = Week 8. (Same style as the PSNA weekday table, but weekly not daily.)
2. Baked table, all 8 weeks × top maps: for each week, the top 5 Central Tyria maps with (a) map name, (b) headline/common reward name, (c) full-track TP value at build time, (d) entry waypoint chat code. The Week 4 row is fully verified above. Weeks 1, 2, 3, 5, 6, 7, 8 need the same treatment: take the top 5 from GW TODOBOX / wiki mbrp for that week (selectable by week on gw-todo.vercel.app/weekly) and verify each map's entry waypoint in pois.json. Do NOT reuse Week 4's ranking for other weeks — every week has a different top 5.
   - Known anchor for the cycle best: Week 8 top is Fireheart Rise, 18g 11s 77c (live, GW TODOBOX).
3. Tag the 5 entry waypoints with `map bonus` / `map bonus rewards` phrases in tags.json (Pagga's, Earthshake, Pearl Islet, Penitent, Citadel of Flame) so a map-name search returns them; run apply_tags.py + test_search.py to validate. Penitent Waypoint is currently untagged — it will need a new tag entry.
4. Weekly maintenance: the *tracks* never change, but the *ranking + gold values* should be re-checked each Thursday after 20:00 UTC (prices move). If the builder only bakes Week 4, the section goes stale on Thu 19 Nov 20:00 UTC — either bake all 8 weeks, or ship Week 4 with a clear "valid until 19 Nov 20:00 UTC" and a weekly data update. Baking all 8 weeks is the right call; the ranking per week is then fixed until TP prices shift it, and the date-stamp covers that.
5. No network fetch in v1: do not add a live TP fetch for this section. The offline baked-table design matches how PSNA already works in the addon.

## Verdict

- **Fixed rotation: YES.** 8-week cycle, Thursday 20:00 UTC, fixed per-map tracks — bakeable offline exactly like PSNA. No live fetch needed to know the rewards.
- **"Best" ranking: price-dependent, snapshot only.** The ranking ORDER baked into the addon is the 17 Nov 2026 snapshot order; prices are no longer displayed in the addon (v1.10.2) — the values below are the record of how that order was computed. Re-check weekly. Do not claim it is live.
- **Current week (verified): Week 4, 12–19 Nov 2026. Best: Malchor's Leap (17g 37s), then Frostgorge Sound (12g 20s), Southsun Cove (10g 62s), Cursed Shore (9g 23s), Fireheart Rise (7g 46s)** — all five entry waypoints verified in the dataset.
- **Scope: Central Tyria top 5 only.** HoT/PoF/EoD/SotO tracks are fixed or currency-based and are not ranked here.

## Baked tables — all 8 weeks (computed 17 Nov 2026, v1.9)

Computed from the GW2 Wiki Template:Map bonus reward data (full 40-reward
tables for all 21 Central Tyria maps) and live /v2/commerce/prices fetched
17 Nov 2026 ~07:35 UTC, net of the 15% TP tax (vendor value for vendor-only
items, 0 for account-bound items). Headline = highest-value single item.
TODOBOX only ranks 5 maps; this ranking covers all 21, so it differs where
an untracked map wins. Cross-checks: Week 4 top 3 and Week 8 #1 match TODOBOX.

### Week 1

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Mount Maelstrom | Shiny Bauble | 15g 57s 55c | Maelstrom's Waypoint `[&BM0CAAA=]` |
| 2 | Malchor's Leap | Elaborate Totem | 10g 84s 76c | Pagga's Waypoint `[&BKYCAAA=]` |
| 3 | Straits of Devastation | Vial of Powerful Blood | 10g 34s 40c | Fort Trinity Waypoint `[&BO4CAAA=]` |
| 4 | Southsun Cove | Ancient Bone | 10g 04s 36c | Pearl Islet Waypoint `[&BNUGAAA=]` |
| 5 | Diessa Plateau | Shiny Bauble | 9g 36s 04c | Bloodcliff Waypoint `[&BMQDAAA=]` |

6th: Dredgehaunt Cliffs (9g 14s 39c).

### Week 2

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Frostgorge Sound | Vial of Powerful Blood | 14g 43s 92c | Earthshake Waypoint `[&BHoCAAA=]` |
| 2 | Straits of Devastation | Shiny Bauble | 14g 40s 00c | Fort Trinity Waypoint `[&BO4CAAA=]` |
| 3 | Kessex Hills | Shiny Bauble | 13g 77s 80c | Cereboth Waypoint `[&BBIAAAA=]` |
| 4 | Blazeridge Steppes | Shiny Bauble | 13g 43s 56c | Lowland Burns Waypoint `[&BE4DAAA=]` |
| 5 | Southsun Cove | Vicious Fang | 10g 85s 12c | Pearl Islet Waypoint `[&BNUGAAA=]` |

6th: Cursed Shore (9g 91s 26c).

### Week 3

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Bloodtide Coast | Shiny Bauble | 14g 18s 76c | Firthside Vigil Waypoint `[&BKoBAAA=]` |
| 2 | Frostgorge Sound | Shiny Bauble | 13g 56s 54c | Earthshake Waypoint `[&BHoCAAA=]` |
| 3 | Brisban Wildlands | Shiny Bauble | 13g 32s 14c | Gallowfields Waypoint `[&BGMAAAA=]` |
| 4 | Straits of Devastation | Vicious Claw | 13g 19s 94c | Fort Trinity Waypoint `[&BO4CAAA=]` |
| 5 | Malchor's Leap | Vial of Powerful Blood | 10g 63s 60c | Pagga's Waypoint `[&BKYCAAA=]` |

6th: Fireheart Rise (10g 60s 18c).

### Week 4

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Malchor's Leap | Shiny Bauble | 17g 36s 94c | Pagga's Waypoint `[&BKYCAAA=]` |
| 2 | Frostgorge Sound | Vicious Claw | 11g 83s 54c | Earthshake Waypoint `[&BHoCAAA=]` |
| 3 | Southsun Cove | Armored Scale | 10g 36s 69c | Pearl Islet Waypoint `[&BNUGAAA=]` |
| 4 | Mount Maelstrom | Ancient Bone | 10g 36s 66c | Maelstrom's Waypoint `[&BM0CAAA=]` |
| 5 | Timberline Falls | Shiny Bauble | 9g 36s 74c | Gentle River Waypoint `[&BFACAAA=]` |

6th: Gendarran Fields (9g 09s 04c).

### Week 5

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Cursed Shore | Shiny Bauble | 16g 34s 67c | Penitent Waypoint `[&BBkDAAA=]` |
| 2 | Iron Marches | Shiny Bauble | 14g 37s 97c | Bulwark Waypoint `[&BOwBAAA=]` |
| 3 | Lornar's Pass | Shiny Bauble | 13g 74s 10c | Durmand Priory Waypoint `[&BOkAAAA=]` |
| 4 | Fireheart Rise | Elaborate Totem | 13g 18s 86c | The Citadel of Flame Waypoint `[&BEAFAAA=]` |
| 5 | Frostgorge Sound | Powerful Venom Sac | 11g 26s 36c | Earthshake Waypoint `[&BHoCAAA=]` |

6th: Malchor's Leap (9g 97s 60c).

### Week 6

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Southsun Cove | Shiny Bauble | 14g 74s 00c | Pearl Islet Waypoint `[&BNUGAAA=]` |
| 2 | Fields of Ruin | Shiny Bauble | 13g 31s 34c | Rosko's Campsite Waypoint `[&BNgAAAA=]` |
| 3 | Cursed Shore | Vicious Claw | 11g 68s 88c | Penitent Waypoint `[&BBkDAAA=]` |
| 4 | Straits of Devastation | Vicious Fang | 10g 96s 78c | Fort Trinity Waypoint `[&BO4CAAA=]` |
| 5 | Mount Maelstrom | Elaborate Totem | 10g 31s 96c | Maelstrom's Waypoint `[&BM0CAAA=]` |

6th: Malchor's Leap (9g 75s 44c).

### Week 7

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Southsun Cove | Vicious Claw | 11g 25s 10c | Pearl Islet Waypoint `[&BNUGAAA=]` |
| 2 | Fireheart Rise | Vial of Powerful Blood | 10g 90s 72c | The Citadel of Flame Waypoint `[&BEAFAAA=]` |
| 3 | Mount Maelstrom | Armored Scale | 10g 21s 94c | Maelstrom's Waypoint `[&BM0CAAA=]` |
| 4 | Cursed Shore | Powerful Venom Sac | 9g 33s 44c | Penitent Waypoint `[&BBkDAAA=]` |
| 5 | Frostgorge Sound | Vicious Fang | 9g 14s 10c | Earthshake Waypoint `[&BHoCAAA=]` |

6th: Straits of Devastation (7g 58s 80c).

### Week 8

| Rank | Map | Headline reward | Full-track TP net | Entry waypoint |
|---|---|---|---|---|
| 1 | Fireheart Rise | Shiny Bauble | 18g 12s 32c | The Citadel of Flame Waypoint `[&BEAFAAA=]` |
| 2 | Harathi Hinterlands | Shiny Bauble | 13g 49s 58c | Junction Camp Waypoint `[&BLAAAAA=]` |
| 3 | Cursed Shore | Ancient Bone | 13g 38s 58c | Penitent Waypoint `[&BBkDAAA=]` |
| 4 | Frostgorge Sound | Elaborate Totem | 9g 63s 86c | Earthshake Waypoint `[&BHoCAAA=]` |
| 5 | Straits of Devastation | Armored Scale | 9g 42s 45c | Fort Trinity Waypoint `[&BO4CAAA=]` |

6th: Snowden Drifts (9g 17s 84c).
