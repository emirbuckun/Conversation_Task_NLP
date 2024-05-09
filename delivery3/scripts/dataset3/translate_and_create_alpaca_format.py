import json
import deepl
import sys

ENGLISH_DATASET_FILE = "dataset_english_1.json"
API_KEY = "fa656053-fbc5-4a71-b698-58061190924f:fx"
MAX_TOKEN_COUNT = 512
INSTRUCTION_TEXT = "Yukarıdaki konuşma geçmişine göre sohbeti devam ettir. "

translator = deepl.Translator(API_KEY)

def translate_json_object_messages(json_object):
    translated_messages = []
    for message in json_object['messages']:
        translated_message = translator.translate_text(message, target_lang="TR").text
        print('translated message: ', translated_message.encode('utf-8').decode(sys.stdout.encoding))
        translated_messages.append(translated_message)
    return translated_messages

def token_count(string):
    words = string.split()
    return len(words)

def is_instruction_empty(alpaca_object):
    return len(alpaca_object['instruction']) == 0

def create_new_instruction(previous_instruction, previous_output, new_message):
    new_instruction = ""
    if len(previous_instruction) != 0:
        new_instruction = previous_instruction + "\n"
        new_instruction += "Ajan: " + previous_output + "\n"
    new_instruction += "Kullanıcı: " + new_message
    return new_instruction


with open(ENGLISH_DATASET_FILE, 'r', encoding='utf-8') as json_file:
    json_array = json.load(json_file)
    alpaca_array = []
    
    for json_object in json_array:
        translated_messages = translate_json_object_messages(json_object)
        previous_instruction = "" # will be used to set a conversation history
        previous_output = "" # will be used to set a conversation history
        alpaca_object = {
            'instruction': "",
            'input': "",
            'output': ""
        }
        
        for message in translated_messages:
            # if no instruction, create one
            if is_instruction_empty(alpaca_object):
                alpaca_object['instruction'] = create_new_instruction(previous_instruction, previous_output, message)
                previous_instruction = alpaca_object['instruction']
                alpaca_object['instruction'] += "\n" + INSTRUCTION_TEXT
                continue
            
            # skip the instruction when exceeding token size limit
            if token_count(alpaca_object['instruction']) > MAX_TOKEN_COUNT:
                continue
            
            alpaca_object["output"] = message
            previous_output = message
            alpaca_array.append({'instruction': alpaca_object["instruction"], 'input': "", 'output': alpaca_object["output"]})
            
            # reset the variables
            alpaca_object["instruction"] = ""
            alpaca_object["output"] = ""
        
    alpaca_file_name = 'dataset3.json'
    with open(alpaca_file_name, 'w', encoding='utf-8') as alpaca_file:
        json.dump(alpaca_array, alpaca_file, indent=4, ensure_ascii=False)
