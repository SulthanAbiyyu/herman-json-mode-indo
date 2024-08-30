import pandas as pd
import json
import re

def extract_schema(sistem):
    schema_match = re.search(r'<schema>(.*?)</schema>', sistem, re.DOTALL)
    if schema_match:
        schema_str = schema_match.group(1).replace("'", '"')  # Replace single quotes with double quotes for valid JSON
        return json.loads(schema_str)
    return None

def parse_json_output(output):
    return json.loads(output)

def validate_json_against_schema(schema, json_output):
    if 'required' in schema:
        for key in schema['required']:
            assert key in json_output, f"Key '{key}' is missing in the output."
    else:
        for key in schema.get('properties', {}).keys():
            assert key in json_output, f"Key '{key}' is missing in the output."

if __name__ == "__main__":
    df = pd.read_csv('./data/herman-json-mode.csv')

    for index, row in df.iterrows():
        schema = extract_schema(row['sistem'])
        if schema:
            json_output = parse_json_output(row['output'])
            try:
                validate_json_against_schema(schema, json_output)
                print(f"Row {index}: Validation successful.")
            except AssertionError as e:
                print(f"Row {index}: Validation failed - {e}")
        else:
            print(f"Row {index}: No valid schema found in 'sistem' column.")