import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from database import insert_page

def fetch_page(url, start_domain):
    try:
        res = requests.get(url, timeout=3)
        if res.status_code != 200:
            return None, []
    except:
        return None, []

    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.title.string.strip() if soup.title else url
    content = soup.get_text(" ", strip=True)[:1500]

    links = []
    for tag in soup.find_all("a", href=True):
        abs_url = urljoin(url, tag["href"])

        if urlparse(abs_url).netloc != start_domain:
            continue

        if any(x in abs_url for x in ["login", "signup", "search", "#", "javascript"]):
            continue

        links.append(abs_url)

    return (url, title, content), links


def bfs_crawler(start_url, max_depth=1, max_pages=50, workers=10):
    visited = set()
    queue = deque([(start_url, 0)])
    start_domain = urlparse(start_url).netloc

    with ThreadPoolExecutor(max_workers=workers) as executor:
        while queue and len(visited) < max_pages:
            batch = []

            while queue and len(batch) < workers:
                url, depth = queue.popleft()
                if url not in visited and depth <= max_depth:
                    visited.add(url)
                    batch.append((url, depth))

            futures = []
            for url, depth in batch:
                futures.append((executor.submit(fetch_page, url, start_domain), depth))

            for future, depth in futures:
                result, links = future.result()

                if result:
                    url, title, content = result
                    insert_page(url, title, content)
                    print("Saved:", url)

                for link in links:
                    if link not in visited:
                        queue.append((link, depth + 1))