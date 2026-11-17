#!/usr/bin/env python3
"""Test harness: mirrors src/entry.cpp Search() ranking exactly, against
data/pois.json (with tags merged by tools/apply_tags.py).

 - rank 0: every token is a substring of "<display> <map> <region>"
  (lowercased) — v1.6: region is in the haystack, so "castora" (a region,
  not a map) finds all 205 Castora entries
- rank 1: every token matches ONE tag phrase (whole word, or substring
  for tokens of 3+ letters) — see TokenMatchesTagPhrase in entry.cpp
- sort: rank, then same-map (skipped here: no MumbleLink), then
  display name, then map name.
- v1.7 PSNA: "daily psna" / "psna today" / "today psna" and
  "psna <weekday>" are intercepted BEFORE the name/tag search (mirroring
  src/entry.cpp) and return exactly that day's 6 agents in agent order
  (Verma, Derwena, Fox, Mehem, Yana, Katelyn), with the PSNA day
  computed from a UTC time with the 08:00 UTC cutoff. Plain "psna" /
  "pact supply" falls through to the tag search and returns all 40
  unique PSNA locations (42 agent-day slots; 2 waypoints repeat).
Run: python3 tools/test_search.py [query ...]
"""
import json, os, sys, pathlib
from datetime import datetime, timezone
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(BASE, "data", "pois.json")))
rows = data["entries"]

# --- v1.7 PSNA rotation table (mirrors kPsnaLinks in src/entry.cpp) ---
# Rows: Monday..Sunday. Columns (agent order): Verma, Derwena, Fox,
# Mehem, Yana, Katelyn. Sources: GW2 Wiki PSNA table, Doncpauli
# (2026-11-17), gw2timer gist — see tools/add_v17_psna.py.
PSNA_LINKS = [
    ["[&BA8CAAA=]", "[&BKYBAAA=]", "[&BEwDAAA=]", "[&BIcHAAA=]", "[&BNIEAAA=]", "[&BIMCAAA=]"],
    ["[&BIMBAAA=]", "[&BBkAAAA=]", "[&BEgAAAA=]", "[&BH8HAAA=]", "[&BKgCAAA=]", "[&BGQCAAA=]"],
    ["[&BPEBAAA=]", "[&BKYAAAA=]", "[&BMIBAAA=]", "[&BH4HAAA=]", "[&BP0CAAA=]", "[&BDgDAAA=]"],
    ["[&BOcBAAA=]", "[&BIMAAAA=]", "[&BF0AAAA=]", "[&BKsHAAA=]", "[&BO4CAAA=]", "[&BF0GAAA=]"],
    ["[&BNMAAAA=]", "[&BNUGAAA=]", "[&BMwCAAA=]", "[&BJQHAAA=]", "[&BJsCAAA=]", "[&BHsBAAA=]"],
    ["[&BBABAAA=]", "[&BJIBAAA=]", "[&BLkCAAA=]", "[&BH8HAAA=]", "[&BBEDAAA=]", "[&BEICAAA=]"],
    ["[&BCECAAA=]", "[&BC0AAAA=]", "[&BDoBAAA=]", "[&BIkHAAA=]", "[&BO4CAAA=]", "[&BIUCAAA=]"],
]
PSNA_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
PSNA_DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PSNA_AGENTS = ["Verma Giftrender", "Lady Derwena", "The Fox",
               "Mehem the Traveled", "Specialist Yana", "Despina Katelyn"]
# Expected display names per day, in agent order (same as PSNA_LINKS).
PSNA_DAY_DISPLAYS = [
    ["Haymal Gore", "Marshwatch Haven Waypoint", "Lionguard Waystation Waypoint", "Restoration Refuge", "Rally Waypoint", "Ridgerock Camp Waypoint"],
    ["Temperus Point Waypoint", "Garenhoff", "Desider Atum Waypoint", "Camp Resolve Waypoint", "Waste Hollows Waypoint", "Travelen's Waypoint"],
    ["Ferrusatos Village", "Shieldbluff Waypoint", "Swampwatch Post", "Town of Prosperity", "Caer Shadowfain", "Mennerheim"],
    ["Village of Scalecatch Waypoint", "Altar Brook Trading Post", "Wendon Waypoint", "Blue Oasis", "Fort Trinity Waypoint", "Rocklair"],
    ["Hawkgates Waypoint", "Pearl Islet Waypoint", "Bard's Waypoint", "Repair Station", "Shelter Docks", "Dolyak Pass Waypoint"],
    ["Bovarin Estate", "Vigil Keep Waypoint", "Gallant's Folly", "Camp Resolve Waypoint", "Augur's Torch", "Balddistead"],
    ["Snow Ridge Camp Waypoint", "Mudflat Camp", "Mabon Waypoint", "Azarr's Arbor", "Fort Trinity Waypoint", "Blue Ice Shining Waypoint"],
]
PSNA_ALL_DISPLAYS = sorted({d for day in PSNA_DAY_DISPLAYS for d in day})

