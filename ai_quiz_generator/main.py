from tkinter import *
from tkinter import filedialog
from google import genai
from google.genai import types
from docx import Document
from fpdf import FPDF
import mimetypes
import pathlib


def findFile():
    dialog = Tk()
    dialog.withdraw()
    path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx"),
            ("All supported", "*.pdf *.docx"),
        ]
    )
    dialog.destroy()
    return path


def docx_to_text(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def guess_mime_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type

def sanitize_for_pdf(text):
    replacements = {
        "\u2018": "'",  
        "\u2019": "'",  
        "\u201c": '"',  
        "\u201d": '"',  
        "\u2013": "-",  
        "\u2014": "-",  
        "\u2026": "...",  
    }
    for smart, plain in replacements.items():
        text = text.replace(smart, plain)
    return text.encode("latin-1", "ignore").decode("latin-1")  # drop anything else unsupported

def save_as_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, sanitize_for_pdf(text))
    pdf.output(output_path)


def save_response(text):
    save_path = filedialog.asksaveasfilename(
        title="Save summary as",
        defaultextension=".pdf",
        filetypes=[("PDF file", "*.pdf")]
    )
    if not save_path:
        print("Save cancelled.")
        return

    save_as_pdf(text, save_path)
    print("Saved to:", save_path)


def main():
    client = genai.Client()
    path = findFile()

    if not path:
        print("No file selected.")
        return

    prompt = """
        Based on the content of this document, generate a comprehensive quiz to test understanding of the material.

        Requirements:
        - Create questions minimum of 25 and max of 50 depends on the file submitted, covering the full range of the document (not just the intro).
        - Mix question types: multiple choice (3 options each), true/false, short answer.
        - Vary difficulty: include recall questions (facts, definitions) and application/analysis questions (why/how, cause-effect, comparisons).
        - Cover different sections/topics of the document proportionally — don't cluster all questions on one part.
        - In the last part of the reviewer, create an asnwer key section, and a bried descriptions.

        Format Example:
        Q1. [Type: Multiple Choice]
        [question text]
        A) ...
        B) ...
        C) ...
        D) ...

        And in the last part of the reviewer is the answer key.
        Multiple Choice
        1. [letter] — [brief explanation]

        """

    if path.endswith(".docx"):
        file_part = docx_to_text(path)
    else:
        mime_type = guess_mime_type(path)
        file_path = pathlib.Path(path)
        pdf_data = file_path.read_bytes()
        file_part = types.Part.from_bytes(
            data=pdf_data,
            mime_type=mime_type
        )

    chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="""
            - Limit your responses within 1000 words.
            - Automatically detect when a line is becoming too long.
            - Wrap text naturally without breaking words unnecessarily.
            - Prefer wrapping at spaces, punctuation, or sentence boundaries.
            - Keep words intact whenever possible.
            - Preserve the original text and meaning.
            - Do not add unnecessary line breaks.
            - Make the result look clean, balanced, and easy to read.""",
            temperature=0.3
        )
    )

    AIresponse = chat.send_message([file_part, prompt])
    print(AIresponse.text)

    save_response(AIresponse.text)


if __name__ == "__main__":
    main()






