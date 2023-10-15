import os
from PyPDF2 import PdfReader
import csv


def get_pdf_page_count(pdf_path):
    try:
        pdf_reader = PdfReader(pdf_path)
        return len(pdf_reader.pages)
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_pdfs_in_folder(folder_path, output_csv):
    # Initialize an empty list to store results
    pdf_info_list = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            page_count = get_pdf_page_count(file_path)
            pdf_info_list.append([filename, page_count])

    # Write the PDF names and page counts to the output CSV file
    with open(output_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(['PDF File Names', 'Page Count'])
        # Write the data
        csv_writer.writerows(pdf_info_list)

    print("PDF names and page counts have been written to", output_csv)


# Function to find PDF files and write them to a CSV
def find_and_write_pdf_names(folder_path):
    csv_folder = os.path.join(folder_path, "csv_file")
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    output_csv = os.path.join(csv_folder, "pdffile.csv")
    analyze_pdfs_in_folder(folder_path, output_csv)


