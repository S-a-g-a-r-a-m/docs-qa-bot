import ollama


class Generator:

    def __init__(self):

        self.model_name = "qwen2.5:3b"


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
6. Do not add unnecessary explanations.

Context:

{context}

Question:

{question}

Answer:
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]