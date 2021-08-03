import ast
import json
import os


def json_reformat(input_file, indent=4, sort_keys=True):
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf8') as file:
            for line in file:
                data = line
        data = ast.literal_eval(data)
        json_data = json.dumps(data, indent=indent, sort_keys=sort_keys)
        with open('reformat_file.json', 'w', encoding='utf8') as file:
            file.write(json_data)
    else:
        print('File not found')


file_json = '../temp/1.json'
json_reformat(file_json, indent=4, sort_keys=False)
