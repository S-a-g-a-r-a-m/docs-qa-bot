
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class Generator:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model_name = "gemini-3.5-flash-lite"


    def generate(self, question, context):

        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided context.

Rules:

1. Do not use outside knowledge.
2. If the answer is not present in the context,
   say that the information is not available.
3. Do not include citations or source references.
4. Include all important facts needed to answer
   the question.
5. For multi-part answers, use a numbered list.
6. Do not add explanations that are not necessary
   to answer the question.

Context:

{context}

Question:

{question}

Answer:
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text
