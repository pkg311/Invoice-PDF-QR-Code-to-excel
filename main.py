from Pdf_To_Image_To_decode_csv_Step1 import QRdecode
from CSV_Data_to_partioning import definedata
from EncryptionDataProcess import ecryptionprocess
from compare_csv_to_excell import fun
from pdfToCSV import find_and_write_pdf_names
import win32com.client as win32
import os
import pythoncom
import datetime


def send_email_with_attachments(output, encryption, mailaddress):
    try:
        # Create an Outlook application object
        outlook = win32.Dispatch('outlook.application', pythoncom.CoInitialize())

        # Create a new email
        mail = outlook.CreateItem(0)  # 0 represents a mail item

        # Set email properties
        mail.Subject = 'Process Report of uploaded invoice pdf'
        mail.Body = 'PFA'
        mail.BCC = 'mail@email.com'# Replace with the recipient's email addresses


        mail.To = mailaddress  # Replace with the recipient's email addresses

        # Add attachments
        mail.Attachments.Add(output)  # Replace with the actual file path of the 'output' file
        mail.Attachments.Add(encryption)  # Replace with the actual file path of the 'encryption' file

        # Send the email
        mail.Send()

        print("Email with attachments sent successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def ExecuteQROpeartion(input_folder):
    try:
        # step 0: Record pdf
        print(datetime.datetime.now())
        find_and_write_pdf_names(input_folder)

        # Step 1: Decoding

        QRdecode(input_folder)
        input = str(input_folder) + '\csv_file\qr_code_data.csv'

        output_file = str(input_folder) + '\csv_file\output.csv'
        path = str(input_folder) + '\csv_file'

        definedata(input, output_file, path)

        # # step 4: Encrption to decryption process
        input = str(input_folder) + '\csv_file\Encryption.csv'
        ecryptionprocess(input)
        return str(input_folder) + '\csv_file\Encryption.xlsx'



    except Exception as e:
        print(e)


def combine_process(output, pdf, excel):
    fun(output, pdf, excel)


input1 = input("enter pdf file path")
mailaddress = input("Enter mail address for output")
if __name__ == '__main__':
    input = input1
    a = ExecuteQROpeartion(input)
    output = os.path.join(input, "csv_file", 'Encryption.xlsx')
    encryption = os.path.join(input, "csv_file", 'output.csv')
    pdffile = os.path.join(input, "csv_file", 'pdffile.csv')
    combine_process(encryption, pdffile, output)
    send_email_with_attachments(output, encryption, mailaddress)
    print(datetime.datetime.now())
