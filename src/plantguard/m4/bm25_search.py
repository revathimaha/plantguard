import re

from rank_bm25 import BM25Okapi


class PlantGuardBM25:

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks

        tokenized_chunks = [
            self._tokenize(chunk["text"])
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(
            r"\b\w+(?:\.\w+)?\b",
            text.lower(),
        )

    def search(
        self,
        query: str,
        limit: int = 5,
    ):
        query_tokens = self._tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:limit]

        return [
            {
                "chunk": self.chunks[index],
                "score": float(scores[index]),
            }
            for index in ranked_indices
        ]
    