import fitz  # PyMuPDF
import docx

def extract_text(file_path, ext):
    try:
        if ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == 'pdf':
            doc = fitz.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        elif ext == 'docx':
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        else:
            return None
    except Exception as e:
        print(f"Text extraction failed: {e}")
        return None