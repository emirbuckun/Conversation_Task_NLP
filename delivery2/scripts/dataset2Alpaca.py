import pandas as pd
import json
import deepl

auth_key = "476d3290-265f-4de6-9b4c-316386e7651b:fx"  # Replace with your key

translator = deepl.Translator(auth_key)

df = pd.read_csv("casual_data_windows.csv", encoding="utf-8", nrows=6000)  # Read first 100 rows
rows = df.to_dict(orient="records")  # Convert dataframe to list of dictionaries
alpaca_rows = []
with open("alpacaFormat.json", "w", encoding="utf-8") as file:
    try:
        for row in rows:
            input_TR = translator.translate_text(row['1'], target_lang="TR").text
            output_TR = translator.translate_text(row['2'], target_lang="TR").text
            new_row = {
                "instruction": "Aşağıdaki ifadeye karşılık ver.",
                "input": input_TR,
                "output": output_TR
            }
            alpaca_rows.append(new_row)
            print(f"{row['0']} == {new_row}")
    except Exception :
        print(Exception)
        
    json.dump(alpaca_rows, file, indent=2, ensure_ascii=False)