import json, re
c = json.load(open("candidates.json", encoding="utf-8"))
drop = re.compile(r"Riyadh Skyline|Summer Untold|USACE|Ismail Awan|قصر الامارة|Heritage village|قرية|Apple at|Fig at|Pomegranate|Prickly|South Abhur|AlSaif", re.I)
keep, khasha = [], 0
for p in c:
    t = p["title"]
    if drop.search(t):
        continue
    if "Khasha'a" in t:
        khasha += 1
        if khasha % 5:  # keep every 5th of the 32-shot series
            continue
    keep.append({"url": p["url"], "credit": p["credit"], "title": t[5:].rsplit(".", 1)[0]})
json.dump(keep, open("photos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(keep))
for k in keep: print(" -", k["title"])
