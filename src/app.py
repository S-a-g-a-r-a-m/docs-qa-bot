import streamlit as st

from retriever import Retriever
from generator import Generator
from rag import RAG


# -------------------------
# Page configuration
# -------------------------

st.set_page_config(
    page_title="Docs Q&A Bot",
    page_icon="📚",
    layout="wide",
)


# -------------------------
# Initialize RAG pipeline
# -------------------------

@st.cache_resource
def load_rag():

    retriever = Retriever(
        top_k=3
    )

    generator = Generator()

    return RAG(
        retriever=retriever,
        generator=generator,
    )


rag = load_rag()


# -------------------------
# UI
# -------------------------

st.title("📚 Docs Q&A Bot")

st.write(
    "Ask questions about the documents "
    "stored in the knowledge base."
)


question = st.text_input(
    "Ask a question",
    placeholder="What raster data was analysed?",
)


if question:

    with st.spinner("Searching documents and generating answer..."):

        result = rag.answer(question)


    # -------------------------
    # Answer
    # -------------------------

    st.subheader("Answer")

    st.write(
        result["answer"]
    )


    # -------------------------
    # Sources
    # -------------------------

    st.subheader("Sources")

    for source in result["sources"]:

        st.write(
            f"- {source}"
        )


    # -------------------------
    # Retrieved chunks
    # -------------------------

    with st.expander("Retrieved chunks"):

        documents = result["retrieved"]["documents"]
        metadatas = result["retrieved"]["metadatas"]
        distances = result["retrieved"]["distances"]


        for i, (
            document,
            metadata,
            distance,
        ) in enumerate(
            zip(
                documents,
                metadatas,
                distances,
            )
        ):

            st.markdown(
                f"**Result {i + 1}**"
            )

            st.write(
                f"Distance: {distance:.4f}"
            )

            if "page" in metadata:

                st.write(
                    f"Source: {metadata['source']} "
                    f"— Page {metadata['page']}"
                )

            else:

                st.write(
                    f"Source: {metadata['source']}"
                )

            st.write(document)

            st.divider()
