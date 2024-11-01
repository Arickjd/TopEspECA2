# -*- coding: utf-8 -*-
"""
Editor Spyder

Este é um arquivo de script temporário.

Partes do código gerados pelo perplexity.ai
"""

import pandas as pd
from PIL import Image
import re
import os
import json

import ollama


curr_path = os.getcwd()
system_prompt_filename = "system_prompt_1.txt"
user_prompt_filename = "user_prompt_double_pass_1.txt"
system_parsing_prompt_filename = "system_parsing_prompt_2.txt"
parsing_prompt_filename = "parsing_prompt_2.txt"

system_prompt_filepath = curr_path + "\\" + system_prompt_filename
user_prompt_filepath = curr_path + "\\" + user_prompt_filename

# Open the file with UTF-8 encoding
with open(system_prompt_filepath, 'r', encoding='utf-8') as file:
    # Read the content of the file
    system_prompt = file.read()
with open(user_prompt_filepath, 'r', encoding='utf-8') as file:
    # Read the content of the file
    user_prompt = file.read()


def extract_rating(json_string):
    print(f'JSON string to data:{json_string}')
    data = json.loads(json_string)
    return list(data.values())[0]

def update_spreadsheet_with_data(file_path):
    # Read the Excel file
    print(f'*** Reading XLSX file {file_path}')
    df = pd.read_excel(file_path)

    # Check if the DataFrame is empty
    if df.empty:
        print("The Excel file is empty.")
        return

    # Display the headers
    print("Headers:", df.columns.tolist())

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
            
            
        text_filename = folder_path+'Dilemma'+str(index)
        rating = row['Rating']
        print(f'>>>> Dilemma {index}: current rating is {rating}')
        if not isinstance(rating,(int, float)) or pd.isna(rating):
            body = row['Body'] # text of the dilemma
            
        else:
            body = None
        if body is not None:
            logfile_path = text_filename + '.LOG.txt'
            logfile = open(logfile_path,'w')
            print(f"The byte array of the text body is {len(body)} bytes long.")
            rating_messages = [
                {'role':'system',
                'content': system_prompt,
                }
                ,
                {'role': 'user',
                'content': user_prompt + body,
                },
            ]
            opts = {
               'temperature': 0.0
            }
            
            response = ollama.chat(model='phi3', messages = rating_messages, options = opts)
            
            logfile.write('Rating pass:\n' + repr(response) + '\n\n')
            
            content = response['message']['content']
            print(content)
           
            
            system_parsing_prompt_filepath = curr_path + "\\" + system_parsing_prompt_filename
            parsing_prompt_filepath = curr_path + "\\" + parsing_prompt_filename
            with open(system_parsing_prompt_filepath, 'r', encoding='utf-8') as file:
                # Read the content of the file
                system_parsing_prompt = file.read()
            with open(parsing_prompt_filepath, 'r', encoding='utf-8') as file:
                    # Read the content of the file
                    parsing_prompt = file.read()
            parsing_prompt += content
            print(f'-----------------------\n\n Parsing prompt: \n\n {parsing_prompt}')
            parsing_messages = [
              {'role': 'system',
               'content': system_parsing_prompt,
               }
              ,
              {
                'role': 'user',
                'content': parsing_prompt,
              },
            ]
            
            response = ollama.chat('phi3', messages = parsing_messages, options = opts)
            
            repr_response = repr(response)
            
            logfile.write('Parsing pass:\n' + repr(repr_response.encode(encoding='utf-8')) + '\n\n')
            
            parsed = response['message']['content']
            print(parsed)
            j_begin=parsed.find('{')
            j_end=parsed.find('}')+1
            
            json_string = parsed[j_begin:j_end]
                      
            #print(f'JSON string: {json_string}')
            rating_estimate = extract_rating(json_string)

            print(f"Row {index + 1}: the estimated rating for dilemma {index} is {rating_estimate}. ")

            print("Excel file updated successfully.")
            
            df.at[index, df.columns[2]] =rating_estimate
            # Update the file at each iteration
            df.to_excel(file_path, index=False)

## MAIN

folder_path = os.getcwd() + '\\dilemmas\\'
spreadsheet_file = folder_path + 'Dilemmas_Results.xlsx'

## This file should be created only once
## This should run once. Afterwards, it will only be open, and rows already filled with results will not 
## run again.

if not(os.path.isfile(spreadsheet_file)):
    create_spreadsheet_from_images(folder_path, spreadsheet_file)
    
# Now read the spreadsheet and iterate along the rows
# If the corresponding Rating is empty, ask LLava for it.


update_spreadsheet_with_data(spreadsheet_file)