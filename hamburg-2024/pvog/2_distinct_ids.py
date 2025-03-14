import csv
import os

directory = "data/1"
# directory = "data/ars00"

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
    with open(filepath, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter="|")
        for row in csv_reader:
            id = row["ID-LB"]
            if ".LB." in id:
                dict[id] = True

result_list = list(dict.keys())

# data/ars00/distinct_id-lbs.csv
with open("data/2/distinct_id-lbs.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for id in result_list:
        writer.writerow([id])