def psna_weekday_index(dt):
    """0 = Monday .. 6 = Sunday for a UTC datetime. Locations change at
    08:00 UTC: before that hour the previous day's set still applies."""
    idx = dt.weekday()
    if dt.hour < 8:
        idx = (idx - 1) % 7
    return idx

def build_daily_list_string(day_idx):
    """Today's 6 PSNA chat links, one space-separated line (71 chars)."""
    return " ".join(PSNA_LINKS[day_idx])

def display_name(e):
    name = e.get("name") or ""
    if name:
        return name
    if e["type"] == "vista":
        return f"Vista - {e['map_name']}"
    return f"Waypoint - {e['map_name']}"

def token_matches_hay(hay, token):
    if len(token) >= 3:
        return token in hay
    return token in hay.split()

def token_matches_tag_phrase(phrase, token):
    words = phrase.split()
    if token in words:
        return True
    if len(token) >= 3 and token in phrase:
        return True
    return False

def find_matching_tag(tags, tokens):
    for phrase in tags:
        if all(token_matches_tag_phrase(phrase, t) for t in tokens):
            return phrase
    return ""

def psna_day_search(query, now):
    """v1.7 mirror of the Search() interception in src/entry.cpp.
    Returns the day's 6 results in agent order, or None if the query is
    not a PSNA-day query (plain "psna" falls through to tag search)."""
    tokens = query.lower().split()
    is_psna = "psna" in tokens or ("pact" in tokens and "supply" in tokens)
    if not is_psna:
        return None
    weekday = next((i for i, d in enumerate(PSNA_DAYS) if d in tokens), -1)
    is_daily = "daily" in tokens or "today" in tokens
    if weekday < 0 and not is_daily:
        return None
    day = weekday if weekday >= 0 else psna_weekday_index(now)
    by_link = {e["chat_link"]: e for e in rows}
    out = []
    for i, link in enumerate(PSNA_LINKS[day]):
        e = by_link.get(link)
        if e is None:
            continue
        label = (f"{'Daily PSNA' if weekday < 0 else 'PSNA'} — "
                 f"{PSNA_DAY_NAMES[day]}: {PSNA_AGENTS[i]}")
        out.append((0, label, display_name(e), e))
    return out

def search(query, now=None):
    if now is None:
        now = datetime.now(timezone.utc)
    day_res = psna_day_search(query, now)
    if day_res is not None:
        return day_res
    tokens = query.lower().split()
    out = []
    for e in rows:
        if e["type"] not in ("waypoint", "landmark", "vista"):
            continue
        display = display_name(e)
        hay = f"{display} {e['map_name']} {e.get('region','')}".lower()
        if all(token_matches_hay(hay, t) for t in tokens):
            out.append((0, "", display, e))
        else:
            tags = [t.lower() for t in e.get("tags", [])]
            tag = find_matching_tag(tags, tokens)
            if tag:
                out.append((1, tag, display, e))
    out.sort(key=lambda r: (r[0], r[2], r[3]["map_name"]))
    return out

