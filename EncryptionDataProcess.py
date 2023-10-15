import pandas as pd
import base64
import re
import json


# Function to perform Base64 decryption and append the result to the existing file

def fix_base64_padding(base64_string):
    missing_padding = len(base64_string) % 4
    if missing_padding != 0:
        base64_string += '=' * (4 - missing_padding)
    return base64_string


def base64_to_text(base64_string):
    try:
        # Fix the padding first (if needed)
        base64_string = fix_base64_padding(base64_string)
        decoded_bytes = base64.b64decode(base64_string)
        decoded_text = decoded_bytes.decode('latin-1')
        return decoded_text
    except Exception as e:
        print("Error decoding Base64 string:", e)
        return None


def process_base64_decryption(input_file):
    """
    Process Base64 decryption on the "QR Code Data" column and append the decrypted data to the existing CSV file.

    :param input_file: The path to the input CSV file.
    """
    try:
        # Read the CSV file

        df = pd.read_csv(input_file)

        # Function to perform Base64 decryption
        def base64_decrypt(encoded_data):

            a = '":"'
            try:
                val = encoded_data.split('.')[1]
                val = base64_to_text(val).split(a)[1]
                val = val.split('","')[0]
                return val
            except Exception as e:

                return str(e)  # Return the error message if decryption fails

        # Apply Base64 decryption to the "QR Code Data" column and append the result to a new "raw data" column
        df["raw data"] = df["QR Code Data"].apply(base64_decrypt)

        # Save the DataFrame with the added "raw data" column back to the same CSV file
        df.to_csv(input_file, index=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def process_and_store_data(input_file):
    try:
        output_file = (str(input_file).split('.csv')[0] + '.xlsx')
        # Read the CSV file
        df = pd.read_csv(input_file)

        # Function to convert JSON strings in "raw data" column to dictionaries
        def json_to_dict(json_string):
            try:
                json_string = json_string.replace('\\', '')
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON string: {str(e)}")
                return None

        # Apply JSON string to dictionary conversion to the "raw data" column
        df['raw data'] = df['raw data'].apply(json_to_dict)

        # Expand the dictionary into separate columns
        df = pd.concat([df.drop(['raw data'], axis=1), pd.json_normalize(df['raw data'])], axis=1)

        # Create a new Excel file with the processed data
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='ProcessedData', index=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage:
def ecryptionprocess(input_file):
    process_base64_decryption(input_file)
    process_and_store_data(input_file)
