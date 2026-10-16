from pathlib import Path


# class PlantGuardDocumentLoader:

#     def __init__(self, corpus_path: str):
#         self.corpus_path = Path(corpus_path)

#     def load_documents(self) -> list[dict]:
#         documents = []

#         for file_path in self.corpus_path.glob("*.txt"):
#             text = file_path.read_text(encoding="utf-8")

#             documents.append({
#                 "source": file_path.name,
#                 "text": text,
#             })

#         return documents


from pathlib import Path


class PlantGuardDocumentLoader:

    def __init__(self, corpus_path: str):
        self.corpus_path = Path(corpus_path)

    def load_markdown_documents(self) -> list[dict]:
        documents = []

        markdown_path = self.corpus_path / "markdown"

        for file_path in sorted(markdown_path.glob("*.md")):
            text = file_path.read_text(encoding="utf-8")

            documents.append({
                "source": file_path.name,
                "file_type": "markdown",
                "text": text,
            })

        return documents

    def load_pdf_documents(self) -> list[dict]:
        from pypdf import PdfReader

        documents = []

        pdf_path = self.corpus_path / "pdf"

        for file_path in sorted(pdf_path.glob("*.pdf")):
            reader = PdfReader(str(file_path))

            pages = [
                page.extract_text() or ""
                for page in reader.pages
            ]
            text = "\n\n".join(pages).strip()

            if not text:
                continue

            documents.append({
                "source": file_path.name,
                "file_type": "pdf",
                "text": text,
            })

        return documents
    
    def chunk_document(
            self,
            document: dict,
            max_chars: int = 2000,
        ) -> list[dict]:

        lines = document["text"].splitlines()

        sections = []
        current_section = None
        current_lines = []

        # First: split document by headings
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("#"):
                if current_lines:
                    sections.append({
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                    })

                current_section = stripped.lstrip("#").strip()
                current_lines = [line]

            else:
                current_lines.append(line)

        if current_lines:
            sections.append({
                "section": current_section,
                "text": "\n".join(current_lines).strip(),
            })

        # Second: split oversized sections
        chunks = []

        for section in sections:
            text = section["text"]

            if len(text) <= max_chars:
                chunks.append({
                    "text": text,
                    "metadata": {
                        "source": document["source"],
                        "section": section["section"],
                    },
                })
                continue

            # Split large sections by paragraphs
            paragraphs = text.split("\n\n")

            current_text = ""

            for paragraph in paragraphs:
                if not paragraph.strip():
                    continue

                if (
                    current_text
                    and len(current_text) + len(paragraph) + 2
                    > max_chars
                ):
                    chunks.append({
                        "text": current_text.strip(),
                        "metadata": {
                            "source": document["source"],
                            "section": section["section"],
                        },
                    })

                    current_text = paragraph
                else:
                    if current_text:
                        current_text += "\n\n"

                    current_text += paragraph

            if current_text.strip():
                chunks.append({
                    "text": current_text.strip(),
                    "metadata": {
                        "source": document["source"],
                        "section": section["section"],
                    },
                })

        return chunks