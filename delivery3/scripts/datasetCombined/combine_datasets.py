"""This script combines multiple json files into a single json file."""

import json

# Create a list of all the JSON files that you want to combine.
json_files = ["Dataset1.json", "Dataset2.json", "Dataset3.json", "Dataset4.json"]

# Create an empty list to store the Python objects.
python_objects = []

# Load each JSON file into a Python object.
for json_file in json_files:
    with open(json_file, "r", encoding = "utf-8") as f:
        python_objects.extend(json.load(f))

# Dump all the Python objects into a single JSON file.
with open("combined.json", "w", encoding = "utf-8") as f:
    json.dump(python_objects, f, indent = 2, ensure_ascii = False)
