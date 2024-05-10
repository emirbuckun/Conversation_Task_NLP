""" 
This script takes a CSV file as input and translates the text into Turkish alpaca
format using DeepL API. The output is a JSON file with the translated and formatted text.
"""

import csv
import json
import deepl

# set DeepL API key
AUTH_KEY = "09813bf8-0fd4-413e-89c2-0c536148672a:fx"
translator = deepl.Translator(AUTH_KEY)

# read CSV file
file = open("emotion-emotion_69k.csv", encoding="utf-8")
csvreader = csv.reader(file)

# skip header
header = []
header = next(csvreader)
print(header)

rows = [] # save new rows
dialogHistory = "" # save dialog history
prevSituation = "" # check situation for same dialogs

# statistics
totalTranslatedChars = 0
instructionCount = 0
dialogCount = 0

# iterate through each row in the CSV file
for row in csvreader:
    # new situation -> new dialog
    if row[2] != prevSituation:
        prevSituation = row[2]
        dialogHistory = ""
        dialogCount += 1

    # remove extra texts bcz of deepl char limit, they will be added later on
    row[3] = row[3].replace("Customer :","").replace("\nAgent :","")

    # check DeepL API char limit
    if totalTranslatedChars + len(row[3]) + len(row[4]) >= 500000: # deepl limit = 500000
        print("Deepl API char limit reached (500000 chars). Skipping rest of the dialogs...")
        break

    # translate user input and agent output
    userInput_TR = translator.translate_text(row[3], target_lang="TR").text
    agentOutput_TR = translator.translate_text(row[4], target_lang="TR").text

    # update total translated char count
    totalTranslatedChars += len(row[3]) + len(row[4])

    # format instruction
    instruction = dialogHistory + "Kullanıcı: " + userInput_TR + "\nYukarıdaki konuşma geçmişine göre sohbeti devam ettir."

    # create new row and append to rows, increment instruction count by one
    new_row = {
        "instruction": instruction,
        "input": "",
        "output": agentOutput_TR
    }
    rows.append(new_row)
    instructionCount += 1

    # update dialog history
    dialogHistory += "Kullanıcı: " + userInput_TR + "\nAjan: " + agentOutput_TR + "\n"

# show statistics
print("Number of Translated Chars: ", totalTranslatedChars)
print("Number of Instructions: ", instructionCount)
print("Number of Dialogs: ", dialogCount)

# write to JSON file
with open("transformed_dataset4.json", "w", encoding="utf-8") as file:
    json.dump(rows, file, indent = 2, ensure_ascii = False)
