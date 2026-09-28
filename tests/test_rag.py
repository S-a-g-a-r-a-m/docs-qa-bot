
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


class FakeGenerator:

    def generate(self, question, context):

        return (
            "FAKE ANSWER\n\n"
            f"Question: {question}\n\n"
            "The generator received the retrieved context successfully."
        )


retriever = Retriever(top_k=3)

generator = FakeGenerator()

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