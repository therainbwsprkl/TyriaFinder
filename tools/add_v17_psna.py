#!/usr/bin/env python3
"""v1.7 tag additions: Pact Supply Network Agents (PSNA) — daily rotation.

Merge into data/tags.json, validating every (name, map) against
data/pois.json AND the expected chat_link (both must match — catches a
wrong-name lookup). Same merge pattern as add_v16_jps.py: if an entry
is already tagged, new phrases are UNIONED onto it.
Run: python3 tools/add_v17_psna.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py

What PSNA is: 6 special karma merchants, unlocked by the Pact Commander
mastery Supply Line Management (tier 3, Heart of Thorns required). Each
sells Pact Scout's Mapping Materials (5,250 karma) + a random recipe
(25,200 karma) + Torn Page, one item per vendor per day. One agent per
region: Verma Giftrender (Ascalon), Lady Derwena (Kryta), The Fox
(Maguuma Jungle), Mehem the Traveled (Maguuma Wastes), Specialist Yana
(Ruins of Orr), Despina Katelyn (Shiverpeaks).

Rotation: FIXED 7-day weekday cycle. Locations change at 08:00 UTC,
NOT at the 00:00 UTC daily reset (before 08:00 UTC the previous day's
locations still apply). Recipes change at 00:00 UTC and are random per
vendor per day — NOT predictable, NOT tagged here.

Sources (all three agree on the weekday mapping):
- GW2 Wiki "Pact Supply Network Agent" page, table 2025-07-27 to
  2025-08-03 (weekday -> agent locations)
- Doncpauli PSNA page, fetched live 2026-11-17 (weekday table used here)
- PowerShell gist using gw2timer as source (same weekday mapping)

DISPUTED CODES — gist vs Doncpauli, resolved against data/pois.json
(the dataset entry must match the expected location name):
- Mehem Sunday: gist [&BIsHAAA=] is "Oasis" (Dry Top landmark), NOT
  Azarr's Arbor. Doncpauli [&BIkHAAA=] is "Azarr's Arbor" — used.
- Fox Thursday: gist [&BE8AAAA=] is "Seraph Protectors" (Brisban
  landmark — the wiki's description of where the Fox stands, south of
  Wendon Waypoint). Doncpauli [&BF0AAAA=] is "Wendon Waypoint" — used.
- Yana Thursday: gist [&BP0DAAA=] is "Armada Harbor" (Straits landmark).
  Doncpauli [&BO4CAAA=] is "Fort Trinity Waypoint" (wiki: Fort Trinity)
  — used.
- Verma Thursday: gist [&BOQBAAA=] is "Old Piken Ruins Waypoint".
  Doncpauli [&BOcBAAA=] is "Village of Scalecatch Waypoint" — used.
All 42 Doncpauli codes exist in data/pois.json with the expected
name/map. 22 of the 42 are waypoints; 20 are landmark POIs (the
published code points at the agent's spot, not a waypoint). POI codes
are tagged AS-IS — no substitution of a nearby waypoint (e.g. NOT
Restoration Refuge Waypoint [&BIgHAAA=] for Restoration Refuge
[&BIcHAAA=], NOT Caer Shadowfain Waypoint [&BCEDAAA=] for Caer
Shadowfain [&BP0CAAA=], NOT Repair Station Waypoint [&BJcHAAA=] for
Repair Station [&BJQHAAA=]). The note on each POI entry says so.
42 agent-day slots, 40 unique entries: Camp Resolve Waypoint repeats
Tue + Sat (Mehem), Fort Trinity Waypoint repeats Thu + Sun (Yana).

Tag phrases per entry: generic PSNA phrases + agent phrases + the
"psna <weekday>" phrase for each day that agent is at that location.
"daily psna" is tagged on every PSNA entry so a "daily" search finds
the PSNA set at all — but searching "daily psna" / "psna today" /
"today psna" is INTERCEPTED at runtime in src/entry.cpp (and mirrored
in tools/test_search.py) and returns ONLY today's 6, computed from the
system UTC time with the 08:00 UTC cutoff. The static tag alone would
return all 40; the runtime table is what makes it daily.
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tags_path = os.path.join(BASE, "data", "tags.json")
pois = json.load(open(os.path.join(BASE, "data", "pois.json")))["entries"]
by_nm = {}
for e in pois:
    by_nm.setdefault((e.get("name"), e["map_name"]), []).append(e)

doc = json.load(open(tags_path))
tags = doc["tags"]
by_link_tags = {t["chat_link"]: t for t in tags}

GENERIC = ["psna", "pact supply", "pact supply network agent",
           "pact supply network", "pact scout mapping materials",
           "mapping materials", "daily psna"]
AGENT_PHRASES = {
    "Verma Giftrender": ["verma giftrender", "verma"],
    "Lady Derwena": ["lady derwena", "derwena"],
    "The Fox": ["the fox", "fox"],
    "Mehem the Traveled": ["mehem the traveled", "mehem"],
    "Specialist Yana": ["specialist yana", "yana"],
    # "Katyn" is a common misspelling of Katelyn in some sources; alias it.
    "Despina Katelyn": ["despina katelyn", "katelyn", "despina katyn", "katyn"],
}
AGENT_REGION = {
    "Verma Giftrender": "Ascalon",
    "Lady Derwena": "Kryta",
    "The Fox": "Maguuma Jungle",
    "Mehem the Traveled": "Maguuma Wastes",
    "Specialist Yana": "Ruins of Orr",
    "Despina Katelyn": "Shiverpeaks",
}

# (agent, weekday, location name, map, chat_link)
ADD = [
 # Monday
 ("Verma Giftrender", "Monday", "Haymal Gore", "Fireheart Rise", "[&BA8CAAA=]"),
 ("Lady Derwena", "Monday", "Marshwatch Haven Waypoint", "Bloodtide Coast", "[&BKYBAAA=]"),
 ("The Fox", "Monday", "Lionguard Waystation Waypoint", "Caledon Forest", "[&BEwDAAA=]"),
 ("Mehem the Traveled", "Monday", "Restoration Refuge", "Dry Top", "[&BIcHAAA=]"),
 ("Specialist Yana", "Monday", "Rally Waypoint", "Straits of Devastation", "[&BNIEAAA=]"),
 ("Despina Katelyn", "Monday", "Ridgerock Camp Waypoint", "Frostgorge Sound", "[&BIMCAAA=]"),
 # Tuesday
 ("Verma Giftrender", "Tuesday", "Temperus Point Waypoint", "Plains of Ashford", "[&BIMBAAA=]"),
 ("Lady Derwena", "Tuesday", "Garenhoff", "Kessex Hills", "[&BBkAAAA=]"),
 ("The Fox", "Tuesday", "Desider Atum Waypoint", "Metrica Province", "[&BEgAAAA=]"),
 ("Mehem the Traveled", "Tuesday", "Camp Resolve Waypoint", "The Silverwastes", "[&BH8HAAA=]"),
 ("Specialist Yana", "Tuesday", "Waste Hollows Waypoint", "Malchor's Leap", "[&BKgCAAA=]"),
 ("Despina Katelyn", "Tuesday", "Travelen's Waypoint", "Dredgehaunt Cliffs", "[&BGQCAAA=]"),
 # Wednesday
 ("Verma Giftrender", "Wednesday", "Ferrusatos Village", "Blazeridge Steppes", "[&BPEBAAA=]"),
 ("Lady Derwena", "Wednesday", "Shieldbluff Waypoint", "Harathi Hinterlands", "[&BKYAAAA=]"),
 ("The Fox", "Wednesday", "Swampwatch Post", "Sparkfly Fen", "[&BMIBAAA=]"),
 ("Mehem the Traveled", "Wednesday", "Town of Prosperity", "Dry Top", "[&BH4HAAA=]"),
 ("Specialist Yana", "Wednesday", "Caer Shadowfain", "Cursed Shore", "[&BP0CAAA=]"),
 ("Despina Katelyn", "Wednesday", "Mennerheim", "Snowden Drifts", "[&BDgDAAA=]"),
 # Thursday
 ("Verma Giftrender", "Thursday", "Village of Scalecatch Waypoint", "Iron Marches", "[&BOcBAAA=]"),
 ("Lady Derwena", "Thursday", "Altar Brook Trading Post", "Queensdale", "[&BIMAAAA=]"),
 ("The Fox", "Thursday", "Wendon Waypoint", "Brisban Wildlands", "[&BF0AAAA=]"),
 ("Mehem the Traveled", "Thursday", "Blue Oasis", "The Silverwastes", "[&BKsHAAA=]"),
 ("Specialist Yana", "Thursday", "Fort Trinity Waypoint", "Straits of Devastation", "[&BO4CAAA=]"),
 ("Despina Katelyn", "Thursday", "Rocklair", "Lornar's Pass", "[&BF0GAAA=]"),
 # Friday
 ("Verma Giftrender", "Friday", "Hawkgates Waypoint", "Fields of Ruin", "[&BNMAAAA=]"),
 ("Lady Derwena", "Friday", "Pearl Islet Waypoint", "Southsun Cove", "[&BNUGAAA=]"),
 ("The Fox", "Friday", "Bard's Waypoint", "Mount Maelstrom", "[&BMwCAAA=]"),
 ("Mehem the Traveled", "Friday", "Repair Station", "Dry Top", "[&BJQHAAA=]"),
 ("Specialist Yana", "Friday", "Shelter Docks", "Malchor's Leap", "[&BJsCAAA=]"),
 ("Despina Katelyn", "Friday", "Dolyak Pass Waypoint", "Wayfarer Foothills", "[&BHsBAAA=]"),
 # Saturday
 ("Verma Giftrender", "Saturday", "Bovarin Estate", "Diessa Plateau", "[&BBABAAA=]"),
 ("Lady Derwena", "Saturday", "Vigil Keep Waypoint", "Gendarran Fields", "[&BJIBAAA=]"),
 ("The Fox", "Saturday", "Gallant's Folly", "Mount Maelstrom", "[&BLkCAAA=]"),
 ("Mehem the Traveled", "Saturday", "Camp Resolve Waypoint", "The Silverwastes", "[&BH8HAAA=]"),
 ("Specialist Yana", "Saturday", "Augur's Torch", "Cursed Shore", "[&BBEDAAA=]"),
 ("Despina Katelyn", "Saturday", "Balddistead", "Timberline Falls", "[&BEICAAA=]"),
 # Sunday
 ("Verma Giftrender", "Sunday", "Snow Ridge Camp Waypoint", "Fireheart Rise", "[&BCECAAA=]"),
 ("Lady Derwena", "Sunday", "Mudflat Camp", "Bloodtide Coast", "[&BC0AAAA=]"),
 ("The Fox", "Sunday", "Mabon Waypoint", "Caledon Forest", "[&BDoBAAA=]"),
 ("Mehem the Traveled", "Sunday", "Azarr's Arbor", "Dry Top", "[&BIkHAAA=]"),
 ("Specialist Yana", "Sunday", "Fort Trinity Waypoint", "Straits of Devastation", "[&BO4CAAA=]"),
 ("Despina Katelyn", "Sunday", "Blue Ice Shining Waypoint", "Frostgorge Sound", "[&BIUCAAA=]"),
]

def add(agent, weekday, name, map_name, link):
    matches = by_nm.get((name, map_name))
    if not matches:
        sys.exit(f"v1.7 PSNA: location not in dataset: {name} / {map_name}")
    if len(matches) > 1:
        sys.exit(f"v1.7 PSNA: ambiguous (name, map): {name} / {map_name} "
                 f"({len(matches)} entries)")
    e = matches[0]
    if e["chat_link"] != link:
        sys.exit(f"v1.7 PSNA: chat_link mismatch for {name} / {map_name}: "
                 f"table says {link}, dataset says {e['chat_link']}")
    region = AGENT_REGION[agent]
    kind = "POI" if e["type"] == "landmark" else "waypoint"
    note = (f"PSNA — {agent} ({region}), {weekday}: {name}, {map_name}. "
            f"Pact Supply Network Agent, fixed 7-day rotation, locations "
            f"change 08:00 UTC.")
    if e["type"] == "landmark":
        note += (" Published code is the POI, not a waypoint — tagged as-is; "
                 "do not substitute the nearby waypoint.")
    t = by_link_tags.get(link)
    if t is None:
        t = {"chat_link": link, "map": e["map_name"],
             "name": e["name"], "tags": [], "note": note}
        tags.append(t)
        by_link_tags[link] = t
    phrases = GENERIC + AGENT_PHRASES[agent] + [f"psna {weekday.lower()}"]
    for p in phrases:
        if p not in t["tags"]:
            t["tags"].append(p)
    if note not in t.get("note", ""):
        t["note"] = (t.get("note", "") + " " + note).strip()

for agent, weekday, name, map_name, link in ADD:
    add(agent, weekday, name, map_name, link)

doc["generated"] = "2026-11-17"
doc["_note"] = doc.get("_note", "") + (
    " v1.7: PSNA (Pact Supply Network Agents) — 42 agent-day slots, 40 "
    "unique entries, 6 already tagged (34 new). Weekday table from "
    "Doncpauli (fetched live 2026-11-17), cross-checked against the GW2 "
    "Wiki PSNA table (2025-07-27 to 2025-08-03) and a gw2timer-sourced "
    "gist; all three agree on the weekday mapping. 4 gist codes rejected "
    "after dataset check (see tools/add_v17_psna.py): Mehem Sunday "
    "[&BIsHAAA=] is Oasis not Azarr's Arbor; Fox Thursday [&BE8AAAA=] "
    "is Seraph Protectors not Wendon Waypoint; Yana Thursday [&BP0DAAA=] "
    "is Armada Harbor not Fort Trinity; Verma Thursday [&BOQBAAA=] is "
    "Old Piken Ruins not Scalecatch. 20 of the 42 codes are landmark "
    "POIs, tagged as-is. Recipes are random per vendor per day and are "
    "NOT tagged.")
json.dump(doc, open(tags_path, "w"), indent=1)
print(f"v1.7 PSNA: {len(tags)} tagged entries, "
      f"{sum(len(t['tags']) for t in tags)} tag phrases")
