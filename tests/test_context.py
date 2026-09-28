import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever
from context_builder import build_context



retriever = Retriever(top_k=3)

question = "What raster data was analysed?"

results = retriever.retrieve(question)

context = build_context(results)

print("\nCONTEXT:")
print(context)