from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_embeddings(pages):
    texts = []
    urls = []

    for url, title, content in pages:
        combined = (title + " " + content)[:2000]
        texts.append(combined)
        urls.append(url)

    if len(texts) == 0:
        return np.array([]), []

    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings, urls


def search_semantic(query, embeddings, urls, top_k=10):
    if len(embeddings) == 0:
        return []

    query_vec = model.encode([query])[0]

    scores = np.dot(embeddings, query_vec)
    ranked = np.argsort(scores)[::-1]

    return [urls[i] for i in ranked[:top_k]]