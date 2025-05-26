from pypdf import PdfReader
import PyPDF2


def load_content(file_path):
    # check if pdf then below code will be executed else add read txt file
    if file_path.endswith(".pdf"):
        pdf = PdfReader(file_path)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as file:
            return file.read()
    else:
        print("Unsupported file format")
        return ""


def load_content_streamlit(upload_file):
    if upload_file is not None:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(upload_file)
        # Extract the content
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()
        return content
