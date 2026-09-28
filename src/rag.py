
from retriever import Retriever
from context_builder import build_context


class RAG:

    def __init__(self, retriever, generator):

        self.retriever = retriever
        self.generator = generator


    def answer(self, question):

        # 1. Retrieve relevant chunks
        results = self.retriever.retrieve(question)

        # 2. Build context for the generator
        context = build_context(results)

        # 3. Generate answer
        answer = self.generator.generate(
            question,
            context,
        )

        # 4. Build deterministic sources
        sources = []

        seen_sources = set()

        for metadata in results["metadatas"]:

            source = metadata["source"]

            if "page" in metadata:
                citation = (
                    f"{source}, "
                    f"Page {metadata['page']}"
                )
            else:
                citation = source

            if citation not in seen_sources:
                sources.append(citation)
                seen_sources.add(citation)

        return {
            "answer": answer,
            "sources": sources,
            "retrieved": results,
        }
