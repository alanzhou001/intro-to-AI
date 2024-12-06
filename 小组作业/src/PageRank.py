import networkx as nx


# 构建字对共现图
def build_co_occurrence_graph(poem_database):
    G = nx.DiGraph()
    for poem in poem_database:
        cleaned_poem = "".join(poem.split())
        for i in range(len(cleaned_poem) - 1):
            for j in range(i + 1, len(cleaned_poem)):
                G.add_edge(cleaned_poem[i], cleaned_poem[j], weight=G.get_edge_data(cleaned_poem[i], cleaned_poem[j], {}).get('weight', 0) + 1)
                G.add_edge(cleaned_poem[j], cleaned_poem[i], weight=G.get_edge_data(cleaned_poem[j], cleaned_poem[i], {}).get('weight', 0) + 1)

    pagerank_scores = nx.pagerank(G, weight='weight')
    return pagerank_scores
