import time
import pickle
import os
from crawler import bfs_crawler
from database import get_all_pages
from indexer import build_index
from autocomplete import build_trie
from semantic import build_embeddings

os.makedirs("storage", exist_ok=True)

print("Step 1: Crawling...")
bfs_crawler("https://arxiv.org/list/cs/recent", max_depth=1, max_pages=30)

print("Step 2: Loading pages from DB...")
pages = get_all_pages()
print("Pages:", len(pages))

if len(pages) == 0:
    print("No pages found. Exiting.")
    exit()

print("Step 3: Building index...")
start = time.time()

index = build_index(pages)
trie = build_trie(index.keys())
embeddings, urls = build_embeddings(pages)

end = time.time()

print("Docs:", len(pages))
print("Time:", round(end - start, 2))

with open("storage/index.pkl", "wb") as f:
    pickle.dump(index, f)

with open("storage/trie.pkl", "wb") as f:
    pickle.dump(trie, f)

with open("storage/semantic.pkl", "wb") as f:
    pickle.dump((embeddings, urls), f)

print("Saved all files.")