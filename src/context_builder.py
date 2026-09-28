def build_context(results):

    context_parts = []

    for document, metadata in zip(
        results["documents"],
        results["metadatas"],
    ):

        source = metadata["source"]

        citation = f"Source: {source}"

        if "page" in metadata:
            citation += f", Page {metadata['page']}"

        context_parts.append(
            f"[{citation}]\n"
            f"{document}"
        )

    return "\n\n".join(context_parts)
