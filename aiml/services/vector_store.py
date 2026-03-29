import os
import faiss
import numpy as np
import json
from .embedding_services import get_embedding

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_INDEX_FILE = os.path.join(_DATA_DIR, "attacks.index")
_PROMPTS_FILE = os.path.join(_DATA_DIR, "attacks_metadata.json")

dimension = 384
index = faiss.IndexFlatL2(dimension)

stored_prompts = []

def load_data():
    """Load initial jailbreak attacks from JSON file."""
    with open(os.path.join(_DATA_DIR, "jailbreak_attacks.json")) as f:
        data = json.load(f)
    for p in data:
        emb = get_embedding(p)
        add_prompt(emb, p)


def save_index():
    """Persist FAISS index and metadata to disk."""
    faiss.write_index(index, _INDEX_FILE)
    with open(_PROMPTS_FILE, 'w') as f:
        json.dump(stored_prompts, f)


def load_index():
    """Load FAISS index from disk if it exists, otherwise initialize from data."""
    global index, stored_prompts
    if os.path.exists(_INDEX_FILE) and os.path.exists(_PROMPTS_FILE):
        index = faiss.read_index(_INDEX_FILE)
        with open(_PROMPTS_FILE, 'r') as f:
            stored_prompts = json.load(f)
    else:
        load_data()


def add_prompt(embedding, text):
    index.add(np.array([embedding]).astype('float32'))
    stored_prompts.append(text)

def add_new_attack(text):
    """Dynamically inject newly discovered attacks into FAISS memory and persist."""
    emb = get_embedding(text)
    add_prompt(emb, text)
    save_index()  # Persist after each new attack

def search_similar(embedding, k=1):
    if index.ntotal == 0:
        return None, None

    distances, indices = index.search(
        np.array([embedding]).astype('float32'), k
    )

    return distances[0][0], indices[0][0]

load_index()