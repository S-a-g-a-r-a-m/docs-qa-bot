import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1] / "src"
    )
)
from retriever import Retriever


retriever = Retriever(top_k=5)


# -------------------------
# Ground-truth evaluation set
# -------------------------

evaluation_questions = {

    # -------------------------
    # Answerable questions
    # -------------------------

    "What raster data was analysed?": {
        "expected": "relevant",
        "ground_truth_chunk": 1,
    },

    "How were the yearly seasonal flood fraction rasters processed?": {
        "expected": "relevant",
        "ground_truth_chunk": 2,
    },

    "How were the population exposure estimates calculated?": {
        "expected": "relevant",
        "ground_truth_chunk": 4,
    },

    "What percentile levels were used for MAM 2024?": {
        "expected": "relevant",
        "ground_truth_chunk": 6,
    },

    "What percentile levels were used for OND 2024?": {
        "expected": "relevant",
        "ground_truth_chunk": 6,
    },

    "What seasons were analysed?": {
        "expected": "relevant",
        "ground_truth_chunk": 1,
    },

    "What threshold was used for binary reclassification?": {
        "expected": "relevant",
        "ground_truth_chunk": 2,
    },

    "What population raster was used?": {
        "expected": "relevant",
        "ground_truth_chunk": 3,
    },

    "At what administrative level were the estimates initially aggregated?": {
        "expected": "relevant",
        "ground_truth_chunk": 4,
    },

    "How were the exposure ranges combined?": {
        "expected": "relevant",
        "ground_truth_chunk": 7,
    },


    # -------------------------
    # Unanswerable questions
    # -------------------------

    "What programming language was used to create this methodology?": {
        "expected": "irrelevant",
    },

    "What is the boiling point of water?": {
        "expected": "irrelevant",
    },

    "Who wrote Hamlet?": {
        "expected": "irrelevant",
    },

    "What is the latest version of Python?": {
        "expected": "irrelevant",
    },

    "How does backpropagation work in neural networks?": {
        "expected": "irrelevant",
    },
}


# -------------------------
# Recall counters
# -------------------------

recall_at_1_hits = 0
recall_at_3_hits = 0

answerable_questions = 0


# -------------------------
# Evaluate retrieval
# -------------------------

for question, information in evaluation_questions.items():

    results = retriever.retrieve(question)

    chunks = results["metadatas"]

    retrieved_chunks = [
        metadata["chunk"]
        for metadata in chunks
    ]

    distances = results["distances"]

    ground_truth = information.get(
        "ground_truth_chunk"
    )


    # -------------------------
    # Distance features
    # -------------------------

    best_distance = distances[0]

    second_distance = distances[1]

    third_distance = distances[2]

    gap_1_2 = (
        second_distance
        - best_distance
    )

    gap_1_3 = (
        third_distance
        - best_distance
    )

    mean_top_3 = (
        best_distance
        + second_distance
        + third_distance
    ) / 3


    print("\n" + "=" * 60)

    print("QUESTION:")

    print(question)


    print(
        f"\nRetrieved chunks: "
        f"{retrieved_chunks}"
    )


    print(
        f"Distances: "
        f"{[round(distance, 4) for distance in distances]}"
    )


    print(
        f"\nBest distance: "
        f"{best_distance:.4f}"
    )


    print(
        f"Gap 1→2: "
        f"{gap_1_2:.4f}"
    )


    print(
        f"Gap 1→3: "
        f"{gap_1_3:.4f}"
    )


    print(
        f"Mean top-3: "
        f"{mean_top_3:.4f}"
    )


    # -------------------------
    # Answerable question
    # -------------------------

    if ground_truth is not None:

        answerable_questions += 1

        hit_at_1 = (
            ground_truth
            in retrieved_chunks[:1]
        )

        hit_at_3 = (
            ground_truth
            in retrieved_chunks[:3]
        )


        if hit_at_1:

            recall_at_1_hits += 1


        if hit_at_3:

            recall_at_3_hits += 1


        print(
            f"\nGround-truth chunk: "
            f"{ground_truth}"
        )


        print(
            f"Recall@1 hit: "
            f"{hit_at_1}"
        )


        print(
            f"Recall@3 hit: "
            f"{hit_at_3}"
        )


    # -------------------------
    # Unanswerable question
    # -------------------------

    else:

        print(
            "\nQuestion type: "
            "Unanswerable"
        )


# -------------------------
# Final metrics
# -------------------------

recall_at_1 = (
    recall_at_1_hits
    / answerable_questions
)

recall_at_3 = (
    recall_at_3_hits
    / answerable_questions
)


print("\n" + "=" * 60)

print("RETRIEVAL EVALUATION")


print(
    f"\nAnswerable questions: "
    f"{answerable_questions}"
)


print(
    f"Recall@1: "
    f"{recall_at_1_hits}/{answerable_questions} "
    f"= {recall_at_1:.2%}"
)


print(
    f"Recall@3: "
    f"{recall_at_3_hits}/{answerable_questions} "
    f"= {recall_at_3:.2%}"
)