import os
import faiss
import numpy as np
import json
from .embedding_services import get_embedding

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

dimension = 384
index = faiss.IndexFlatL2(dimension)

stored_prompts = []

def load_data():
    with open(os.path.join(_DATA_DIR, "jailbreak_attacks.json")) as f:
        data = json.load(f)

    for p in data:
        emb = get_embedding(p)
        add_prompt(emb, p)


def add_prompt(embedding, text):
    index.add(np.array([embedding]).astype('float32'))
    stored_prompts.append(text)

def search_similar(embedding, k=1):
    if index.ntotal == 0:
        return None, None

    distances, indices = index.search(
        np.array([embedding]).astype('float32'), k
    )

    return distances[0][0], indices[0][0]

load_data()