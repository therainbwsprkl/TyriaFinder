#!/usr/bin/env python3
"""Build data/pois.json from the official GW2 API (fetched 2026-11-16).
Sources:
  https://api.guildwars2.com/v2/maps?ids=all
  https://api.guildwars2.com/v2/continents/{1,2}/floors/{floor}
Only points_of_interest with type waypoint / landmark / vista are included.
Hero Points are NOT included: see data/COVERAGE.md - the API's
skill_challenges entries have no name and no chat_link (only coord + an
id like "0-224"), so there is nothing searchable to copy.
Chat links are taken verbatim from the API (p['chat_link']), NOT
re-encoded by this script. Verified against known codes, e.g.
Jaka Itzel Waypoint -> [&BOAHAAA=], Caledon Haven -> [&BDwBAAA=].
"""
import json, glob, collections, os, sys
RAW = "/tmp/gw2raw"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "pois.json")
maps = {m["id"]: m for m in json.load(open(os.path.join(RAW, "maps.json")))}
seen = {}
for path in sorted(glob.glob(os.path.join(RAW, "floor_*.json"))):
    d = json.load(open(path))
    for rid, r in d.get("regions", {}).items():
        for mid, m in r.get("maps", {}).items():
            mid = int(mid)
            for pid, p in m.get("points_of_interest", {}).items():
                pid = int(pid)
                if pid in seen:
                    continue
                if p.get("type") not in ("waypoint", "landmark", "vista"):
                    continue
                info = maps.get(mid, {})
                seen[pid] = {
                    "id": pid,
                    "name": p.get("name"),
                    "type": p.get("type"),  # waypoint | landmark (= POI) | vista
                    "map_id": mid,
                    "map_name": (m.get("name") or info.get("name") or "").strip(),
                    "region": (r.get("name") or info.get("region_name") or "").strip(),
                    "continent_id": info.get("continent_id"),
                    "coord": p.get("coord"),  # continent coords [x, y]
                    "chat_link": p.get("chat_link"),
                }
rows = sorted(seen.values(), key=lambda x: (x["map_name"] or "", x["name"] or ""))
with open(OUT, "w") as f:
    json.dump({"generated": "2026-11-16", "source": "api.guildwars2.com v2 continents + maps",
               "count": len(rows), "entries": rows}, f, indent=1)
print(f"wrote {OUT}: {len(rows)} entries")
print(collections.Counter(r["type"] for r in rows))
print("maps covered:", len({r["map_id"] for r in rows}))
