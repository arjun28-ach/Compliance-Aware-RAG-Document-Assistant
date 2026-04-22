import json
from app.services.hybrid_retriever import HybridRetriever


def evaluate():
    retriever = HybridRetriever()

    # Load dataset
    with open("data/eval_dataset.json", "r") as f:
        dataset = json.load(f)

    total = len(dataset)
    success = 0

    print("\n📊 Evaluation Started")
    print("----------------------")

    for item in dataset:
        query = item["query"]
        expected = item["expected_keyword"].lower()

        results = retriever.search(query, top_k=5)

        found = False

        for r in results:
            if expected in r["text"].lower():
                found = True
                break

        if found:
            success += 1

        print(f"\nQuery: {query}")
        print(f"Expected: {expected}")
        print(f"Found: {'✅ YES' if found else '❌ NO'}")

    recall_at_5 = success / total

    print("\n📈 FINAL RESULTS")
    print("----------------")
    print(f"Total Queries: {total}")
    print(f"Recall@5: {recall_at_5:.2f}")


if __name__ == "__main__":
    evaluate()