from sentence_transformers import CrossEncoder


class PlantGuardReranker:
    """Reranks retrieved chunks using a cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: list,
        limit: int = 5,
    ) -> list[dict]:

        if not results:
            return []

        pairs = []

        for item in results:
            result = item["result"]

            if isinstance(result, dict):
                text = result["chunk"]["text"]
            else:
                text = result.payload["text"]

            pairs.append((query, text))

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(results, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        reranked = []

        for item, score in ranked[:limit]:
            reranked.append(
                {
                    "result": item,
                    "rerank_score": float(score),
                }
            )

        return reranked