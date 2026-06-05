import re
from collections import defaultdict
import math

def build_index(pages):
    index = defaultdict(dict)
    doc_count = defaultdict(int)
    total_docs = len(pages)

    for url, title, content in pages:
        text = (title + " " + content).lower()
        words = re.findall(r"\b[a-z]{3,}\b", text)

        if len(words) == 0:
            continue

        freq = defaultdict(int)
        for w in words:
            freq[w] += 1

        for word, count in freq.items():
            tf = count / len(words)
            index[word][url] = tf
            doc_count[word] += 1

    for word in index:
        idf = math.log((total_docs + 1) / (doc_count[word] + 1))
        for url in index[word]:
            index[word][url] *= idf

    return index


def search(query, index):
    words = query.lower().split()
    scores = defaultdict(float)

    for word in words:
        if word in index:
            for url, score in index[word].items():
                scores[url] += score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [url for url, _ in ranked]