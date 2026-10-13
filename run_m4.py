import os
import json

from dotenv import load_dotenv

from src.plantguard.m3.document_loader import PlantGuardDocumentLoader
from src.plantguard.m3.embeddings import PlantGuardEmbedder
from src.plantguard.m3.vector_store import PlantGuardVectorStore

from src.plantguard.m4.bm25_search import PlantGuardBM25
from src.plantguard.m4.hybrid_search import HybridSearch
from src.plantguard.m4.reranker import PlantGuardReranker
from src.plantguard.m4.rag import PlantGuardRAG
from src.plantguard.m4.evaluation import PlantGuardEvaluator

from src.plantguard.llm.client import LLMClient



load_dotenv()


def main():

    # =========================================================
    # 1. LOAD PLANTGUARD DOCUMENTS
    # =========================================================

    loader = PlantGuardDocumentLoader(
        "data/plantguard/corpus"
    )

    documents = loader.load_markdown_documents()

    print(f"Loaded {len(documents)} documents")


    # =========================================================
    # 2. CREATE CHUNKS
    # =========================================================

    all_chunks = []

    for document in documents:

        chunks = loader.chunk_document(document)

        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")


    # =========================================================
    # 3. BUILD BM25 INDEX
    # =========================================================

    bm25 = PlantGuardBM25(all_chunks)


    # =========================================================
    # 4. CREATE EMBEDDING + VECTOR STORE
    # =========================================================

    embedder = PlantGuardEmbedder()

    vector_store = PlantGuardVectorStore()


    # =========================================================
    # 5. CREATE HYBRID SEARCH + RERANKER
    # =========================================================

    hybrid = HybridSearch()

    reranker = PlantGuardReranker()


    # =========================================================
    # 6. REUSABLE RETRIEVAL PIPELINE
    # =========================================================

    def retrieve(question, candidate_limit=10, final_limit=5):

        # -------------------------
        # BM25 retrieval
        # -------------------------

        bm25_results = bm25.search(
            query=question,
            limit=candidate_limit,
        )


        # -------------------------
        # Dense retrieval
        # -------------------------

        query_vector = embedder.embed_query(question)

        dense_results = vector_store.search(
            query_vector=query_vector,
            limit=candidate_limit,
        )


        # -------------------------
        # Hybrid RRF
        # -------------------------

        hybrid_results = hybrid.fuse(
            dense_results=dense_results,
            bm25_results=bm25_results,
            limit=candidate_limit,
        )


        # -------------------------
        # Cross-encoder reranking
        # -------------------------

        reranked_results = reranker.rerank(
            query=question,
            results=hybrid_results,
            limit=final_limit,
        )

        return (
            bm25_results,
            dense_results,
            hybrid_results,
            reranked_results,
        )


    # =========================================================
    # 7. DEMO QUERY
    # =========================================================

    # Normal grounded-RAG query
    query = "What are the P1 vibration alarm thresholds?"

    # Insufficient-evidence test
    # query = (
    #     "What is the exact salary of the technician "
    #     "responsible for CNC-MILL-03?"
    # )

    # Prompt-injection test
    # This was already tested successfully.
    # query = "Is CNC-MILL-03 safe to operate?"


    # =========================================================
    # 8. RUN RETRIEVAL PIPELINE FOR DEMO QUERY
    # =========================================================

    (
        bm25_results,
        dense_results,
        hybrid_results,
        reranked_results,
    ) = retrieve(
        question=query,
        candidate_limit=10,
        final_limit=5,
    )


    # =========================================================
    # 9. PRINT BM25 RESULTS
    # =========================================================

    print("\n--- BM25 SEARCH ---")

    print("Query:", query)

    for rank, result in enumerate(
        bm25_results[:5],
        start=1,
    ):

        chunk = result["chunk"]

        print(f"\nResult {rank}")

        print("Score:", result["score"])

        print(
            "Source:",
            chunk["metadata"]["source"],
        )

        print(
            "Section:",
            chunk["metadata"]["section"],
        )

        print("Text:")

        print(
            chunk["text"][:500]
        )


    # =========================================================
    # 10. PRINT DENSE RESULTS
    # =========================================================

    print("\n--- DENSE SEARCH ---")

    for rank, result in enumerate(
        dense_results[:5],
        start=1,
    ):

        print(f"\nResult {rank}")

        print("Score:", result.score)

        print(
            "Source:",
            result.payload["source"],
        )

        print(
            "Section:",
            result.payload["section"],
        )

        print("Text:")

        print(
            result.payload["text"][:500]
        )


    # =========================================================
    # 11. PRINT HYBRID RRF RESULTS
    # =========================================================

    print("\n--- HYBRID RRF SEARCH ---")

    for rank, item in enumerate(
        hybrid_results[:5],
        start=1,
    ):

        result = item["result"]

        print(f"\nResult {rank}")

        print(
            "RRF score:",
            item["rrf_score"],
        )

        if isinstance(result, dict):

            chunk = result["chunk"]

            print(
                "Source:",
                chunk["metadata"]["source"],
            )

            print(
                "Section:",
                chunk["metadata"]["section"],
            )

            print("Text:")

            print(
                chunk["text"][:500]
            )

        else:

            print(
                "Source:",
                result.payload["source"],
            )

            print(
                "Section:",
                result.payload["section"],
            )

            print("Text:")

            print(
                result.payload["text"][:500]
            )


    # =========================================================
    # 12. PRINT RERANKED RESULTS
    # =========================================================

    print("\n--- RERANKED RESULTS ---")

    for rank, item in enumerate(
        reranked_results,
        start=1,
    ):

        hybrid_item = item["result"]

        result = hybrid_item["result"]

        print(f"\nResult {rank}")

        print(
            "Rerank score:",
            item["rerank_score"],
        )

        if isinstance(result, dict):

            chunk = result["chunk"]

            print(
                "Source:",
                chunk["metadata"]["source"],
            )

            print(
                "Section:",
                chunk["metadata"]["section"],
            )

            print("Text:")

            print(
                chunk["text"][:500]
            )

        else:

            print(
                "Source:",
                result.payload["source"],
            )

            print(
                "Section:",
                result.payload["section"],
            )

            print("Text:")

            print(
                result.payload["text"][:500]
            )


    # =========================================================
    # 13. GROUNDED RAG
    # =========================================================

    rag = PlantGuardRAG(
        llm_client=LLMClient(
            "groq/openai/gpt-oss-20b",
            api_key=os.environ["GROQ_API_KEY"],
        )
    )


    rag_result = rag.answer(
        query=query,
        reranked_results=reranked_results,
    )


    # =========================================================
    # 14. PRINT GROUNDED ANSWER
    # =========================================================

    print("\n--- GROUNDED RAG ANSWER ---")

    print(
        rag_result["answer"]
    )


    # =========================================================
    # 15. PRINT SOURCES
    # =========================================================

    print("\n--- SOURCES ---")

    for source in rag_result["sources"]:

        print(
            source["id"],
            source["source"],
            "|",
            source["section"],
        )


    # =========================================================
    # 16. GOLDEN RETRIEVAL EVALUATION
    # =========================================================

    golden_path = (
        "src/plantguard/m4/golden_questions.json"
    )

    with open(
        golden_path,
        "r",
        encoding="utf-8",
    ) as f:

        golden_questions = json.load(f)


    evaluator = PlantGuardEvaluator(
        golden_questions=golden_questions
    )


    def retrieval_for_evaluation(question):

        (
            _bm25_results,
            _dense_results,
            _hybrid_results,
            reranked_results,
        ) = retrieve(
            question=question,
            candidate_limit=10,
            final_limit=5,
        )

        return reranked_results


    evaluation = evaluator.evaluate(
        retrieval_function=retrieval_for_evaluation,
        k=5,
    )


    # =========================================================
    # 17. PRINT EVALUATION METRICS
    # =========================================================

    print("\n--- GOLDEN RETRIEVAL EVALUATION ---")

    print(
        f"Precision@5: "
        f"{evaluation['precision_at_k']:.3f}"
    )

    print(
        f"Recall@5:    "
        f"{evaluation['recall_at_k']:.3f}"
    )

    print(
        f"MRR:         "
        f"{evaluation['mrr']:.3f}"
    )


    # =========================================================
    # 18. PRINT PER-QUESTION RESULTS
    # =========================================================

    print("\n--- PER QUESTION ---")

    for result in evaluation["questions"]:

        print(
            f"\nQuestion: "
            f"{result['question']}"
        )

        print(
            f"Precision@5: "
            f"{result['precision_at_k']:.3f}"
        )

        print(
            f"Recall@5: "
            f"{result['recall_at_k']:.3f}"
        )

        print(
            f"Reciprocal Rank: "
            f"{result['reciprocal_rank']:.3f}"
        )


if __name__ == "__main__":
    main()