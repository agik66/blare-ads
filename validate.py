#!/usr/bin/env python3
"""Checks ads.json before you push it. Run: python3 validate.py"""
import json, sys, datetime, urllib.parse

SLOTS = {"lib","find","landscape-banner","ipad-column","web-leaderboard","web-inline","web-side","web-find"}
FORMATS = {"narrow","wide","tall"}
PLATFORMS = {"ios","web"}
REQUIRED = ["id","enabled","weight","platforms","slots","kicker","title","line","cta","url","creative"]

def fail(msg): print("✗", msg); sys.exit(1)

d = json.load(open("ads.json"))
if d.get("version") != 1: fail("version must be 1")
datetime.date.fromisoformat(d["updated"])
if not (1 <= d.get("refresh_hours", 0) <= 168): fail("refresh_hours 1..168")
ids = set()
for a in d["ads"]:
    for k in REQUIRED:
        if k not in a: fail(f"{a.get('id','?')}: missing {k}")
    if a["id"] in ids: fail(f"duplicate id {a['id']}")
    ids.add(a["id"])
    if not set(a["platforms"]) <= PLATFORMS: fail(f"{a['id']}: platforms {a['platforms']}")
    if not set(a["slots"]) <= SLOTS: fail(f"{a['id']}: unknown slot in {a['slots']}")
    if a["weight"] < 0: fail(f"{a['id']}: weight")
    for key in ("from","until"):
        if a.get(key): datetime.date.fromisoformat(a[key])
    if urllib.parse.urlparse(a["url"]).scheme != "https": fail(f"{a['id']}: url must be https")
    if set(a["creative"].keys()) != FORMATS: fail(f"{a['id']}: creative needs exactly narrow/wide/tall")
    for f, c in a["creative"].items():
        if c is not None:
            if urllib.parse.urlparse(c.get("image","")).scheme != "https": fail(f"{a['id']}: {f} image must be https")
    for k in ("kicker","title","line","cta"):
        if len(a[k]) > 140: fail(f"{a['id']}: {k} too long")
print(f"✓ ads.json ok — {len(d['ads'])} ads, {sum(1 for a in d['ads'] if a['enabled'])} enabled")
