import chromadb

from embedding_model import EmbeddingModel


CHROMA_DIR = "chroma_db"


def main():

    # -------------------------
    # 1. Connect to Chroma
    # -------------------------

    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )

    collection = client.get_collection(
        name="documents_collection"
    )


    # -------------------------
    # 2. Create embedding model
    # -------------------------

    embedding_model = EmbeddingModel()


    # -------------------------
    # 3. User question
    # -------------------------

    question = "What raster data was analysed?"

    # -------------------------
    # 4. Embed the question
    # -------------------------

    query_embedding = embedding_model.embed(
        [question]
    )[0]


    # -------------------------
    # 5. Search Chroma
    # -------------------------

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3,
    )


    # -------------------------
    # 6. Display results
    # -------------------------

    for i, document in enumerate(
        results["documents"][0]
    ):
        print(f"\n--- Result {i + 1} ---")
        print(document)

        print(
            "Distance:",
            results["distances"][0][i]
        )

        print(
            "Metadata:",
            results["metadatas"][0][i]
        )


if __name__ == "__main__":
    main()