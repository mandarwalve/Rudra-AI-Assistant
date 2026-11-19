
import os
from pathlib import Path
from tkinter import Tk, filedialog

from pypdf import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)

    if reader.is_encrypted:
        raise ValueError("This PDF is password protected.")

    pages = []

    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n--- Page {number} ---\n{text}")

    result = "\n".join(pages)

    if not result.strip():
        return "No readable text found. This may be a scanned PDF."

    return result


def read_docx(file_path):
    try:
        from docx import Document
    except ImportError:
        return "Install Word support using: python -m pip install python-docx"

    document = Document(file_path)
    content = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            content.append(paragraph.text)

    # Also read tables
    for table in document.tables:
        for row in table.rows:
            content.append(" | ".join(cell.text for cell in row.cells))

    return "\n".join(content) or "No readable text found."


def read_txt(file_path):
    encodings = ["utf-8", "utf-16", "cp1252"]

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeError:
            continue

    raise ValueError("Could not decode this text file.")


def read_document(file_path):
    if not os.path.isfile(file_path):
        return "Error: File does not exist."

    extension = Path(file_path).suffix.lower()

    try:
        if extension == ".pdf":
            return read_pdf(file_path)

        elif extension == ".docx":
            return read_docx(file_path)

        elif extension == ".txt":
            return read_txt(file_path)

        else:
            return "Unsupported file format. Use PDF, DOCX, or TXT."

    except Exception as error:
        return f"Document reading error: {error}"


def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select a document for RUDRA",
        filetypes=[
            ("Supported Documents", "*.pdf *.docx *.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    root.destroy()

    if not file_path:
        print("No document selected.")
        return

    print(f"\nReading: {os.path.basename(file_path)}")

    content = read_document(file_path)

    print("\n" + "=" * 50)
    print("DOCUMENT CONTENT")
    print("=" * 50)
    print(content)
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
