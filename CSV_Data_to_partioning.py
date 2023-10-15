import pandas as pd
import re


# Function to apply string containment check and return the remark
def apply_string_check(qr_code_data):
    # Check if the string ".ey" is present in the data
    if ".ey" in qr_code_data:
        return "Encryption"
    elif ',' in qr_code_data and ':' in qr_code_data and 'PO' in qr_code_data:
        return "Po Data"
    elif ',' in qr_code_data and ':' in qr_code_data and 'SellerGstin' in qr_code_data:
        return "Decrypted invoice data"
    else:
        return "Normal"


# Function to process the CSV file
def process_csv(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Apply the string containment check to the "QR Code Data" column and store the result in the "remark" column
    df["remark"] = df["QR Code Data"].apply(apply_string_check)

    # Save the entire DataFrame with the added "remark" column to a new CSV file
    df.to_csv(output_file, index=False)




def fetchencription(csv,path):
    # Read the "output.csv" file
    output_file = csv
    df = pd.read_csv(output_file)
    # Filter rows where the "remark" column is "Encryption"
    encryption_df = df[df["remark"] == "Encryption"]
    # Save the filtered DataFrame as "Encryption.csv"
    encryption_output_file = path +'/'+ "Encryption.csv"
    encryption_df.to_csv(encryption_output_file, index=False)



def definedata(input,output_file,path):
    input_file = input
    process_csv(input_file, output_file)
    fetchencription(output_file,path)
