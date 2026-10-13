class HybridSearch:

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def fuse(
        self,
        dense_results: list,
        bm25_results: list,
        limit: int = 5,
    ):
        scores = {}
        chunks = {}

        # Dense ranking
        for rank, result in enumerate(dense_results, start=1):
            chunk_id = self._get_chunk_id(result)

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1.0 / (self.rrf_k + rank)
            )

            chunks[chunk_id] = result

        # BM25 ranking
        for rank, result in enumerate(bm25_results, start=1):
            chunk_id = self._get_chunk_id(result)

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1.0 / (self.rrf_k + rank)
            )

            chunks[chunk_id] = result

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )[:limit]

        return [
            {
                "result": chunks[chunk_id],
                "rrf_score": scores[chunk_id],
            }
            for chunk_id in ranked_ids
        ]

    def _get_chunk_id(self, result):
        if isinstance(result, dict) and "chunk" in result:
            chunk = result["chunk"]

            return (
                chunk["metadata"]["source"],
                chunk["metadata"]["section"],
                chunk["text"],
            )

        return (
            result.payload["source"],
            result.payload["section"],
            result.payload["text"],
        )