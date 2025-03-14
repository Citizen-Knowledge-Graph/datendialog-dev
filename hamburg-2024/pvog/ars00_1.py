import os
import json
import shutil

input_dir = "data/ars00/vollstaendige_leistungsbeschreibungen"
output_dir = "data/ars00/sozialleistungen"

for filename in os.listdir(input_dir):
    path = os.path.join(input_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    personalMatters = data.get("personalMatters")
    if len(personalMatters) > 0:
        children = personalMatters[0]["children"]
        for child in children:
            if child.get("code") == "1140000":  # Sozialleistungen
                print(f"{filename} is a Sozialleistung")
                shutil.copy(path, os.path.join(output_dir, filename))
