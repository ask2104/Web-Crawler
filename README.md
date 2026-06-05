# Web Crawler Search Engine

A simple search engine built in Python. The project crawls web pages, stores them in SQLite, creates a TF-IDF index for keyword search, and generates embeddings for semantic search. A Flask web interface provides search and autocomplete functionality.

## Features

* Web crawling with configurable depth and page limits
* SQLite-based page storage
* TF-IDF keyword search
* Semantic search using Sentence Transformers
* Autocomplete using a Trie
* Simple web interface built with Flask

## Requirements

* Python 3.9+
* pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Build the index

This crawls pages, stores them in the database, and creates the search indexes.

```bash
python create_index.py
```

By default, the crawler starts from:

```text
https://arxiv.org/list/cs/recent
```

You can change the seed URL in `create_index.py`.

### 2. Start the application

```bash
python app.py
```

Open your browser and go to:

```text
http://localhost:5000
```

## Search Modes

### Normal Search

Uses a TF-IDF based inverted index to rank documents matching the query terms.

### Semantic Search

Uses sentence embeddings to find documents that are semantically related to the query, even when exact keywords are not present.

## Files

* `app.py` – Flask application and search interface
* `crawler.py` – Web crawler
* `database.py` – SQLite database operations
* `indexer.py` – TF-IDF index generation
* `search.py` – Keyword search
* `semantic.py` – Embedding generation and semantic search
* `autocomplete.py` – Trie construction and suggestions
* `create_index.py` – Crawling and index creation pipeline

## Notes

The following files are generated locally and are not tracked by Git:

* `storage/`
* `search.db`

## License

MIT License
