import os
from PIL import Image
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = os.environ['tesseract']

from PyPDF2 import PdfReader
from docx import Document
import pdfplumber

from independentsoft.msg import Message
from independentsoft.msg import Attachment

import re

# `print(os.environ['tesseract'])`

class attachment_handler():
    def image_to_text(self,image_path):
        """
        Convert an image to text using OCR.
        
        :param image_path: Path to the image file.
        :return: Extracted text from the image.
        """

        with Image.open(image_path) as img:
            # Use pytesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
            return text

    def pdf_to_text(self,pdf_path):
        """code to read the pdf data from the given file"""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

    def docx_to_text(self,docx_path):
        """code to read the dox data from the given file"""
        doc = Document(docx_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text)

    

class email_handler():
    def extract_msg_details(self,msg_path):
        message = Message(msg_path)
        
        msg_details = {
            "subject": str(message.subject),
            "client_submit_time": str(message.client_submit_time),
            "sender": {
                "name": str(message.sender_name),
                "email": str(message.sender_email_address)
            },
            "recipient": {
                "name": str(message.received_by_name), 
                "email": str(message.received_by_email_address),
                "display_to": str(message.display_to)
            },
            "content": {
                "body": str(message.body),
                "html": str(message.body_html_text)
            }
        }
        return msg_details  
        
    def extract_msg_attachments(self,file_path):
        # Regex to extract the .msg file name
        match = re.search(r'([^\\]+\.msg)$', file_path)

        # Sanitize the file name to remove invalid characters for folder creation
        if match:
            file_name = re.sub(r'[<>:"/\\|?*]', '_', match.group(1).rstrip('.msg')).strip()
            print(file_name)  # Output: Sanitized file name

        # Create the folder path dynamically
        output_folder = os.path.join("C:\\practice\\personal\\attachments", file_name)
        os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

        message = Message(file_path=file_path)
        attachments_list = []
    
        # Save attachments in the relevant folder
        for i in range(len(message.attachments)):
            attachment = message.attachments[i]
            attachment_file_path = os.path.join(output_folder, str(attachment.file_name).strip())
            attachment.save(attachment_file_path)
            attachments_list.append(attachment_file_path)
        return attachments_list


def file_to_text(file_path):
    """
    Directs the file to the appropriate handler based on its type (.msg, .pdf, .docx, image).
    :param file_path: Path to the file.
    :return: Extracted text from the file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".msg":
        # Extract body text from .msg file
        
        email = email_handler()
        details = email.extract_msg_details(file_path)
        attachments = email.extract_msg_attachments(file_path)
        return [details,attachments]
    
    elif ext == ".pdf":
        attachment= attachment_handler()
        return attachment.pdf_to_text(file_path)
    
    elif ext == ".docx":
        attachment= attachment_handler()
        return attachment.docx_to_text(file_path)
    
    elif ext in [".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp"]:
        attachment= attachment_handler()
        return attachment.image_to_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# Example usage:
if __name__ == "__main__":
    a = attachment_handler()
    print(a.pdf_to_text(r"C:\IDP\test_data\doc_templates\Medical Records\Updated_Medical001.pdf"))
