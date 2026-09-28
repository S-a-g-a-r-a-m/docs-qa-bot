import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever


retriever = Retriever(top_k=3)

question = "What raster data was analysed?"

results = retriever.retrieve(question)


for i, (document, metadata, distance) in enumerate(
    zip(
        results["documents"],
        results["metadatas"],
        results["distances"],
    )
):

    print(f"\nRESULT {i + 1}")
    print("Distance:", distance)
    print("Metadata:", metadata)
    print("Document:")
    print(document)