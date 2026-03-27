from services.embedding_services import get_embedding
from services.vector_store import search_similar

def check_anomaly(prompt: str):
    emb = get_embedding(prompt)
    distance, idx = search_similar(emb)

    if distance is None:
        return {"is_anomaly": True, "score": 0}

    score = 1 / (1 + distance)

    return {
        "score": score,
        "is_anomaly": score < 0.4
    }