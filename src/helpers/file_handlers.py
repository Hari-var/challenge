import os
from pathlib import Path
from typing import Optional
from PIL import Image
import pytesseract
from fastapi import UploadFile #type: ignore
import shutil

# pytesseract.pytesseract.tesseract_cmd = os.environ['tesseract']

from PyPDF2 import PdfReader #type: ignore
from docx import Document #type: ignore
import pdfplumber #type: ignore

from independentsoft.msg import Message #type: ignore
from independentsoft.msg import Attachment #type: ignore

import re
import pdfkit #type: ignore
import io

from helpers.config import vehicle_images_path



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
            from helpers.config import wkhtlm
            # Path to wkhtmltopdf executable (adjust this according to your system)
            wkhtmltopdf_path = wkhtlm
            
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
    

class Load:
    async def save_vehicle_images(
        self,
        front_img: UploadFile,
        back_img: UploadFile,
        left_img: UploadFile,
        right_img: UploadFile,
        folder_name: str,
        typeofvehicle: str
    ):
        """
        Save four vehicle images (front, back, left, right) in a new folder under vehicle_images.
        """

        base_path = vehicle_images_path
        save_folder = os.path.join(base_path, typeofvehicle, folder_name)
        os.makedirs(save_folder, exist_ok=True)

        paths: dict[str, Optional[str]] = {"main_folder": save_folder}

        # Helper to save each image
        async def save_image(upload_file: UploadFile, name: str):
            if upload_file:
                file_path = os.path.join(save_folder, f"{name}.jpg")
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(upload_file.file, f)
                return file_path
            return None

        paths["front"] = await save_image(front_img, "front")
        paths["back"] = await save_image(back_img, "back")
        paths["left"] = await save_image(left_img, "left")
        paths["right"] = await save_image(right_img, "right")

        return paths



    async def _save_files(self, folder_name: str,subfolder:str, prefix: str, *files: UploadFile):
        """
        Generic method to save multiple files under a specified subfolder.
        """
        base_path = r"C:\practice\challenge\data\claims"
        save_folder = Path(base_path, folder_name, subfolder)
        os.makedirs(save_folder, exist_ok=True)

        saved_paths = []

        for idx, file in enumerate(files):
            if file:
                # Extract safe extension
                _, ext = os.path.splitext(file.filename or "")
                ext = ext if ext else ".bin"  # fallback if no extension

                file_path = os.path.join(save_folder, f"{prefix}_{idx + 1}{ext}")
                
                # Async safe: read file and write in chunks
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)

                saved_paths.append(str(file_path))

        return saved_paths

    async def save_claim_images(self, folder_name: str, *images: UploadFile):
        """
        Save multiple claim images in a new folder under claim_images.
        """
        return await self._save_files(folder_name, "claim_images", "claim_image", *images)

    async def save_documents(self, folder_name: str, *documents: UploadFile):
        """
        Save multiple documents in a new folder under documents.
        """
        return await self._save_files(folder_name, "documents", "document", *documents)
    

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
    x = Transform()
    y=x.image_to_text(r"C:\practice\challenge\data\trail\download7.jpg")
    print(y)
    print(type(y))