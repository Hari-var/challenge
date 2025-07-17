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
import pdfkit
import io

from .config import vehicle_images_path

# `print(os.environ['tesseract'])`
class Extract():

    def extract_code(self,response, file_type="json"):
        response = response.strip().replace(f"```{file_type}","").strip().replace("```","").strip()
        return response
    

class Transform():
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
    
    

    def html_to_pdf(self,html_content: str, output_filename="output.pdf"):
        """
        Convert raw HTML content to a PDF and return a BytesIO buffer for download or further use.

        Args:
            html_content (str): HTML content to be converted to PDF.
            output_filename (str): Optional name for the PDF output (default: 'output.pdf').

        Returns:
            BytesIO: PDF file as a stream, or error message string if conversion fails.
        """
        try:
            # Path to wkhtmltopdf executable (adjust this according to your system)
            wkhtmltopdf_path = r"C:\practice\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe"
            
            # Set pdfkit config
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            
            # Optional: Wrap with <html> if the passed HTML is partial
            if "<html" not in html_content:
                html_content = f"<html><body>{html_content}</body></html>"

            # PDF options
            options = {
                "encoding": "UTF-8",
                "page-size": "A4",
                "margin-top": "20mm",
                "margin-bottom": "20mm",
                "margin-left": "15mm",
                "margin-right": "15mm"
            }

            # Convert to PDF and store in memory
            pdf_bytes = pdfkit.from_string(html_content, output_path=False, configuration=config, options=options)
            
            pdf_buffer = io.BytesIO()
            pdf_buffer.write(bytes(pdf_bytes))
            pdf_buffer.seek(0)

            return pdf_buffer

        except Exception as e:
            return f"Error converting HTML to PDF: {str(e)}"
        
    def file_to_text(self,file_path: str):
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
            attachment= Transform()
            return attachment.pdf_to_text(file_path)
        
        elif ext == ".docx":
            attachment= Transform()
            return attachment.docx_to_text(file_path)
        
        elif ext in [".tif", ".tiff", ".png", ".jpg", ".jpeg", ".bmp"]:
            attachment= Transform()
            return attachment.image_to_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    

class Load():
    def save_vehicle_images(self,front_img, back_img, left_img, right_img, folder_name,typeofvehicle):
        """
        Save four vehicle images (front, back, left, right) in a new folder under vehicle_images.

        Args:
            front_img, back_img, left_img, right_img: Uploaded file objects (e.g., from Streamlit file_uploader).
            folder_name (str): Name of the folder to create for saving images.

        Returns:
            dict: Paths to the saved images.
        """
        base_path = vehicle_images_path
        save_folder = os.path.join(base_path,typeofvehicle, folder_name)
        os.makedirs(save_folder, exist_ok=True)

        paths = {}
        paths["main_folder"] = save_folder
        if front_img:
            front_path = os.path.join(save_folder, "front.jpg")
            with open(front_path, "wb") as f:
                f.write(front_img.getbuffer())
            paths["front"] = front_path
        if back_img:
            back_path = os.path.join(save_folder, "back.jpg")
            with open(back_path, "wb") as f:
                f.write(back_img.getbuffer())
            paths["back"] = back_path
        if left_img:
            left_path = os.path.join(save_folder, "left.jpg")
            with open(left_path, "wb") as f:
                f.write(left_img.getbuffer())
            paths["left"] = left_path
        if right_img:
            right_path = os.path.join(save_folder, "right.jpg")
            with open(right_path, "wb") as f:
                f.write(right_img.getbuffer())
            paths["right"] = right_path

        return paths
    

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
        else:
            raise ValueError("Invalid file path: Unable to extract .msg file name")

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


# Example usage:
if __name__ == "__main__":
    pass