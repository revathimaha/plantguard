import hashlib
import json
import os
import time

from langchain_google_genai import GoogleGenerativeAIEmbeddings


class PlantGuardEmbedder:

    def __init__(
        self,
        model: str = "gemini-embedding-001",
        cache_dir: str = ".embcache",
    ):
        self.model = model
        self.cache_dir = cache_dir

        os.makedirs(self.cache_dir, exist_ok=True)

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=self.model
        )

    def _cache_key(self, text: str) -> str:
        return hashlib.sha1(
            (self.model + "::" + text).encode("utf-8")
        ).hexdigest()

    def _cache_path(self, text: str) -> str:
        return os.path.join(
            self.cache_dir,
            self._cache_key(text) + ".json",
        )

    def _get_cached(self, text: str):
        path = self._cache_path(text)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        return None

    def _save_cached(self, text: str, vector: list[float]):
        path = self._cache_path(text)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(vector, f)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        results = [None] * len(texts)
        missing = []

        for index, text in enumerate(texts):
            cached = self._get_cached(text)

            if cached is not None:
                results[index] = cached
            else:
                missing.append(index)

        print(
            f"Embedding {len(missing)} new chunks "
            f"({len(texts) - len(missing)} cached)"
        )

        # Day 2 lab uses throttled batches.
        batch_size = 90

        for start in range(0, len(missing), batch_size):
            batch_indices = missing[start:start + batch_size]

            batch_texts = [
                texts[index]
                for index in batch_indices
            ]

            vectors = self.embedding_model.embed_documents(
                batch_texts
            )

            for index, vector in zip(batch_indices, vectors):
                results[index] = vector
                self._save_cached(texts[index], vector)

            if start + batch_size < len(missing):
                print("Pausing before next embedding batch...")
                time.sleep(60)

        return results

    def embed_query(self, query: str) -> list[float]:
        cached = self._get_cached(query)

        if cached is not None:
            return cached

        vector = self.embedding_model.embed_query(query)

        self._save_cached(query, vector)

        return vector