import pandas as pd
import os


def sanitize_sheet_name(sheet_name):
    # Replace invalid characters with underscores
    invalid_chars = ['\\', '/', '*', '?', ':', '[', ']']
    for char in invalid_chars:
        sheet_name = sheet_name.replace(char, '_')

    # Limit the sheet name to 31 characters
    return sheet_name


def fun(a, b, c):
    try:
        # Paths to your CSV files
        csv_file1 = a
        csv_file2 = b

        # Sanitize and shorten the sheet names from the CSV file names
        sheet_name1 = sanitize_sheet_name(''.join(csv_file1.split('\csv_file\\')[1]))
        sheet_name2 = sanitize_sheet_name(''.join(csv_file2.split('\csv_file\\')[1]))

        # Excel file where you want to create new sheets
        excel_file = c

        # Function to check if a PDF file exists
        def pdf_file_exists(pdf_file):
            return os.path.isfile(pdf_file)

        # Load CSV data into DataFrames
        df1 = pd.read_csv(csv_file1)
        df2 = pd.read_csv(csv_file2)
        df3 = pd.read_excel(excel_file, sheet_name='ProcessedData')

        # Create a new Excel writer object with the engine specified
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Check if the default "Sheet" exists before removing it
            if 'Sheet' in writer.book.sheetnames:
                writer.book.remove(writer.book['Sheet'])

            # Write df1 to the first sheet
            df2.to_excel(writer, sheet_name=sheet_name2, index=False)

            # Add a new column 'Matched' in df1 based on CSV2 data
            df2['Matched'] = df2['PDF File Names'].isin(df1['PDF File'])

            # Write df1 to the first sheet again with the "Matched" column
            df2.to_excel(writer, sheet_name=sheet_name2, index=False)

            # Write df2 to the second sheet
            df1.to_excel(writer, sheet_name=sheet_name1, index=False)
            #write existing data of excell
            df3.to_excel(writer, sheet_name='ProcessedData', index=False)
    except Exception as e:
        print(e)
