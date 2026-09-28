import chromadb

from embedding_model import EmbeddingModel


CHROMA_DIR = "chroma_db"


QUESTIONS = [
    # Relevant
    ("What raster data was analysed?", True),
    ("How were the yearly seasonal flood fraction rasters processed?", True),
    ("How were the population exposure estimates calculated?", True),
    ("What percentile levels were used for MAM 2024?", True),
    ("What percentile levels were used for OND 2024?", True),

    # Irrelevant
    ("What is the capital of France?", False),
    ("Who invented the telephone?", False),
    ("What is the boiling point of water?", False),
    ("How does a convolutional neural network work?", False),
    ("What is the population of India?", False),
]


def main():

    # -------------------------
    # Connect to Chroma
    # -------------------------

    client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )

    collection = client.get_collection(
        name="documents_collection"
    )

    embedding_model = EmbeddingModel()


    # -------------------------
    # Evaluate questions
    # -------------------------

    for question, expected_relevant in QUESTIONS:

        query_embedding = embedding_model.embed(
            [question]
        )[0]

        results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=3,
        )

        distances = results["distances"][0]

        print("\n" + "=" * 60)
        print("QUESTION:")
        print(question)

        print(
            "\nEXPECTED:",
            "RELEVANT" if expected_relevant
            else "IRRELEVANT"
        )

        print("\nDISTANCES:")

        for i, distance in enumerate(distances):

            print(
                f"Result {i + 1}: "
                f"{distance:.4f}"
            )


if __name__ == "__main__":
    main()
