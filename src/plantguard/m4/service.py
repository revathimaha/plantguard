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

        return reranked_results