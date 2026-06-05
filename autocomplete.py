def build_trie(words):
    trie = {}
    for word in words:
        node = trie
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True
    return trie

def suggest(trie, prefix):
    node = trie
    for c in prefix:
        if c not in node:
            return []
        node = node[c]

    res = []

    def dfs(n, path):
        if "$" in n:
            res.append(path)
        for c in n:
            if c != "$":
                dfs(n[c], path + c)

    dfs(node, prefix)
    return res[:5]