import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever
from rag import RAG
from generator import Generator


retriever = Retriever(top_k=3)

generator = Generator()

rag = RAG(
    retriever=retriever,
    generator=generator,
)


question = "What raster data was analysed?"

result = rag.answer(question)


print("\nANSWER:")
print(result["answer"])


print("\nSOURCES:")

for source in result["sources"]:
    print("-", source)