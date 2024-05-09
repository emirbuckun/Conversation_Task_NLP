import csv
import json

RAW_DATASET_FILE = "delivery3\\scripts\\dataset3\\topical_chat.csv"
MAX_CHAR_NUMBER = 500_000  # max number of characters allowed to be translated with no cost by DeepL's API

# returns the number of characters in a json object's string array 'messages'
def number_of_characters(json_object):
    return sum(len(message) for message in json_object["messages"])

with open(RAW_DATASET_FILE, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    csv_rows = list(csv_reader)
    
    current_file_no = 1
    current_char_number = 0
    json_array = []
    json_object = {
        "conversation_id": None,
        "messages": []
    }
    
    for row in csv_rows:
        if json_object["conversation_id"] is None:
            json_object["conversation_id"] = row["conversation_id"]
        
        # when skip to a new conversation with different id
        if row["conversation_id"] != json_object["conversation_id"]:
            # if new conversation exceeds the max character limit
            if current_char_number + number_of_characters(json_object) > MAX_CHAR_NUMBER:
                json_file_name = 'dataset_english_' + str(current_file_no) + '.json'
                # each time create json files that contains max 500'000 characters
                with open(json_file_name, 'w', encoding='utf-8') as json_file:
                    json.dump(json_array, json_file, indent=4)
                # reset json array
                json_array = []
                # update commonly used variables
                current_file_no += 1
                current_char_number = 0
            
            json_array.append(json_object)
            current_char_number += number_of_characters(json_object)
            json_object = {
                "conversation_id": row["conversation_id"],
                "messages": [row["message"]]
            }
        # when the character limit is not reached
        else:
            json_object["messages"].append(row["message"])
    
    # Save the last conversation
    if current_char_number + number_of_characters(json_object) > MAX_CHAR_NUMBER:
        json_file_name = 'dataset_english_' + str(current_file_no) + '.json'
        with open(json_file_name, 'w', encoding='utf-8') as json_file:
            json.dump(json_array, json_file, indent=4)
        json_array = []
        current_file_no += 1
        current_char_number = 0
        
    json_array.append(json_object)
    json_file_name = 'dataset_english_' + str(current_file_no) + '.json'
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(json_array, json_file, indent=4)
