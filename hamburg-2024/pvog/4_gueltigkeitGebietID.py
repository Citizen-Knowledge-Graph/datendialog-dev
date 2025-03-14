import os
import json

directory = "data/3"
dict = {}

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    gebietID = data.get("gueltigkeitGebietID")
    if "schemeID" in gebietID[0]:
        schemeID = gebietID[0]["schemeID"]
        if schemeID not in dict:
            dict[schemeID] = 1
        else:
            dict[schemeID] += 1

print(dict)
