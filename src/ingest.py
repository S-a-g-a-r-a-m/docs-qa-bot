from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document_loader import load_document
from embedding_model import EmbeddingModel


DOCUMENTS_DIR = Path("documents")
CHROMA_DIR = "chroma_db"


def main():

    # -------------------------
    # 1. Find documents
    # -------------------------

    files = [
        file_path
        for file_path in DOCUMENTS_DIR.iterdir()
        if file_path.suffix.lower() in [".md", ".pdf"]
    ]

    print(f"Found {len(files)} files.")


    # -------------------------
    # 2. Load documents
    # -------------------------

    loaded_documents = []

    for file_path in files:

        documents = load_document(file_path)

        print(
            f"Loaded {file_path.name}: "
            f"{len(documents)} sections"
        )

        loaded_documents.extend(documents)


    print(
        f"Total loaded sections: "
        f"{len(loaded_documents)}"
    )


    # -------------------------
    # 3. Chunk documents
    # -------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
    )

    chunks = []
    chunk_metadata = []

    for document in loaded_documents:

        document_chunks = splitter.split_text(
            document["text"]
        )

        for chunk in document_chunks:

            chunks.append(chunk)

            chunk_metadata.append(
                document["metadata"].copy()
            )


    print(f"Total chunks: {len(chunks)}")


    # -------------------------
    # 4. Create embeddings
    # -------------------------

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.embed(chunks)

    print(
        f"Embedding shape: "
        f"{embeddings.shape}"
    )


    # -------------------------
    # 5. Connect to Chroma
    # -------------------------

    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )

    collection = client.get_or_create_collection(
        name="documents_collection"
    )


    # -------------------------
    # 6. Create IDs
    # -------------------------

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]


    # -------------------------
    # 7. Add chunk numbers
    # -------------------------

    for i, metadata in enumerate(
        chunk_metadata
    ):
        metadata["chunk"] = i


    # -------------------------
    # 8. Store everything
    # -------------------------

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=chunk_metadata,
    )


    print("Ingestion complete.")


if __name__ == "__main__":
    main()