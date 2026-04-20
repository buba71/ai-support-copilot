from ai_service.infrastructure.vector_db import VectorDB

db = VectorDB()

results = db.search("refund defective product", k=3)

for r in results:
    print("SOURCE:", r["metadata"]["source"])
    print("CONTENT:", r["content"][:100])
    print("DISTANCE:", r["distance"])
    print("---")