CASES = [
    # v1.4 multi-spot: full expected lists, alphabetical (rank-1 tag matches
    # sort by display name). "flax" must return ALL 9 farm spots.
    ("flax", ["Allied Encampment Waypoint", "Eastwatch Waypoint", "Ground Zero Waypoint",
              "Heathen's Hold Waypoint", "Jaka Itzel Waypoint", "Ogre Camp Waypoint",
              "Soulkeeper's Airship Waypoint", "Westwatch Waypoint", "Yatendi Village Waypoint"]),
    ("flax seeds", ["Allied Encampment Waypoint", "Eastwatch Waypoint", "Ground Zero Waypoint",
              "Heathen's Hold Waypoint", "Jaka Itzel Waypoint", "Ogre Camp Waypoint",
              "Soulkeeper's Airship Waypoint", "Westwatch Waypoint", "Yatendi Village Waypoint"]),
    ("flax farm", ["Allied Encampment Waypoint", "Eastwatch Waypoint", "Ground Zero Waypoint",
              "Heathen's Hold Waypoint", "Jaka Itzel Waypoint", "Ogre Camp Waypoint",
              "Soulkeeper's Airship Waypoint", "Westwatch Waypoint", "Yatendi Village Waypoint"]),
    ("rich mithril", ["Doric's Waypoint", "Meddler's Waypoint", "Path of Starry Skies Waypoint",
              "Pearl Islet Waypoint", "Shipwreck Rock Waypoint", "Slough of Despond Waypoint",
              "The Citadel of Flame Waypoint", "Valley of Lyss Waypoint", "Verdance Waypoint"]),
    ("rich orichalcum", ["Anchorage Waypoint", "Blighted Arch Waypoint", "Dimotiki Waypoint",
              "Doric's Waypoint", "Drakkar Waypoint", "Earthshake Waypoint", "Gavbeorn's Waypoint",
              "Lair of the Forgotten Waypoint", "Lakeside Bazaar Waypoint", "Meddler's Waypoint",
              "Murmur Waypoint", "Pagga's Waypoint", "Pursuit Pass Waypoint",
              "Red Leaf Retreat Waypoint", "Spearmarshal's Lament"]),
    ("rich copper", ["Ashford Waypoint", "Caledon Haven Waypoint", "Claypool Waypoint",
              "Crossroads Haven Waypoint", "Desider Atum Waypoint"]),
    ("rich silver", ["Cereboth Waypoint", "Durmand Priory Waypoint", "Gallowfields Waypoint",
              "Provern Shore Waypoint", "Rosko's Campsite Waypoint"]),
    ("rich gold", ["Forlorn Gate Waypoint", "Graupel Waypoint", "Junction Camp Waypoint",
              "Lowland Burns Waypoint"]),
    ("rich iron", ["Cereboth Waypoint", "Durmand Priory Waypoint", "Gallowfields Waypoint",
              "Graupel Waypoint", "Helliot Mine Waypoint", "Junction Camp Waypoint",
              "Lowland Burns Waypoint"]),
    ("rich platinum", ["Ashen Waypoint", "Bulwark Waypoint", "Firthside Vigil Waypoint",
              "Gentle River Waypoint", "Ocean's Gullet Waypoint", "The Citadel of Flame Waypoint"]),
    ("quartz", ["Destiny's Gorge Waypoint", "Prosperity Waypoint", "Repair Station Waypoint",
              "Vine Bridge Waypoint"]),
    ("rich quartz", ["Destiny's Gorge Waypoint"]),
    ("elder wood", ["Anchorage Waypoint", "Camp Reclamation Waypoint", "Earthshake Waypoint",
              "Pagga's Waypoint", "Pearl Islet Waypoint", "Waywarde Waypoint"]),
    ("hard wood", None),  # rank-0 name matches (Iceshard Trail / Vloxen Shards in Drizzlewood Coast) sort above the tag matches; see INCLUSION_CASES
    ("soft wood", ["Cereboth Waypoint", "Forlorn Gate Waypoint", "Gallowfields Waypoint",
              "Oldgate Waypoint", "Provern Shore Waypoint"]),
    ("seasoned wood", ["Graupel Waypoint", "Wynchona Rally Point Waypoint"]),
    ("ore", None),  # just check count / no crash
    ("tequatl", ["Splintered Coast Waypoint"]),
    ("teq", ["Splintered Coast Waypoint"]),
    ("shatterer", ["Lowland Burns Waypoint"]),
    ("shadow behemoth", ["Godslost Waypoint", "Swamplost Haven Waypoint"]),
    ("claw of jormag", ["Earthshake Waypoint"]),
    ("world boss", None),
    ("triple trouble", ["Firthside Vigil Waypoint"]),
    ("tt", ["Firthside Vigil Waypoint"]),
    ("octovine", ["Eastwatch Waypoint", "Northwatch Waypoint", "Southwatch Waypoint", "Westwatch Waypoint"]),  # all four Tarir lanes are valid entry points
    ("battle in tarir", ["Eastwatch Waypoint", "Northwatch Waypoint", "Southwatch Waypoint", "Westwatch Waypoint"]),
    ("chak gerent", ["Ley-Line Confluence Waypoint"]),
    ("drakkar", ["Drakkar Waypoint", "Still Waters Speaking Waypoint"]),  # Frostgorge waypoint literally named Drakkar is the name match; Bjora meta is the tag match
    ("jaka itzel", ["Jaka Itzel Waypoint"]),
    ("caledon haven", None),
    ("nonsensexyz", []),
    # v1.3 — one per new category (at least)
    ("mordrem vinewrath", ["Camp Resolve Waypoint"]),
    ("ley-line anomaly", ["Provern Shore Waypoint"]),
    ("raid", ["Bloodcoast Ward Waypoint"]),
    ("loreclaw expanse", ["Loreclaw Waypoint"]),
    ("goemm's lab", ["Cuatl Waypoint"]),
    ("morgan's leap", ["Spiral Waypoint"]),
    ("bank", ["Accountancy Waypoint", "Ashford Waypoint", "Claypool Waypoint",
              "Factorium Waypoint", "Ministers Waypoint", "Trade Commons Waypoint",
              "Trader's Forum Waypoint", "Upper Commons Waypoint"]),
    ("guild bank", ["Accountancy Waypoint", "Ashford Waypoint", "Claypool Waypoint",
              "Factorium Waypoint", "Ministers Waypoint", "Trade Commons Waypoint",
              "Trader's Forum Waypoint", "Upper Commons Waypoint"]),
    ("mystic forge", ["PvP Lobby Waypoint", "Trader's Forum Waypoint"]),
    ("trading post", None),  # rank-0 name matches (Altar Brook / Hanto Trading Post landmarks) sort above the tag matches; see INCLUSION_CASES
    ("laurel merchant", ["Accountancy Waypoint", "Amnoon Waypoint", "Arborstone Waypoint",
              "Balthazar Waypoint", "Bloodcoast Ward Waypoint", "Fort Marriner Waypoint",
              "Great Lodge Waypoint", "Memorial Waypoint", "Snowblind Waypoint",
              "Trader's Forum Waypoint", "Upper Commons Waypoint"]),
    ("armorsmith", ["Accountancy Waypoint", "Ashford Waypoint", "Claypool Waypoint",
              "Desider Atum Waypoint", "Factorium Waypoint", "Mabon Waypoint",
              "Ministers Waypoint", "Trade Commons Waypoint", "Trader's Forum Waypoint",
              "Upper Commons Waypoint"]),
    ("chef", ["Accountancy Waypoint", "Ashford Waypoint", "Claypool Waypoint",
              "Desider Atum Waypoint", "Factorium Waypoint", "Mabon Waypoint",
              "Ministers Waypoint", "Trade Commons Waypoint", "Trader's Forum Waypoint",
              "Upper Commons Waypoint"]),
    ("merchant", None),  # 19 results: service hubs + laurel merchants
    ("chest run", ["Akk Wilds Waypoint", "Order of Whispers Camp Waypoint", "Wanderer's Waypoint"]),
    ("casino blitz", ["Amnoon Waypoint"]),
    ("kaineng blackout", ["Lutgardis Plaza Waypoint"]),
    ("meta event", None),
    ("jumping puzzle", None),
    ("dungeon", None),
    # v1.6 — jumping puzzles (wiki list, all expansions)
    ("crimson plateau", ["Breached Wall Waypoint", "Redreave Mill Waypoint"]),
    ("branded mine", ["Tenaebron Waypoint"]),
    ("trials of the tengu", ["Monastery Waypoint"]),
    ("wind through the walls", ["Lutgardis Plaza Waypoint"]),
    ("king jalis's refuge", ["Snowhawk Landing Waypoint"]),
    ("winter wonderland", ["Crown Pavilion Waypoint"]),
    ("obsidian sanctum", ["Obsidian Sanctum Waypoint", "Obsidian Sanctum Waypoint", "Obsidian Sanctum Waypoint"]),
    ("mistlock mountaineer", ["Fort Marriner Waypoint"]),
    ("traversing the titan", ["Hidden Nodule Waypoint"]),
    ("treetop beehive", ["Harvest Den Waypoint"]),
    ("abaddon's ascent", ["Camp Reclamation Waypoint"]),
    # v1.6 — adventures (HoT / PoF / EoD / SotO / Janthir / VoE / festivals)
    ("flying circus", ["Mellaggan's Valor Waypoint"]),
    ("sanctum scramble", ["Forgotten City Waypoint"]),
    ("tendril torchers", ["Shipwreck Peak Waypoint"]),
    ("the floor is lava", ["Wanderer's Waypoint"]),
    ("jade bot rally", ["Garden Heights Waypoint", "Luxon Terminus Waypoint", "Mori Village Waypoint"]),
    ("skyscale target practice", ["Beacon of Ages Waypoint", "Tower Courtyard Waypoint"]),
    ("flying fireworks", ["Hullgarden Pier Waypoint"]),
    ("warclaw run", ["Forager's Hunt Waypoint", "Journeykin Outpost Waypoint"]),
    ("griffon master", None),
    ("roller beetle", None),
    # v1.6 — collections (Dive Master, 36 of 38 locations)
    ("dive master", None),
    ("dive goggles sanctum harbor", ["Diverse Ledges Waypoint"]),
    ("diving goggles wizard's fief", ["Cereboth Waypoint"]),
    # v1.6 — mini dungeons (20 of 22; Trial of the Elders and From Ruins
    # to Riches have no verified nearest waypoint and are not tagged)
    ("bad neighborhood", ["Ojon's Lumbermill Waypoint"]),
    ("flame temple tombs", ["Font of Rhand Waypoint"]),
    ("forsaken fortune", ["Wyrmblood Waypoint"]),
    ("tears of itlaocol", ["Falias Thorp Waypoint"]),
    ("goemm's lab", ["Cuatl Waypoint"]),
    ("branded mine", ["Tenaebron Waypoint"]),
    # v1.6 — region search
    ("castora", None),
    ("eternity's garden", None),
    ("creeping crevasse", ["Shipwreck Peak Waypoint"]),
    ("janthir", None),
    ("heart of maguuma", None),
    # v1.7 — PSNA agent spot checks (alphabetical; the CASES runner also
    # accepts the sorted order). Verma/Derwena/Fox/Katelyn: 7 distinct
    # spots each. Mehem/Yana: 6 unique (Camp Resolve repeats Tue+Sat,
    # Fort Trinity repeats Thu+Sun, so 7 slots -> 6 entries).
    ("verma", ["Bovarin Estate", "Ferrusatos Village", "Hawkgates Waypoint",
               "Haymal Gore", "Snow Ridge Camp Waypoint", "Temperus Point Waypoint",
               "Village of Scalecatch Waypoint"]),
    ("verma giftrender", ["Bovarin Estate", "Ferrusatos Village", "Hawkgates Waypoint",
               "Haymal Gore", "Snow Ridge Camp Waypoint", "Temperus Point Waypoint",
               "Village of Scalecatch Waypoint"]),
    ("mehem", ["Azarr's Arbor", "Blue Oasis", "Camp Resolve Waypoint",
               "Repair Station", "Restoration Refuge", "Town of Prosperity"]),
    ("the fox", ["Bard's Waypoint", "Desider Atum Waypoint", "Gallant's Folly",
               "Lionguard Waystation Waypoint", "Mabon Waypoint", "Swampwatch Post",
               "Wendon Waypoint"]),
    ("specialist yana", ["Augur's Torch", "Caer Shadowfain", "Fort Trinity Waypoint",
               "Rally Waypoint", "Shelter Docks", "Waste Hollows Waypoint"]),
    ("lady derwena", ["Altar Brook Trading Post", "Garenhoff", "Marshwatch Haven Waypoint",
               "Mudflat Camp", "Pearl Islet Waypoint", "Shieldbluff Waypoint",
               "Vigil Keep Waypoint"]),
    ("despina katelyn", ["Balddistead", "Blue Ice Shining Waypoint", "Dolyak Pass Waypoint",
               "Mennerheim", "Ridgerock Camp Waypoint", "Rocklair", "Travelen's Waypoint"]),
    ("katelyn", ["Balddistead", "Blue Ice Shining Waypoint", "Dolyak Pass Waypoint",
               "Mennerheim", "Ridgerock Camp Waypoint", "Rocklair", "Travelen's Waypoint"]),
]

