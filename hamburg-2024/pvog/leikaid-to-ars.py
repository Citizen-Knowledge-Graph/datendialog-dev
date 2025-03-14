import csv
import os

directory = "data/1"
dict = {}
files = os.listdir(directory)
total = len(files)
count = 0
previous_perc = 0

for filename in files:
    count += 1
    perc = round((count / total) * 100)
    if perc != previous_perc:
        print(f"{perc}%")
        previous_perc = perc

    filepath = os.path.join(directory, filename)
    ars = filename.split(".")[0]
    with open(filepath, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter="|")
        for row in csv_reader:
            idlb = row["ID-LB"]
            leikaid = row["Leikaschlüssel"]
            if dict.get(leikaid) is None:
                dict[leikaid] = { "ars": [], "idlb": [] }
            if idlb not in dict[leikaid]["idlb"]:
                dict[leikaid]["idlb"].append(idlb)
            if ars not in dict[leikaid]["ars"]:
                dict[leikaid]["ars"].append(ars)

keys = list(dict.keys())

with open("data/leikaid-to-ars.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for leikaid in keys:
        writer.writerow([leikaid] + dict[leikaid]["idlb"] + dict[leikaid]["ars"])
