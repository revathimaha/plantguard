import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()


class PlantGuardVectorStore:

    def __init__(
        self,
        collection_name: str = "plantguard_manuals",
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
            timeout=60,
        )

    def create_collection(self, vector_dimension: int):
        collections = self.client.get_collections()

        existing_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in existing_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_dimension,
                    distance=Distance.COSINE,
                ),
            )

            print(
                f"Created collection: {self.collection_name}"
            )
        else:
            print(
                f"Collection already exists: "
                f"{self.collection_name}"
            )

    def upload_chunks(
        self,
        chunks: list[dict],
        vectors: list[list[float]],
    ):
        existing = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        if existing.count == len(chunks):
            print(
                f"Qdrant already contains {existing.count} points. "
                "Skipping upload."
            )
            return

        print(
            f"Qdrant contains {existing.count} points. "
            f"Uploading {len(chunks)} points."
        )

        batch_size = 5
        batch_size = 5

        for start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[start:start + batch_size]
            batch_vectors = vectors[start:start + batch_size]

            points = []

            for index, (chunk, vector) in enumerate(
                zip(batch_chunks, batch_vectors),
                start=start,
            ):
                points.append(
                    PointStruct(
                        id=index,
                        vector=vector,
                        payload={
                            "text": chunk["text"],
                            "source": chunk["metadata"]["source"],
                            "section": chunk["metadata"]["section"],
                        },
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            print(
                f"Uploaded points {start} - "
                f"{start + len(points) - 1}"
            )

        print(f"Uploaded {len(chunks)} points to Qdrant")


    def get_collection_count(self) -> int:
        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        return results.points