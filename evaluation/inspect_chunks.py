import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever


retriever = Retriever(top_k=5)


questions = [
    "What seasons were analysed?",
    "What threshold was used for binary reclassification?",
    "What population raster was used?",
    "At what administrative level were the estimates initially aggregated?",
    "How were the exposure ranges combined?",
]


for question in questions:

    results = retriever.retrieve(question)

    print("\n" + "=" * 60)
    print("QUESTION:")
    print(question)

    for document, metadata, distance in zip(
        results["documents"],
        results["metadatas"],
        results["distances"],
    ):

        print("\n" + "-" * 60)

        print(
            f"Chunk: {metadata['chunk']}"
        )

        print(
            f"Page: {metadata.get('page', 'N/A')}"
        )

        print(
            f"Distance: {distance:.4f}"
        )

        print("\nText:")
        print(document)