#!/usr/bin/env python3
"""v1.6 tag additions, part 3: collections — Dive Master (Explorer).
Merge into data/tags.json, validating every (name, map) against
data/pois.json (chat_link looked up, not guessed). Same merge pattern
as add_v16_jps.py / add_v16_adventures.py.

Scope (honest, documented): GW2 has hundreds of collections; only
ONE closed, fixed-location set is tagged in this build — Dive Master,
the Explorer achievement "Find and use 38 diving locations".
Legendary collections, Janthir/SotO collections and Mastery Insights
were evaluated and rejected for this build (mixed-type objectives with
no fixed location, or 100+ scattered objectives) — see README.md.
Dive Master: 36 of 38 locations taggable. The 2 Hidden Garden goggles
(Mount Maelstrom #1/#2, Cantle of Sun / Cantle of Sky) are NOT tagged:
the Hidden Garden has no waypoints inside it and is entered via a
portal after defeating one of four keepers, each starting from a
different waypoint (Criterion, Ashen, Oxbow Isle, Irwin Isle) — tagging
either goggle to any one of those would be a guess. The 3 non-counting
goggles (Southsun Cove, Labyrinthine Cliffs, Edge of the Mists) do not
count toward Dive Master and are not tagged.
Count note: Dulfy's intro says "37 locations" but its numbered list
runs 1–38 and the wiki Diving Goggles page says 38 required — use 38.
Dive Master has no distinct in-game name per location, so the tag
phrases are built from the fixed location descriptor (map + area),
e.g. "dive goggles lion's arch", "diving goggles sanctum harbor".
Do NOT invent per-location item names.
Source: Dulfy Dive Master guide
(https://dulfyreborn.net/achievements/general/explorer/gw2-dive-master-achievement-guide.html),
cross-checked against the wiki Diving Goggles page; #5 via Dulfy's
Not So Secret guide, #37 via GuildJen Buried Archives guide
("Start from Shipwreck Rock Waypoint… head west"), #38 via the wiki
Cathedral of Verdance page.
"Tempest Waypoint" is the dataset's exact name for the Malchor's Leap
waypoint [&BLACAAA=] (researcher wrote "Tempests Waypoint").
Run: python3 tools/add_v16_collections.py
Then: python3 tools/apply_tags.py && python3 tools/generate_pois_header.py
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

def add(name, map_name, phrases, note):
    matches = by_nm.get((name, map_name))
    if not matches:
        sys.exit(f"v1.6 coll: waypoint not in dataset: {name} / {map_name}")
    if len(matches) > 1:
        sys.exit(f"v1.6 coll: ambiguous (name, map): {name} / {map_name}")
    e = matches[0]
    t = by_link_tags.get(e["chat_link"])
    if t is None:
        t = {"chat_link": e["chat_link"], "map": e["map_name"],
             "name": e["name"], "tags": [], "note": note}
        tags.append(t)
        by_link_tags[e["chat_link"]] = t
    for p in phrases:
        if p not in t["tags"]:
            t["tags"].append(p)
    if note and note not in t.get("note", ""):
        t["note"] = (t.get("note", "") + " " + note).strip()

def dive_tags(area, map_name):
    a = area.lower()
    m = map_name.lower()
    return ["dive master", "collection", "diving goggles", "dive goggles",
            f"dive goggles {a}", f"diving goggles {a}",
            f"dive master {m}", f"diving goggles {m}"]

# (waypoint name, map, area descriptor, note)
ADD = [
 ("Diverse Ledges Waypoint", "Lion's Arch", "Sanctum Harbor",
  "Dive Master #1: Lion's Arch — Sanctum Harbor diving goggles (Dulfy Dive Master guide)."),
 ("Cereboth Waypoint", "Kessex Hills", "Wizard's Fief",
  "Dive Master #2: Kessex Hills — Wizard's Fief diving goggles (Dulfy)."),
 ("Brigantine Waypoint", "Gendarran Fields", "Brigantine Isles",
  "Dive Master #3: Gendarran Fields #1 — Brigantine Isles diving goggles (Dulfy)."),
 ("Vigil Keep Waypoint", "Gendarran Fields", "Vigil Keep",
  "Dive Master #4: Gendarran Fields #2 — Vigil Keep diving goggles (Dulfy)."),
 ("Broadhollow Waypoint", "Gendarran Fields", "Broadhollow Bluffs",
  "Dive Master #5: Gendarran Fields #3 — Broadhollow Bluffs diving goggles, at the top of the Not So Secret jumping puzzle (Dulfy Not So Secret guide: just south of Broadhollow Waypoint)."),
 ("Shieldbluff Waypoint", "Harathi Hinterlands", "Shieldbluff Point",
  "Dive Master #6: Harathi Hinterlands #1 — Shieldbluff Point diving goggles (Dulfy)."),
 ("Bridgewatch Camp Waypoint", "Harathi Hinterlands", "Greenflin Plateau",
  "Dive Master #7: Harathi Hinterlands #2 — Greenflin Plateau diving goggles (Dulfy)."),
 ("Remanda Waypoint", "Bloodtide Coast", "Remanda Saltmarsh",
  "Dive Master #8: Bloodtide Coast — Remanda Saltmarsh, Bloody Bill's Base diving goggles (Dulfy)."),
 ("Adorea Waypoint", "Plains of Ashford", "Lake Adorea",
  "Dive Master #9: Plains of Ashford #1 — Lake Adorea diving goggles (Dulfy)."),
 ("Loreclaw Waypoint", "Plains of Ashford", "Loreclaw Expanse",
  "Dive Master #10: Plains of Ashford #2 — Loreclaw Expanse diving goggles (Dulfy)."),
 ("Breachwater Waypoint", "Diessa Plateau", "Breachwater Lake",
  "Dive Master #11: Diessa Plateau #1 — Breachwater Lake diving goggles (Dulfy)."),
 ("Manbane's Waypoint", "Diessa Plateau", "Manbane's Outcrop",
  "Dive Master #12: Diessa Plateau #2 — Manbane's Outcrop diving goggles (Dulfy)."),
 ("Tenaebron Waypoint", "Fields of Ruin", "Tenaebron Lake",
  "Dive Master #13: Fields of Ruin #1 — Tenaebron Lake diving goggles (Dulfy)."),
 ("Summit Waypoint", "Fields of Ruin", "Warrior's Crown",
  "Dive Master #14: Fields of Ruin #2 — Warrior's Crown diving goggles (Dulfy)."),
 ("Old Piken Ruins Waypoint", "Iron Marches", "Champion's Shield",
  "Dive Master #15: Iron Marches #1 — Champion's Shield diving goggles, in the Chaos Crystal Cavern jumping puzzle (Dulfy)."),
 ("Warhound Village Waypoint", "Iron Marches", "Sunken Halls of Clarent",
  "Dive Master #16: Iron Marches #2 — Sunken Halls of Clarent diving goggles (Dulfy)."),
 ("Pig Iron Waypoint", "Fireheart Rise", "Pig Iron Mine",
  "Dive Master #17: Fireheart Rise — Pig Iron Mine diving goggles, at the top of the Pig Iron Quarry jumping puzzle tower (Dulfy)."),
 ("Incubation Waypoint", "Rata Sum", "Idea Incubation Lab",
  "Dive Master #18: Rata Sum — Idea Incubation Lab diving goggles (Dulfy)."),
 ("Upper Commons Waypoint", "The Grove", "Upper Commons",
  "Dive Master #19: The Grove — Upper Commons diving goggles (Dulfy)."),
 ("Titan's Staircase Waypoint", "Caledon Forest", "Dominion of Winds",
  "Dive Master #20: Caledon Forest — Dominion of Winds diving goggles, from the bridge at Titan's Staircase (Dulfy)."),
 ("Hexane Regrade Waypoint", "Metrica Province", "Hexane Regrade",
  "Dive Master #21: Metrica Province #1 — Hexane Regrade waterfall diving goggles (Dulfy)."),
 ("Loch Waypoint", "Metrica Province", "Loch Jezt",
  "Dive Master #22: Metrica Province #2 — Loch Jezt diving goggles (Dulfy)."),
 ("Brilitine Waypoint", "Brisban Wildlands", "Gotala Cascade",
  "Dive Master #23: Brisban Wildlands #1 — Gotala Cascade diving goggles (Dulfy)."),
 ("East End Waypoint", "Brisban Wildlands", "Skrittsburgh East End",
  "Dive Master #24: Brisban Wildlands #2 — Skrittsburgh East End diving goggles (Dulfy)."),
 ("Taigan Waypoint", "Wayfarer Foothills", "Taigan Groves",
  "Dive Master #27: Wayfarer Foothills #1 — Taigan Groves diving goggles (Dulfy)."),
 ("Grawlenfjord Waypoint", "Wayfarer Foothills", "Grawlenfjord",
  "Dive Master #28: Wayfarer Foothills #2 — Grawlenfjord diving goggles (Dulfy)."),
 ("Demon's Maw Waypoint", "Lornar's Pass", "Demon's Maw",
  "Dive Master #29: Lornar's Pass #1 — Demon's Maw diving goggles (Dulfy)."),
 ("False Lake Waypoint", "Lornar's Pass", "False Lake",
  "Dive Master #30: Lornar's Pass #2 — False Lake diving goggles (Dulfy)."),
 ("Gentle River Waypoint", "Timberline Falls", "Gentle River",
  "Dive Master #31: Timberline Falls #1 — Gentle River diving goggles (Dulfy)."),
 ("Coil Waypoint", "Timberline Falls", "Nonmoa Lake",
  "Dive Master #32: Timberline Falls #2 — Nonmoa Lake diving goggles, at the krait tower (Dulfy)."),
 ("Ice Floe Waypoint", "Frostgorge Sound", "Shattered Ice Floe",
  "Dive Master #33: Frostgorge Sound — Shattered Ice Floe diving goggles, at the end of the Shattered Ice Ruins jumping puzzle (Dulfy)."),
 ("Thorn Pass Waypoint", "Straits of Devastation", "Terzetto Bay",
  "Dive Master #34: Straits of Devastation #1 — Terzetto Bay diving goggles, at the Fort Trinity docked airship (Dulfy)."),
 ("Lone Post Waypoint", "Straits of Devastation", "Shark's Teeth Archipelago",
  "Dive Master #35: Straits of Devastation #2 — Shark's Teeth Archipelago diving goggles, at the Vizier's Tower bridge (Dulfy)."),
 ("Tempest Waypoint", "Malchor's Leap", "Cathedral of Zephyrs",
  "Dive Master #36: Malchor's Leap — Cathedral of Zephyrs, Sculptor's End diving goggles (Dulfy; dataset name is 'Tempest Waypoint')."),
 ("Shipwreck Rock Waypoint", "Cursed Shore", "Mausollus Sea",
  "Dive Master #37: Cursed Shore #1 — Mausollus Sea diving goggles, in the Buried Archives jumping puzzle (GuildJen Buried Archives guide: start from Shipwreck Rock Waypoint, head west; Dulfy gives no waypoint here)."),
 ("Verdance Waypoint", "Cursed Shore", "Cathedral of Verdance",
  "Dive Master #38: Cursed Shore #2 — Cathedral of Verdance diving goggles (wiki Cathedral of Verdance page)."),
]

for name, map_name, area, note in ADD:
    add(name, map_name, dive_tags(area, map_name), note)

json.dump(doc, open(tags_path, "w"), indent=1)
print(f"v1.6 coll: {len(tags)} tagged entries, "
      f"{sum(len(t['tags']) for t in tags)} tag phrases")
