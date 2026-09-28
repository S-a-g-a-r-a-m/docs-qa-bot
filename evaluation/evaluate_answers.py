import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever
from generator import Generator
from rag import RAG


retriever = Retriever(top_k=3)

generator = Generator()

rag = RAG(
    retriever=retriever,
    generator=generator,
)


evaluation_questions = [

    {
        "question": "What percentile levels were used for MAM 2024?",
        "type": "answerable",
        "expected_facts": [
            "50th percentile",
            "95th percentile",
        ],
    },

    {
        "question": "What raster data was analysed?",
        "type": "answerable",
        "expected_facts": [
            "Daily FloodScan (1998-2022)",
            "WorldPop (2020 UN Adjusted)",
        ],
    },

    {
        "question": "What is the capital of France?",
        "type": "unanswerable",
        "expected_facts": [],
    },

        {
        "question": "How were the population exposure estimates calculated?",
        "type": "answerable",
        "expected_facts": [
            "aggregated at the second administrative level",
            "zonal statistics",
            "percent of population exposed",
            "updated 2024 population dataset",
        ],
    },

    {
        "question": "What percentile levels were used for OND 2024?",
        "type": "answerable",
        "expected_facts": [
            "25th percentile",
            "75th percentile",
        ],
    },

    {
        "question": "Who invented the telephone?",
        "type": "unanswerable",
        "expected_facts": [],
    },

    {
        "question": "How does a convolutional neural network work?",
        "type": "unanswerable",
        "expected_facts": [],
    },

]


for item in evaluation_questions:

    question = item["question"]

    print("\n" + "=" * 60)

    print("QUESTION:")
    print(question)

    print(
        "\nEXPECTED TYPE:",
        item["type"],
    )

    print(
        "\nEXPECTED FACTS:"
    )

    if item["expected_facts"]:

        for fact in item["expected_facts"]:
            print("-", fact)

    else:
        print("- No answer should be available.")


    result = rag.answer(question)


    print("\nGENERATED ANSWER:")
    print(result["answer"])


    print("\nSOURCES:")

    for source in result["sources"]:
        print("-", source)
