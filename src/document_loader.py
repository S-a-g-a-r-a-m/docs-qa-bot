from pathlib import Path

from pypdf import PdfReader


def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [
        {
            "text": text,
            "metadata": {
                "source": file_path.name,
            },
        }
    ]



from pathlib import Path

from pypdf import PdfReader


def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [
        {
            "text": text,
            "metadata": {
                "source": file_path.name,
            },
        }
    ]


def clean_pdf_text(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    paragraphs = []

    current_paragraph = []

    for line in lines:

        current_paragraph.append(line)

        # Treat a line ending with punctuation as
        # a possible paragraph boundary.
        if line.endswith((".", ":", ";")):

            paragraphs.append(
                " ".join(current_paragraph)
            )

            current_paragraph = []

    if current_paragraph:
        paragraphs.append(
            " ".join(current_paragraph)
        )

    return "\n\n".join(paragraphs)


def load_pdf(file_path):

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():

            cleaned_text = clean_pdf_text(text)

            documents.append(
                {
                    "text": cleaned_text,
                    "metadata": {
                        "source": file_path.name,
                        "page": page_number + 1,
                    },
                }
            )

    return documents


def load_document(file_path):

    suffix = file_path.suffix.lower()

    if suffix == ".md":
        return load_markdown(file_path)

    if suffix == ".pdf":
        return load_pdf(file_path)

    return []




def load_document(file_path):

    suffix = file_path.suffix.lower()

    if suffix == ".md":
        return load_markdown(file_path)

    if suffix == ".pdf":
        return load_pdf(file_path)

    return []