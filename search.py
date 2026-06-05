from collections import defaultdict

def search(query, index):
    words = query.lower().split()
    scores = defaultdict(float)

    for w in words:
        if w in index:
            for url, s in index[w].items():
                scores[url] += s

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [u for u, _ in ranked]