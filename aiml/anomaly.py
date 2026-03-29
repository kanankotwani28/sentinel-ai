from .services.embedding_services import get_embedding
from .services.vector_store import search_similar


def check_anomaly(prompt: str):
    emb = get_embedding(prompt)
    distance, idx = search_similar(emb)

    if distance is None:
        # No data in index — can't assess, assume not a threat
        return {"is_threat": False, "attack_similarity": 0.0, "nearest_distance": None}

    # Higher similarity = closer to a KNOWN ATTACK in the FAISS index
    attack_similarity = 1 / (1 + distance)

    return {
        "attack_similarity": round(attack_similarity, 4),
        "is_threat": attack_similarity > 0.6,   # close to a known attack pattern
        "nearest_distance": round(float(distance), 4),
    }