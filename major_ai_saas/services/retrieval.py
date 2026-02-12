import numpy as np
from services.vector_store import embedding_model

def retrive_chunks(question, chunks, index, k=3):
    q_embedding = embedding_model.encode([question])
    distance, indices = index.search(np.array(q_embedding), k)

    return [chunks[i] for i in indices[0]]