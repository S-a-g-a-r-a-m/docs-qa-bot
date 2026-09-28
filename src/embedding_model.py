import os

import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


class EmbeddingModel:

    def __init__(self):
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HF_TOKEN"),
        )

        self.model_name = "BAAI/bge-small-en-v1.5"

    def embed(self, texts):
        embeddings = self.client.feature_extraction(
            texts,
            model=self.model_name,
        )

        return np.array(embeddings)