# v1.6 — exact result counts for the big generic searches. A count change
# means a tag was added or lost; check it before assuming a bug.
COUNT_CASES = [
    ("jumping puzzle", 77),  # was 72; +5 Castora JPs 2026-11-17 (Temple of Abnegation, Doyen's Adytum/Coleopteran, Hall of Assemblage/Inquest Cache, Soaring Copse, Orb Cavern via Inquest Supply Cavern)
    ("adventure", 71),  # was 67; +4 Castora adventures 2026-11-17 (Skimmer Relic Scour, Aetherlocation Detective, Kitshark, Serpent Simulator via Primus Minor POI) — 70 adventure-tagged entries + the rank-0 "Waypoint - Super Adventure Box" name match
    ("castora", 205),
    ("eternity's garden", 50),
    ("creeping crevasse", 1),
    ("dive master", 36),
    ("collection", 37),  # 36 Dive Master + Crystal Collection adventure
    ("janthir", 190),
    ("heart of maguuma", 204),
    ("griffon expert", 9),
    ("griffon master", 8),  # Jahai Master unverified; Sandswept has Expert only
    ("mini dungeon", 26),  # was 23; +3 in 2026-11-17 full sweep (From Ruins to Riches, Hall of Assemblage; Trial of the Elders, Sanctuary of Ione POI; Temple of Abnegation mini dungeon) — 22 mini dungeons, i.e. all 22 on the wiki list; Hidden Garden has 4 access waypoints
    ("hidden garden", 6),  # 4 access waypoints + Govoran (JP tag) + Hidden Cellar POI (name match)
    # v1.7 — PSNA: 42 agent-day slots, 40 unique locations (2 repeats)
    ("psna", 40),
    ("pact supply", 40),
    ("pact supply network agent", 40),
    ("pact supply network", 40),
    ("mapping materials", 40),
    ("daily psna", 6),  # NOTE: count only — which 6 depends on "now"; the
    # exact day's set is asserted in PSNA_DAY_CASES below with fixed times
]

