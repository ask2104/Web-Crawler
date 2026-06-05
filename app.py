from flask import Flask, request, render_template_string
import pickle
from search import search
from autocomplete import suggest
from semantic import search_semantic
from database import get_pages

with open("storage/index.pkl", "rb") as f:
    index = pickle.load(f)

with open("storage/trie.pkl", "rb") as f:
    trie = pickle.load(f)

with open("storage/semantic.pkl", "rb") as f:
    embeddings, urls_list = pickle.load(f)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Brutal Search</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    font-family: Arial, sans-serif;
    background: #fdf6e3;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
}

.title {
    font-size: 3rem;
    font-weight: 900;
    background: #ffcc00;
    display: inline-block;
    padding: 10px 20px;
    border: 4px solid black;
    box-shadow: 6px 6px 0 black;
}

.search-box {
    margin-top: 30px;
    display: flex;
    border: 4px solid black;
    box-shadow: 6px 6px 0 black;
}

input {
    flex: 1;
    padding: 15px;
    font-size: 1.1rem;
    border: none;
    outline: none;
}

button {
    background: #ff4d4d;
    border: none;
    padding: 15px 25px;
    font-weight: bold;
    cursor: pointer;
    border-left: 4px solid black;
}

button:hover {
    background: #ff1a1a;
}

.suggestions {
    border: 4px solid black;
    border-top: none;
    background: white;
    box-shadow: 6px 6px 0 black;
}

.suggestions div {
    padding: 10px;
    cursor: pointer;
}

.suggestions div:hover {
    background: #eee;
}

.results {
    margin-top: 40px;
}

.card {
    background: white;
    border: 4px solid black;
    margin-bottom: 20px;
    padding: 20px;
    box-shadow: 6px 6px 0 black;
    transition: 0.2s;
}

.card:hover {
    transform: translate(-3px, -3px);
    box-shadow: 9px 9px 0 black;
}

.card a {
    font-size: 1.3rem;
    font-weight: bold;
    text-decoration: none;
    color: black;
}

.card p {
    margin-top: 10px;
    color: #333;
}

.mode-toggle {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.mode-toggle button {
    background: #00cc99;
    border: 4px solid black;
    box-shadow: 4px 4px 0 black;
}
</style>
</head>

<body>

<div class="container">
    <div class="title">BRUTAL SEARCH</div>

    <form method="GET" action="/">
        <div class="search-box">
            <input type="text" name="q" id="searchInput" value="{{q}}" placeholder="Search anything..." autocomplete="off">
            <button type="submit">Search</button>
        </div>
        <div id="suggestions" class="suggestions"></div>
    </form>

    <div class="mode-toggle">
        <button onclick="goNormal()">Normal</button>
        <button onclick="goSemantic()">Semantic</button>
    </div>

    <div class="results">
        {% for r in results %}
        <div class="card">
            <a href="{{r.url}}" target="_blank">{{r.title}}</a>
            <p>{{r.content[:200]}}</p>
        </div>
        {% endfor %}
    </div>
</div>

<script>
const input = document.getElementById("searchInput");
const box = document.getElementById("suggestions");

input.addEventListener("input", async () => {
    const q = input.value;
    if (!q) {
        box.innerHTML = "";
        return;
    }

    const res = await fetch(`/suggest?q=${q}`);
    const data = await res.json();

    box.innerHTML = "";
    data.suggestions.forEach(s => {
        const d = document.createElement("div");
        d.innerText = s;
        d.onclick = () => {
            input.value = s;
            box.innerHTML = "";
        };
        box.appendChild(d);
    });
});

function goSemantic() {
    const q = input.value;
    if (q) window.location.href = `/semantic?q=${q}`;
}

function goNormal() {
    const q = input.value;
    if (q) window.location.href = `/?q=${q}`;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    q = request.args.get("q", "")
    results = []
    if q:
        urls = search(q, index)
        results = get_pages(urls)
    return render_template_string(HTML, q=q, results=results)

@app.route("/semantic")
def semantic_route():
    q = request.args.get("q", "")
    results = []
    if q:
        urls = search_semantic(q, embeddings, urls_list)
        results = get_pages(urls[:10])
    return render_template_string(HTML, q=q, results=results)

@app.route("/suggest")
def suggest_api():
    q = request.args.get("q", "")
    return {"suggestions": suggest(trie, q)}

app.run(debug=True)