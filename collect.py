"""Build photos.json: 4K landscape JPEGs from Saudi-only Wikimedia Commons categories."""
import json, time, urllib.parse, urllib.request

CATS = ["Landscapes_of_Saudi_Arabia", "Deserts_of_Saudi_Arabia", "Mountains_of_Saudi_Arabia",
        "Quality_images_of_Saudi_Arabia", "Featured_pictures_of_Saudi_Arabia", "Asir_Province",
        "Nature_of_Saudi_Arabia", "Beaches_of_Saudi_Arabia", "Valleys_of_Saudi_Arabia",
        "Sand_dunes_in_Saudi_Arabia", "Oases_in_Saudi_Arabia", "Sunsets_in_Saudi_Arabia",
        "Rock_formations_in_Saudi_Arabia"]
UA = {"User-Agent": "family-tv-home/1.0 (personal TV dashboard)"}


def get(url):
    for wait in (2, 8, 20, 45):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(wait)
    raise RuntimeError("rate limited")


out = {}
for cat in CATS:
    url = ("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=categorymembers"
           f"&gcmtitle=Category:{cat}&gcmtype=file&gcmlimit=200&prop=imageinfo&iiprop=size|url|user|mime")
    try:
        pages = get(url).get("query", {}).get("pages", {})
    except Exception as e:
        print(cat, "ERR", e, flush=True)
        continue
    n = 0
    for p in pages.values():
        i = (p.get("imageinfo") or [{}])[0]
        w, h = i.get("width", 0), i.get("height", 1)
        if w >= 3840 and 1.3 <= w / h <= 2.1 and i.get("mime") == "image/jpeg":
            orig = i["url"]  # .../commons/a/ab/Name.jpg -> .../commons/thumb/a/ab/Name.jpg/3840px-Name.jpg
            head, name = orig.rsplit("/", 1)
            thumb = head.replace("/commons/", "/commons/thumb/") + f"/{name}/3840px-{name}"
            out[p["title"]] = {"title": p["title"], "url": thumb, "credit": i.get("user", ""), "cat": cat}
            n += 1
    print(cat, "files", len(pages), "4k", n, flush=True)
    time.sleep(3)

json.dump(sorted(out.values(), key=lambda x: (x["cat"], x["title"])), open("candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for v in sorted(out.values(), key=lambda x: (x["cat"], x["title"])):
    print(v["cat"], "::", v["title"])
print("total", len(out))
