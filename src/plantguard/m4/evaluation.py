from typing import Any, Callable


class PlantGuardEvaluator:
    """
    Evaluates the PlantGuard M4 retrieval pipeline.

    The golden set distinguishes between:

    1. retrieve
       Questions for which supporting evidence is expected.

    2. abstain
       Questions for which the knowledge base is expected
       not to contain sufficient evidence.
    """

    def __init__(
        self,
        golden_questions: list[dict[str, Any]],
    ):
        self.golden_questions = golden_questions

    # =========================================================
    # RESULT EXTRACTION
    # =========================================================

    @staticmethod
    def _result_metadata(
        result: dict[str, Any],
    ) -> tuple[str, str]:

        """
        Extract source and section from a reranked result.
        """

        hybrid_item = result["result"]
        underlying = hybrid_item["result"]

        # BM25 / hybrid dictionary result
        if isinstance(underlying, dict):

            chunk = underlying["chunk"]

            return (
                chunk["metadata"]["source"],
                chunk["metadata"]["section"],
            )

        # Qdrant result
        return (
            underlying.payload["source"],
            underlying.payload["section"],
        )

    # =========================================================
    # RELEVANCE
    # =========================================================

    @staticmethod
    def _is_relevant(
        result: dict[str, Any],
        expected_sources: list[dict[str, str]],
    ) -> bool:

        source, section = (
            PlantGuardEvaluator._result_metadata(result)
        )

        return any(
            source == expected["source"]
            and section == expected["section"]
            for expected in expected_sources
        )

    # =========================================================
    # RETRIEVAL METRICS
    # =========================================================

    def evaluate_retrieval_question(
        self,
        question: str,
        expected_sources: list[dict[str, str]],
        retrieved_results: list[dict[str, Any]],
        k: int = 5,
    ) -> dict[str, Any]:

        top_k = retrieved_results[:k]

        relevant_flags = [
            self._is_relevant(
                result,
                expected_sources,
            )
            for result in top_k
        ]

        relevant_count = sum(relevant_flags)

        # -----------------------------------------------------
        # Precision@K
        # -----------------------------------------------------

        precision_at_k = (
            relevant_count / len(top_k)
            if top_k
            else 0.0
        )

        # -----------------------------------------------------
        # Recall@K
        #
        # For the current golden set, each question has one
        # expected source/section.
        # -----------------------------------------------------

        recall_at_k = (
            1.0
            if any(relevant_flags)
            else 0.0
        )

        # -----------------------------------------------------
        # Reciprocal Rank
        # -----------------------------------------------------

        reciprocal_rank = 0.0

        for rank, is_relevant in enumerate(
            relevant_flags,
            start=1,
        ):

            if is_relevant:

                reciprocal_rank = 1.0 / rank

                break

        return {
            "question": question,
            "precision_at_k": precision_at_k,
            "recall_at_k": recall_at_k,
            "reciprocal_rank": reciprocal_rank,
            "relevant_results": relevant_count,
            "retrieved_results": len(top_k),
        }

    # =========================================================
    # ABSTENTION METRIC
    # =========================================================

    def evaluate_abstention_question(
        self,
        question: str,
        retrieved_results: list[dict[str, Any]],
    ) -> dict[str, Any]:

        """
        Evaluate whether a question has supporting evidence.

        This is a retrieval-level abstention check.

        It does NOT evaluate the LLM's final wording.
        """

        has_relevant_evidence = len(retrieved_results) > 0

        return {
            "question": question,
            "expected_behavior": "abstain",
            "retrieved_results": len(retrieved_results),
            "has_retrieved_evidence": has_relevant_evidence,
        }

    # =========================================================
    # COMPLETE EVALUATION
    # =========================================================

    def evaluate(
        self,
        retrieval_function: Callable[
            [str],
            list[dict[str, Any]],
        ],
        k: int = 5,
    ) -> dict[str, Any]:

        retrieval_results = []
        abstention_results = []

        for item in self.golden_questions:

            question = item["question"]

            expected_sources = item.get(
                "expected_sources",
                [],
            )

            expected_behavior = item.get(
                "expected_behavior",
                "retrieve",
            )

            retrieved_results = retrieval_function(
                question
            )

            # -------------------------------------------------
            # Retrieval evaluation
            # -------------------------------------------------

            if expected_behavior == "retrieve":

                result = self.evaluate_retrieval_question(
                    question=question,
                    expected_sources=expected_sources,
                    retrieved_results=retrieved_results,
                    k=k,
                )

                retrieval_results.append(result)

            # -------------------------------------------------
            # Abstention evaluation
            # -------------------------------------------------

            elif expected_behavior == "abstain":

                result = self.evaluate_abstention_question(
                    question=question,
                    retrieved_results=retrieved_results,
                )

                abstention_results.append(result)

        # =====================================================
        # AGGREGATE RETRIEVAL METRICS
        # =====================================================

        if retrieval_results:

            precision_at_k = sum(
                result["precision_at_k"]
                for result in retrieval_results
            ) / len(retrieval_results)

            recall_at_k = sum(
                result["recall_at_k"]
                for result in retrieval_results
            ) / len(retrieval_results)

            mrr = sum(
                result["reciprocal_rank"]
                for result in retrieval_results
            ) / len(retrieval_results)

        else:

            precision_at_k = 0.0
            recall_at_k = 0.0
            mrr = 0.0

        # =====================================================
        # ABSTENTION METRICS
        # =====================================================

        # Important:
        #
        # Retrieval returning chunks does NOT mean the system
        # should answer. RAG must still determine whether those
        # chunks actually support the question.
        #
        # Therefore this metric is informational at the
        # retrieval layer. Final abstention correctness is
        # evaluated separately by the grounded RAG tests.

        abstention_count = len(
            abstention_results
        )

        return {
            "retrieval": {
                "questions": retrieval_results,
                "question_count": len(retrieval_results),
                "precision_at_k": precision_at_k,
                "recall_at_k": recall_at_k,
                "mrr": mrr,
            },
            "abstention": {
                "questions": abstention_results,
                "question_count": abstention_count,
            },
        }