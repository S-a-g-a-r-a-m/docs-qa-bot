import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from pathlib import Path

from document_loader import load_document


documents_dir = Path("documents")


for file_path in documents_dir.iterdir():

    documents = load_document(file_path)

    print(f"\nFILE: {file_path.name}")
    print(f"Loaded sections: {len(documents)}")

    for document in documents[:2]:

        print("\nMetadata:")
        print(document["metadata"])

        print("\nText:")
        print(document["text"][:300])