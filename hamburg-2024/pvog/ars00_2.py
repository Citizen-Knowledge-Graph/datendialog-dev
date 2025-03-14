import os
import json

input_dir = "data/ars00/sozialleistungen"

for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        path = os.path.join(input_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name")
        id_lb, extension = os.path.splitext(filename)
        print(id_lb, ":", name)

        detailsNode = data.get("details")
        if len(detailsNode) > 0:
            for node in detailsNode:
                if node.get("title") == "Voraussetzungen":
                    text = node.get("text")
                    #  if text == "" or text.lower() == "nicht angegeben":
                    print("Voraussetzungen:", text)

        print("\n")
