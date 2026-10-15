import os

from src.plantguard.m3.document_loader import PlantGuardDocumentLoader
from src.plantguard.m3.embeddings import PlantGuardEmbedder
from src.plantguard.m3.vector_store import PlantGuardVectorStore

from src.plantguard.m4.bm25_search import PlantGuardBM25
from src.plantguard.m4.hybrid_search import HybridSearch
from src.plantguard.m4.reranker import PlantGuardReranker


class PlantGuardRetrievalService:
    """Reusable M4 retrieval pipeline for M4, M5, and later milestones."""

    def __init__(
        self,
        corpus_path: str = "data/plantguard/corpus",
        candidate_limit: int = 10,
        final_limit: int = 5,
    ):
        self.candidate_limit = candidate_limit
        self.final_limit = final_limit

        loader = PlantGuardDocumentLoader(corpus_path)
        documents = loader.load_markdown_documents()

        all_chunks = []

        for document in documents:
            chunks = loader.chunk_document(document)
            all_chunks.extend(chunks)

        self.all_chunks = all_chunks
        self.bm25 = PlantGuardBM25(all_chunks)
        self.embedder = PlantGuardEmbedder()
        self.vector_store = PlantGuardVectorStore()
        self.hybrid = HybridSearch()
        self.reranker = PlantGuardReranker()

    def retrieve(
        self,
        question: str,
    ) -> list[dict]:
        """Run BM25 + dense + hybrid RRF + reranking."""

        bm25_results = self.bm25.search(
            query=question,
            limit=self.candidate_limit,
        )

        query_vector = self.embedder.embed_query(question)

        dense_results = self.vector_store.search(
            query_vector=query_vector,
            limit=self.candidate_limit,
        )

        hybrid_results = self.hybrid.fuse(
            dense_results=dense_results,
            bm25_results=bm25_results,
            limit=self.candidate_limit,
        )

        reranked_results = self.reranker.rerank(
            query=question,
            results=hybrid_results,
            limit=self.final_limit,
        )

        return self._add_safety_standard_coverage(
            question,
            reranked_results,
        )

    def _add_safety_standard_coverage(
        self,
        question: str,
        results: list[dict],
    ) -> list[dict]:
        """Ensure intent-relevant safety documents remain in retrieval results.

        Coverage is selected from the user's intent, rather than requiring one
        narrow list of exact safety keywords. The asset-specific manual remains
        part of the original ranking whenever possible.
        """
        question_lower = question.casefold()

        required_sources = []

        asks_about_alarm_control = any(term in question_lower for term in (
            "alarm", "suppress", "disable the alarm", "alarm response",
        ))
        asks_about_permit = any(term in question_lower for term in (
            "permit", "paperwork", "work authorization", "authorisation",
            "authorization", "skip the paperwork", "bypass safety",
        ))
        asks_about_energy_isolation = any(term in question_lower for term in (
            "lockout", "tagout", "loto", "isolation", "isolat",
            "high voltage", "live circuit", "live electrical",
            "skip the paperwork", "bypass safety", "bypass lockout",
        ))

        if asks_about_alarm_control:
            required_sources.append("alarm-response.md")
        if asks_about_energy_isolation:
            required_sources.append("lockout-tagout.md")
        if asks_about_permit:
            required_sources.append("permit-to-work.md")

        if not required_sources:
            return results

        def source_for(item):
            current = item
            while isinstance(current, dict) and "result" in current:
                current = current["result"]

            if isinstance(current, dict) and "chunk" in current:
                metadata = current["chunk"].get("metadata", {})
            elif hasattr(current, "payload"):
                metadata = current.payload or {}
            elif isinstance(current, dict):
                metadata = current.get("metadata", {})
            else:
                return None
            return metadata.get("source")

        covered_sources = {source_for(item) for item in results}
        updated = list(results)

        for source in required_sources:
            if source in covered_sources:
                continue

            candidates = [
                chunk for chunk in self.all_chunks
                if chunk.get("metadata", {}).get("source") == source
            ]
            if not candidates:
                continue

            # Prefer a chunk with lexical overlap, but still include a canonical
            # chunk when overlap is zero: the standard itself is required evidence.
            question_tokens = set(question_lower.split())

            def relevance(chunk):
                text = chunk.get("text", "").casefold()
                return sum(
                    1 for token in question_tokens
                    if len(token.strip(".,?!:;()[]{}\"'")) > 3
                    and token.strip(".,?!:;()[]{}\"'") in text
                )

            best_chunk = max(candidates, key=relevance)
            updated.append({
                "result": {
                    "chunk": best_chunk,
                    "score": 0.0,
                },
                "rerank_score": 0.0,
            })
            covered_sources.add(source)

        if len(updated) <= self.final_limit:
            return updated

        added_results = updated[len(results):]
        slots_needed = min(len(added_results), self.final_limit)
        if slots_needed == 0:
            return results[:self.final_limit]

        # Keep required safety documents and use remaining slots for top-ranked
        # retrieval results. This avoids truncating the newly added standards.
        return results[:self.final_limit - slots_needed] + added_results[:slots_needed]
