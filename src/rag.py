from context_builder import build_context
from evidence_checker import EvidenceChecker


class RAG:

    def __init__(self, retriever, generator):

        self.retriever = retriever
        self.generator = generator
        self.evidence_checker = EvidenceChecker()


    def answer(self, question):

        # 1. Retrieve relevant chunks

        results = self.retriever.retrieve(
            question
        )


        # 2. Build context

        context = build_context(
            results
        )


        # 3. Check whether the retrieved
        #    context contains evidence related
        #    to the question

        is_supported = (
            self.evidence_checker.is_supported(
                question,
                context,
            )
        )


        # 4. Refuse unsupported questions

        if not is_supported:

            return {
                "answer": "The information is not available.",
                "sources": [],
                "retrieved": results,
            }


        # 5. Generate answer

        answer = self.generator.generate(
            question,
            context,
        )


        # 6. Build deterministic sources

        answer_sources = []

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

                answer_sources.append(
                    citation
                )

                seen_sources.add(
                    citation
                )


        # 7. Return complete RAG result

        return {
            "answer": answer,
            "sources": answer_sources,
            "retrieved": results,
        }