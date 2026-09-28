import chromadb

from embedding_model import EmbeddingModel


class Retriever:

    def __init__(
        self,
        chroma_dir="chroma_db",
        collection_name="documents_collection",
        top_k=3,
    ):

        self.embedding_model = EmbeddingModel()

        self.client = chromadb.PersistentClient(
            path=chroma_dir
        )

        self.collection = self.client.get_collection(
            name=collection_name
        )

        self.top_k = top_k


    def retrieve(self, question):

        query_embedding = self.embedding_model.embed(
            [question]
        )[0]

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=self.top_k,
        )

        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0],
        }
