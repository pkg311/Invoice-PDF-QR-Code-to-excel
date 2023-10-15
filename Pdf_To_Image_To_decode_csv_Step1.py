# import cv2
# import csv
# import os
# from pyzbar.pyzbar import decode
# from pdf2image import convert_from_path
#
#
# def get_qr_code_type(decoded_object):
#     if decoded_object.type == "QRCODE":
#         return "QR Code"
#     elif decoded_object.type == "CODE128":
#         return "Code 128"
#     else:
#         return "Unknown"
#
#
# def convert_pdf_to_images(input_folder, output_folder, poppler_path, csv_file):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
#
#     all_pdf_names = []  # Store all processed PDF file names
#     images_to_delete = []  # Store image file paths to be deleted
#     cv=str(csv_file)
#     cv=cv.split('\qr_code_data.csv')[0]
#     if not os.path.exists(cv):
#         os.makedirs(cv)
#
#     with open(str(csv_file), "w", newline="", encoding="utf-8") as csvfile:
#
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow([
#             "PDF File",
#             "Image Name",
#             "QR Code Type",
#             "QR Code Data",
#             "Filename",
#             "Image Name",
#         ])  # Write header row
#
#         for pdf_file in pdf_files:
#             pdf_path = os.path.join(input_folder, pdf_file)
#             images = convert_from_path(pdf_path, poppler_path=poppler_path)
#
#             for page_num, image in enumerate(images):
#                 pageimage = os.path.join(
#                     output_folder, f"{pdf_file}_page_{page_num + 1}.jpg"
#                 )
#                 image.save(pageimage, "JPEG")
#                 img = cv2.imread(pageimage)
#
#                 try:
#                     decoded_objects = decode(img)
#                     for obj in decoded_objects:
#                         if obj:
#                             image_name = os.path.basename(pageimage)
#                             qr_type = get_qr_code_type(obj)
#                             qr_data = obj.data
#                             filename = os.path.basename(pdf_file)
#                             csv_writer.writerow([
#                                 pdf_file,
#                                 image_name,
#                                 qr_type,
#                                 qr_data.decode("utf-8"),
#                                 filename,
#                                 image_name,
#                             ])
#                             # print(
#                             #     f"PDF File: {pdf_file}, Image Name: {image_name}, QR Code Type: {qr_type}, QR Code Data: {qr_data.decode('utf-8')}"
#                             # )
#                         else:
#                             images_to_delete.append(pageimage)
#                 except Exception as e:
#                     print(f"Error decoding QR code: {e}")
#
#             all_pdf_names.append(pdf_file)
#
#     with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         for pdf_name in all_pdf_names:
#             if pdf_name not in pdf_files:
#                 csv_writer.writerow([pdf_name, "", "", "", "", "No QR Code Found"])
#
#
# def QRdecode(inputfolder, outputfolder):
#     poppler_path = 'poppler-23.07.0/Library/bin'
#     csv_file = os.path.join(inputfolder, "csv_file", "qr_code_data.csv")
#     convert_pdf_to_images(inputfolder, outputfolder, poppler_path, csv_file)
#
#
#
import cv2
import csv
import os
import numpy as np
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path



def get_qr_code_type(decoded_object):
    if decoded_object.type == "QRCODE":
        return "QR Code"
    elif decoded_object.type == "CODE128":
        return "Code 128"
    else:
        return "Unknown"


def convert_pdf_to_qr_codes(input_folder, poppler_path, csv_file):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]

    with open(str(csv_file), "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            "PDF File",
            "Page Number",
            "Total Pages",
            "QR Code Type",
            "QR Code Data",
        ])  # Write header row

        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_folder, pdf_file)
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
            total_pages = len(images)

            for page_num, image in enumerate(images, start=1):
                img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format

                try:
                    decoded_objects = decode(img)
                    for obj in decoded_objects:
                        if obj:
                            qr_type = get_qr_code_type(obj)
                            qr_data = obj.data
                            csv_writer.writerow([
                                pdf_file,
                                page_num,
                                total_pages,
                                qr_type,
                                qr_data.decode("utf-8"),
                            ])
                except Exception as e:
                    print(f"Error decoding QR code: {e}")


def QRdecode(inputfolder):
    poppler_path = 'poppler-23.08.0\Library\bin'
    csv_file = os.path.join(inputfolder, "csv_file")
    if not os.path.exists(csv_file):
        os.makedirs(csv_file)
    csv_file = os.path.join( csv_file,"qr_code_data.csv")
    convert_pdf_to_qr_codes(inputfolder, poppler_path, csv_file)