# v1.7 — PSNA-day queries with FIXED UTC times (query, now_utc, expected
# displays in agent order: Verma, Derwena, Fox, Mehem, Yana, Katelyn).
# Mon 2026-11-16 19:00 PST == Tue 2026-11-17 03:00 UTC -> still Monday's
# set (locations change 08:00 UTC, not midnight). Tue 01:00 PST ==
# 09:00 UTC -> Tuesday's set. 07:59 UTC -> previous day; 08:00 -> new day.
PSNA_DAY_CASES = [
    ("daily psna", datetime(2026, 11, 17, 3, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[0]),
    ("psna today", datetime(2026, 11, 17, 3, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[0]),
    ("today psna", datetime(2026, 11, 17, 9, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[1]),
    ("daily psna", datetime(2026, 11, 17, 9, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[1]),
    ("daily psna", datetime(2026, 11, 17, 8, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[1]),
    ("daily psna", datetime(2026, 11, 17, 7, 59, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[0]),
    ("daily psna", datetime(2026, 11, 16, 0, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[6]),
    ("psna monday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[0]),
    ("psna tuesday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[1]),
    ("psna wednesday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[2]),
    ("psna thursday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[3]),
    ("psna friday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[4]),
    ("psna saturday", datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[5]),
    ("psna sunday", datetime(2026, 11, 16, 12, 0, tzinfo=timezone.utc), PSNA_DAY_DISPLAYS[6]),
]

# v1.7 — "Copy daily list" string: exact codes, agent order, no dupes,
# 71 chars (6 x 11 + 5 spaces) — fits GW2 chat's 199-char line limit.
DAILY_LIST_CASES = [
    (datetime(2026, 11, 17, 3, 0, tzinfo=timezone.utc),
     "[&BA8CAAA=] [&BKYBAAA=] [&BEwDAAA=] [&BIcHAAA=] [&BNIEAAA=] [&BIMCAAA=]"),
    (datetime(2026, 11, 17, 9, 0, tzinfo=timezone.utc),
     "[&BIMBAAA=] [&BBkAAAA=] [&BEgAAAA=] [&BH8HAAA=] [&BKgCAAA=] [&BGQCAAA=]"),
    (datetime(2026, 11, 17, 7, 59, tzinfo=timezone.utc),
     "[&BA8CAAA=] [&BKYBAAA=] [&BEwDAAA=] [&BIcHAAA=] [&BNIEAAA=] [&BIMCAAA=]"),
]

# Tag results that are correct but NOT first: a rank-0 name/map match
# (e.g. every POI on the Dragon's Stand map) legitimately sorts above a
# rank-1 tag match. These cases assert inclusion, not position.
INCLUSION_CASES = [
    # Tag results that are correct but NOT first: a rank-0 name/map match
    # (e.g. every POI on the Dragon's Stand map) legitimately sorts above a
    # rank-1 tag match. These cases assert inclusion, not position.
    ("hard wood", ["Ashen Waypoint", "Bulwark Waypoint", "Caer Brier Waypoint",
              "Gentle River Waypoint", "The Citadel of Flame Waypoint"]),
    ("trading post", ["Accountancy Waypoint", "Ashford Waypoint", "Claypool Waypoint",
              "Factorium Waypoint", "Ministers Waypoint", "Smokestead Waypoint",
              "Trade Commons Waypoint", "Trader's Forum Waypoint", "Upper Commons Waypoint"]),
    ("dragon's stand", ["Pact Base Camp Waypoint"]),
    ("dragon's end", ["Harvest Complex Waypoint"]),
    ("dragonstorm", ["Eye of the North Waypoint"]),
    ("ascalonian catacombs", ["Ascalonian Catacombs Waypoint"]),
    ("fractals", ["Fort Marriner Waypoint"]),
    ("forging steel", ["Eye of the North Waypoint"]),
    ("convergence", ["Tower Courtyard Waypoint"]),
    ("bastion of the penitent", ["Depths of the Maw Waypoint"]),
    ("harvest temple", ["Arborstone Waypoint"]),
    ("verdant brink night", ["Jaka Itzel Waypoint"]),
    ("titanic voyage", ["Mantle's Arrival Waypoint"]),
    # v1.6 — mini dungeons whose name is also a landmark POI: the POI is
    # rank-0, the tagged waypoint follows — assert inclusion, not position
    ("spirit vestibule", ["Village Waypoint"]),
    ("valdhertz crypts", ["Mori Village Waypoint"]),
    ("vasburg armory", ["Jade Gate Waypoint"]),
    ("'booter's path", ["Pub Canach Waypoint"]),
    ("palawadan", ["Champion's Dawn Waypoint"]),
    # v1.9 — materials / mob tags (docs/mob-and-poultry-tags.md) and
    # map-bonus / rift tags: assert inclusion, not position
    ("rift", ["Jaka Itzel Waypoint"]),
    ("kryptis rift", ["Jaka Itzel Waypoint"]),
    ("titanspawn rift", ["Harvest Den Waypoint"]),
    ("castora rift", ["Pilgrim's Rest Waypoint"]),
    ("map bonus", ["Pagga's Waypoint"]),
    ("poultry", ["Amnoon Waypoint"]),
    ("moa", ["Bloodcliff Waypoint"]),
    # v1.9 — guild missions + mount races (docs/guild-missions-mount-races.md)
    # and daily activities (docs/daily-activities.md): assert inclusion
    ("guild rush", ["Durmand Priory Waypoint"]),
    ("guild challenge", ["Tumok's Waypoint"]),
    ("guild puzzle", ["Angvar's Trove Waypoint"]),
    ("guild bounty", ["Guild Initiative Headquarters"]),
    ("guild trek", ["Guild Initiative Headquarters"]),
    ("roller beetle race", ["Nageling Waypoint"]),
    ("race to the finish", ["Amnoon Waypoint"]),
    ("mount race", ["Nageling Waypoint"]),
    ("crab toss", ["Camp Karka Waypoint"]),
    ("keg brawl", ["Hero's Compass Waypoint"]),
    ("sanctum sprint", ["Sky Docks Waypoint"]),
    ("southsun survival", ["Bazaar Docks Waypoint"]),
    ("moa racing", ["Farshore Waypoint"]),
    ("aspect arena", ["Sky Docks Waypoint"]),
]

def main():
    queries = sys.argv[1:] or None
    failures = 0
    if queries:
        for q in queries:
            res = search(q)
            print(f"\n'{q}' -> {len(res)} result(s)")
            for rank, tag, disp, e in res[:10]:
                print(f"  rank{rank} {disp} | {e['map_name']} | {e['chat_link']}" + (f" -- tag: {tag}" if tag else ""))
        return 0
    for q, expected in CASES:
        res = search(q)
        got = [disp for _, _, disp, _ in res]
        if expected is None:
            print(f"OK   '{q}': {len(res)} results, first: {got[:3]}")
            continue
        if got[:len(expected)] == expected or (len(expected) > 1 and sorted(got[:len(expected)]) == sorted(expected)):
            print(f"OK   '{q}': {got}")
        else:
            print(f"FAIL '{q}': expected first {expected}, got {got[:6]}")
            failures += 1
    for q, expected_count in COUNT_CASES:
        res = search(q)
        if len(res) == expected_count:
            print(f"OK   '{q}' (count): {len(res)} results")
        else:
            print(f"FAIL '{q}' (count): expected {expected_count}, got {len(res)}")
            failures += 1
    for q, expected in INCLUSION_CASES:
        res = search(q)
        got = [disp for _, _, disp, _ in res]
        missing = [x for x in expected if x not in got]
        if not missing:
            print(f"OK   '{q}' (inclusion): {expected} present in {len(res)} results")
        else:
            print(f"FAIL '{q}' (inclusion): missing {missing}, got {got[:6]}")
            failures += 1
    # v1.7 — PSNA-day queries at fixed UTC times: exact 6, agent order.
    for q, now, expected in PSNA_DAY_CASES:
        res = search(q, now)
        got = [disp for _, _, disp, _ in res]
        labels = [tag for _, tag, _, _ in res]
        if got == expected and len(res) == 6:
            print(f"OK   '{q}' @ {now:%Y-%m-%d %H:%M} UTC: {got} | {labels[0]}")
        else:
            print(f"FAIL '{q}' @ {now:%Y-%m-%d %H:%M} UTC: expected {expected}, got {got}")
            failures += 1
    # v1.7 — "Copy daily list" string: exact codes, agent order, no
    # duplicates, no missing entries, 71 chars (fits 199-char chat limit).
    for now, expected in DAILY_LIST_CASES:
        s = build_daily_list_string(psna_weekday_index(now))
        codes = s.split(" ")
        if s == expected and len(codes) == 6 and len(set(codes)) == 6 and len(s) == 71:
            print(f"OK   daily list @ {now:%Y-%m-%d %H:%M} UTC ({len(s)} chars): {s}")
        else:
            print(f"FAIL daily list @ {now:%Y-%m-%d %H:%M} UTC: expected {expected}, got {s}")
            failures += 1
    # v1.10.3 — user tags removed: "banana" (a nonsense word that only
    # ever matched via a user tag) must find nothing with baked tags only.
    res = search("banana")
    if len(res) == 0:
        print("OK   'banana' with baked tags only: 0 results")
    else:
        print(f"FAIL 'banana' with baked tags only: expected 0, got {len(res)}")
        failures += 1
    # v1.10.4 — Daily Activity section removed: "daily activity" must
    # find nothing (umbrella tags removed; the four individual activities
    # are still found by their own names, tested above), and "edinna"
    # must find nothing either.
    for q in ("daily activity", "edinna", "edinna linhoft"):
        res = search(q)
        if len(res) == 0:
            print(f"OK   '{q}' (Daily Activity removed in v1.10.4): 0 results")
        else:
            print(f"FAIL '{q}' (Daily Activity removed in v1.10.4): expected 0, got {len(res)}")
            failures += 1
    total = len(CASES) + len(INCLUSION_CASES) + len(COUNT_CASES) + len(PSNA_DAY_CASES) + len(DAILY_LIST_CASES) + 4
    # v1.10.1 — layout regression: while a query is non-empty the PSNA /
    # Map Bonus / Rifts sections must be
    # hidden, so result rows render immediately under the search box
    # instead of below the fold (screenshot: "flax" found 9/9, no row
    # visible). And the "Try one of these" example buttons must be gone.
    # (v1.10.4: three sections now — Daily Activity was removed.)
    src = pathlib.Path(__file__).resolve().parent.parent.joinpath("src", "entry.cpp").read_text()
    layout_checks = [
        ("searching flag", "const bool searching = g_queryLower[0] != '\\0';" in src),
        ("PSNA hidden while searching", "if (!searching)" in src and src.count("if (!searching)") >= 3),
        ("no example buttons", "kExamples" not in src),
        ("no user tags (v1.10.3)", "g_userTags" not in src and "My tags" not in src
            and "TyriaFinder_user_tags" not in src and "Add a tag" not in src
            and "Tag##" not in src),
        ("no hardcoded game keybind", "Scan for Rift (J)" not in src and "use your Scan for Rift keybind" in src),
        ("no Daily Activity UI (v1.10.4)", '"Daily Activity"' not in src
            and '"Edinna' not in src and '"Go to Edinna' not in src
            and '"[&BJsDAAA=]"' not in src and "Havoc's Heir" not in src
            and '"Lionbridge' not in src),
    ]
    for name, ok in layout_checks:
        total += 1
        if ok:
            print(f"OK   layout v1.10.1: {name}")
        else:
            print(f"FAIL layout v1.10.1: {name}")
            failures += 1
    # v1.9 — Map Bonus week and Rift set indices at fixed UTC times,
    # mirroring MapBonusWeekIndex / RiftSetIndex in src/entry.cpp.
    # MB anchor Thu 2025-07-24 20:00 UTC = Week 8; rift anchor
    # Mon 2023-11-06 07:30 UTC = Set 1.
    def mb_week(dt):
        anchor = datetime(2025, 7, 24, 20, 0, tzinfo=timezone.utc)
        weeks = int((dt - anchor).total_seconds() // (7 * 86400))
        return ((8 - 1 + weeks) % 8) + 1
    def rift_set(dt):
        anchor = datetime(2023, 11, 6, 7, 30, tzinfo=timezone.utc)
        weeks = int((dt - anchor).total_seconds() // (7 * 86400))
        return 1 + (weeks % 11)
    week_cases = [
        (datetime(2026, 11, 17, 7, 30, tzinfo=timezone.utc), 4, 5),
        (datetime(2026, 11, 19, 19, 59, tzinfo=timezone.utc), 4, 5),
        (datetime(2026, 11, 19, 20, 0, tzinfo=timezone.utc), 5, 5),
        (datetime(2026, 11, 23, 7, 29, tzinfo=timezone.utc), 5, 5),
        (datetime(2026, 11, 23, 7, 30, tzinfo=timezone.utc), 5, 6),
        (datetime(2025, 7, 24, 20, 0, tzinfo=timezone.utc), 8, 2),
    ]
    for dt, exp_mb, exp_rift in week_cases:
        got_mb, got_rift = mb_week(dt), rift_set(dt)
        if got_mb == exp_mb and got_rift == exp_rift:
            print(f"OK   week indices @ {dt:%Y-%m-%d %H:%M} UTC: MB Week {got_mb}, Rift Set {got_rift}")
        else:
            print(f"FAIL week indices @ {dt:%Y-%m-%d %H:%M} UTC: expected MB {exp_mb} / Rift {exp_rift}, got MB {got_mb} / Rift {got_rift}")
            failures += 1
    total += len(week_cases)
    print(f"\n{total - failures}/{total} cases passed")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
