import fitz

class PDFExtractService:
    """
    Service for extractuing text from PDF files using PyMuPDF (fitz).
    """

    @staticmethod
    def extract_text(pdf_path: str) -> str:

        with fitz.open(pdf_path) as document:
            extracted_text = ""

            for page in document:
                extracted_text += page.get_text()

        return extracted_text    
