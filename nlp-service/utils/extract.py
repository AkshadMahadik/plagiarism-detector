import io
import re
import PyPDF2
import docx

def extract_text(file_name: str, file_content: bytes) -> str:
    file_name = file_name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file_content)
    elif file_name.endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        return "Unsupported file format"

def extract_text_from_pdf(file_content: bytes) -> str:
    text = ""
    try:
        with io.BytesIO(file_content) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        return clean_text(text)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_content: bytes) -> str:
    text = ""
    with io.BytesIO(file_content) as docx_file:
        doc = docx.Document(docx_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return clean_text(text)

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
