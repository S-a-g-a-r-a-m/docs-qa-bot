import os

import chromadb
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from embedding_model import EmbeddingModel


load_dotenv()


# -------------------------
# 1. Models
# -------------------------

embedding_model = EmbeddingModel()

llm = InferenceClient(
    provider="auto",
    api_key=os.getenv("HF_TOKEN"),
)


# -------------------------
# 2. Chroma
# -------------------------

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_collection(
    name="documents_collection"
)


# -------------------------
# 3. Ask a question
# -------------------------

question = "What raster data was analysed?"
# -------------------------
# 4. Embed the question
# -------------------------

query_embedding = embedding_model.embed(
    [question]
)[0]


# -------------------------
# 5. Retrieve chunks
# -------------------------

results = collection.query(
    query_embeddings=[
        query_embedding.tolist()
    ],
    n_results=3,
)


documents = results["documents"][0]
metadatas = results["metadatas"][0]


# -------------------------
# 6. Build context
# -------------------------

context_parts = []

for document, metadata in zip(
    documents,
    metadatas,
):

    source = metadata["source"]

    citation = f"Source: {source}"

    if "page" in metadata:
        citation += f", Page {metadata['page']}"

    context_parts.append(
        f"[{citation}]\n"
        f"{document}"
    )


context = "\n\n".join(context_parts)


# -------------------------
# 7. Create prompt
# -------------------------

prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the
provided context.

Rules:

1. Do not use outside knowledge.
2. If the answer is not present in the context,
   say that the information is not available.
3. Do not include citations or source references
   in your answer.
4. Answer concisely.

Context:

{context}

Question:

{question}

Answer:
"""


# -------------------------
# 8. Generate answer
# -------------------------

response = llm.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    max_tokens=200,
)


answer = response.choices[0].message.content

print("\nFINISH REASON:")
print(response.choices[0].finish_reason)

# -------------------------
# 9. Display answer
# -------------------------

print("\nANSWER:")
print(answer)


print("\nRETRIEVED SOURCES:")

for metadata in metadatas:

    source = metadata["source"]

    if "page" in metadata:
        print(
            f"- {source}, "
            f"Page {metadata['page']}"
        )
    else:
        print(
            f"- {source}"
        )

