from src.plantguard.m3.document_loader import PlantGuardDocumentLoader
from src.plantguard.m4.bm25_search import PlantGuardBM25


def main():
    loader = PlantGuardDocumentLoader("data/plantguard/corpus")

    documents = loader.load_pdf_documents()
    print(f"Loaded {len(documents)} PDF documents")

    all_chunks = []
    for document in documents:
        chunks = loader.chunk_document(document)
        all_chunks.extend(chunks)
        print(
            f"  {document['source']}: "
            f"{len(document['text'])} chars -> {len(chunks)} chunks"
        )

    print(f"\nTotal PDF chunks: {len(all_chunks)}")

    bm25 = PlantGuardBM25(all_chunks)
    query = "What are the vibration alarm thresholds?"
    results = bm25.search(query=query, limit=3)

    print(f"\nBM25 over PDF chunks — query: {query}")
    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]
        print(f"\nResult {rank}  score={result['score']:.3f}")
        print(f"  source : {chunk['metadata']['source']}")
        print(f"  section: {chunk['metadata']['section']}")
        print(f"  text   : {chunk['text'][:200]}")


if __name__ == "__main__":
    main()
