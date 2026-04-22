def recall_at_k(relevant_docs, retrieved_docs, k):
    retrieved_k = retrieved_docs[:k]

    hits = sum(1 for doc in retrieved_k if doc in relevant_docs)

    if not relevant_docs:
        return 0

    return hits / len(relevant_docs)


def mrr(relevant_docs, retrieved_docs):
    for i, doc in enumerate(retrieved_docs):
        if doc in relevant_docs:
            return 1 / (i + 1)

    return 0