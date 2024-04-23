import csv
import json
import deepl

auth_key = ""  # Replace with your key

translator = deepl.Translator(auth_key)

result = translator.translate_text("Hello, world!", target_lang="TR")
print(result.text)
file = open("") # Replace with your file path
print(type(file))

csvreader = csv.reader(file)
header = []
rows = []

header = next(csvreader)
print(header)
with open("alpacaFormat.json", "w", encoding="utf-8") as file:
    for row in csvreader:
        input_TR = translator.translate_text(row[1], target_lang="TR").text
        output_TR = translator.translate_text(row[2], target_lang="TR").text
        new_row = {
            "instruction": "Aşağıdaki ifadeye karşılık ver.",
            "input": input_TR,
            "output": output_TR
        }
        rows.append(new_row)
        print(new_row)
    json.dump(rows, file, indent=2, ensure_ascii=False)
