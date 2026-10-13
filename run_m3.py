from src.plantguard.m3.maintenance_history import MaintenanceHistory
from src.plantguard.m3.document_loader import PlantGuardDocumentLoader
from src.plantguard.m3.embeddings import PlantGuardEmbedder
from src.plantguard.m3.vector_store import PlantGuardVectorStore


# def main():
#     history = MaintenanceHistory(
#         work_orders_path="data/plantguard/mock_api/work_orders.json",
#         work_order_details_path="data/plantguard/mock_api/work_order_details.json",
#     )

#     records = history.get_asset_history("VPW-CNC-MILL-03")

#     print(f"Found {len(records)} maintenance records")

#     for record in records[:5]:
#         print(record)

#     # Document loading
#     loader = PlantGuardDocumentLoader(
#         "data/plantguard/corpus"
#     )

#     documents = loader.load_markdown_documents()

#     print(f"\nMarkdown documents loaded: {len(documents)}")


#     for document in documents:
#         chunks = loader.chunk_document(document)

#         max_size = max(len(chunk["text"]) for chunk in chunks)

#         print(
#             f"{document['source']}: "
#             f"max chunk size = {max_size} characters"
#         )

#         embedder = PlantGuardEmbedder()

#         sample_text = chunks[0]["text"]

#         vector = embedder.embed_texts([sample_text])[0]

#         print("\n--- EMBEDDING TEST ---")
#         print("Vector dimension:", len(vector))
#         print("First 5 values:", vector[:5])


# if __name__ == "__main__":
#     main()



from src.plantguard.m3.embeddings import PlantGuardEmbedder


def main():
    # Existing M3 history code
    history = MaintenanceHistory(
        work_orders_path="data/plantguard/mock_api/work_orders.json",
        work_order_details_path="data/plantguard/mock_api/work_order_details.json",
    )

    records = history.get_asset_history("VPW-CNC-MILL-03")

    print(f"Found {len(records)} maintenance records")

    loader = PlantGuardDocumentLoader(
        "data/plantguard/corpus"
    )

    documents = loader.load_markdown_documents()

    print(f"Loaded {len(documents)} documents")

    # Collect chunks from all documents
    all_chunks = []

    for document in documents:
        chunks = loader.chunk_document(document)

        for chunk in chunks:
            all_chunks.append(chunk)

    print(f"Total chunks: {len(all_chunks)}")

    # -----------------------------
    # Embed all chunks
    # -----------------------------
    embedder = PlantGuardEmbedder()

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    vectors = embedder.embed_texts(texts)

    print("\n--- EMBEDDING COMPLETE ---")
    print("Chunks:", len(texts))
    print("Vectors:", len(vectors))
    print("Vector dimension:", len(vectors[0]))

    vector_store = PlantGuardVectorStore()

    vector_store.create_collection(
        vector_dimension=len(vectors[0])
    )

    vector_store.upload_chunks(
        chunks=all_chunks,
        vectors=vectors,
    )

    count = vector_store.get_collection_count()

    print("\n--- QDRANT VERIFICATION ---")
    print("Expected points:", len(all_chunks))
    print("Actual points:", count)


    query = "What are the P1 vibration alarm thresholds?"

    query_vector = embedder.embed_query(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=5,
    )

    print("\n--- SEMANTIC SEARCH ---")
    print("Query:", query)

    for rank, result in enumerate(results, start=1):
        print(f"\nResult {rank}")
        print("Score:", result.score)
        print("Source:", result.payload["source"])
        print("Section:", result.payload["section"])
        print("Text:")
        print(result.payload["text"][:500])

if __name__ == "__main__":
    main()