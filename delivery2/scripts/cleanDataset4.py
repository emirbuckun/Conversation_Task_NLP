"""This script cleans the csv data and converts it into a JSON file."""

import csv
import json

file = open("emotion-emotion_69k.csv", encoding="utf-8")

csvreader = csv.reader(file)
header = []
rows = []

header = next(csvreader)
with open("data.json", "w", encoding="utf-8") as file:
    for row in csvreader:
        new_row = {
            "id": row[0],
            header[1]: row[1],
            header[2]: row[2],
            header[3]: row[3],
            header[4]: row[4],
        }
        rows.append(new_row)
        if row[0] == "3000":
            break
    json.dump(rows, file, indent=2, ensure_ascii=False)
