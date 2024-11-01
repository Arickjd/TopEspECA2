# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:14:04 2024

@author: Professor

Generated with Perplexity.AI
"""

import pandas as pd
import re

def convert_text_to_spreadsheet(input_file, output_file): 
    # Read the content of the text file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regex to find all sections in the specified format
    sections = re.findall(r'(\d+\))\s*(.*?)\n(.*?)(?=\n\d+\)|$)', content, re.DOTALL)

    # Prepare data for DataFrame
    data = []
    for section in sections: 
        title = section[1].strip()  # Title of the section
        body = section[2].strip()    # Body of the section
        data.append({'Title': title, 'Body': body, 'Rating':''})

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data)

    # Export DataFrame to an Excel file
    df.to_excel(output_file, index=False)

# Usage example
input_file = 'input.txt'  # Replace with your input text file path
output_file = 'Dilemmas_Results.xlsx'  # Desired output Excel file path

convert_text_to_spreadsheet(input_file, output_file)
print(f"Data successfully written to {output_file}")
