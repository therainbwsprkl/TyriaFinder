#!/usr/bin/env python3
"""Merge data/tags.json into data/pois.json.

Each tag entry is keyed by chat_link and is validated against the
dataset: the chat_link must exist, and the recorded name/map must match
the dataset entry exactly. Fails loudly on any mismatch instead of
silently tagging the wrong waypoint. Run before
tools/generate_pois_header.py.
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pois_path = os.path.join(BASE, "data", "pois.json")
tags_path = os.path.join(BASE, "data", "tags.json")
data = json.load(open(pois_path))
tags = json.load(open(tags_path))["tags"]
by_link = {e["chat_link"]: e for e in data["entries"]}
for e in data["entries"]:
    e.pop("tags", None)
seen = set()
for t in tags:
    link = t["chat_link"]
    if link in seen:
        sys.exit(f"duplicate tag entry for {link}")
    seen.add(link)
    e = by_link.get(link)
    if e is None:
        sys.exit(f"tag chat_link not in dataset: {link} ({t['name']})")
    if e.get("name") != t["name"] or e["map_name"] != t["map"]:
        sys.exit(f"tag name/map mismatch for {link}: tags.json says "
                 f"{t['name']} / {t['map']}, dataset says "
                 f"{e.get('name')} / {e['map_name']}")
    if not t["tags"]:
        sys.exit(f"empty tag list for {link}")
    e["tags"] = t["tags"]
json.dump(data, open(pois_path, "w"), indent=1)
print(f"tagged {len(tags)} entries in data/pois.json "
      f"({sum(len(t['tags']) for t in tags)} tag phrases)")
