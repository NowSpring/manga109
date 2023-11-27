import MeCab
import ipadic
import itertools
import collections
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def set_mecab():
    
    CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
    CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'
    tokenizer = MeCab.Tagger(ipadic.MECAB_ARGS + CHASEN_ARGS)
    
    return tokenizer

def get_Keywords(tokenizer, xText):
    
    node = tokenizer.parseToNode(xText)
    
    keywords = []
    
    while node:
    
        if node.feature.split(",")[0] == u"名詞" and (node.feature.split(",")[1] == u"一般" or node.feature.split(",")[1] == u"サ変接続"):
    
            if node.surface[0] != "ー":
    
                keywords.append(node.surface)
    
        elif node.feature.split(",")[0] == u"形容詞":

            keywords.append(node.feature.split(",")[6])
    
        elif node.feature.split(",")[0] == u"動詞" and node.feature.split(",")[1] == u"自立":

            if node.feature.split(",")[6] != "する":

                keywords.append(node.feature.split(",")[6])

        node = node.next
    
    return keywords

def get_conbination(xKeywords):
    
    combination_sentences = [list(itertools.combinations(words, 2)) for words in xKeywords]
    combination_sentences = [[tuple(sorted(combi)) for combi in combinations] for combinations in combination_sentences]
    
    tmp = []
    
    for combinations in combination_sentences:
    
        tmp.extend(combinations)
    
    combination_sentences = tmp
    combination_sentences = [tup for tup in combination_sentences if tup[0] != tup[1]]

    return combination_sentences

def make_jaccard_coef_data(combination_sentences):

    combi_count = collections.Counter(combination_sentences)

    word_associates = []
    
    for key, value in combi_count.items():
    
        word_associates.append([key[0], key[1], value])

    word_associates = pd.DataFrame(word_associates, columns=['word1', 'word2', 'intersection_count'])

    words = []
    
    for combi in combination_sentences:
    
        words.extend(combi)

    word_count = collections.Counter(words)
    word_count = [[key, value] for key, value in word_count.items()]
    word_count = pd.DataFrame(word_count, columns=['word', 'count'])

    word_associates = pd.merge(
        word_associates,
        word_count.rename(columns={'word': 'word1'}),
        on='word1', how='left'
    ).rename(columns={'count': 'count1'}).merge(
        word_count.rename(columns={'word': 'word2'}),
        on='word2', how='left'
    ).rename(columns={'count': 'count2'}).assign(
        union_count=lambda x: x.count1 + x.count2 - x.intersection_count
    ).assign(jaccard_coef=lambda x: x.intersection_count / x.union_count).sort_values(
        ['jaccard_coef', 'intersection_count'], ascending=[False, False]
    )
    
    return word_associates

def plot_network(
    data, edge_threshold=0., fig_size=(15, 15),
    fontfamily='Hiragino Maru Gothic Pro', fontsize=14,
    coefficient_of_restitution=0.15,
    image_file_path=None
):

    nodes = list(set(data['node1'].tolist() + data['node2'].tolist()))
    
    plt.figure(figsize=fig_size)
    
    G = nx.Graph()
    # 頂点の追加
    G.add_nodes_from(nodes)


    # 辺の追加
    # edge_thresholdで枝の重みの下限を定めている
    for i in range(len(data)):
        
        row_data = data.iloc[i]
        
        if row_data['weight'] >= edge_threshold:
        
            G.add_edge(row_data['node1'], row_data['node2'], weight=row_data['weight'])

    # 孤立したnodeを削除
    isolated = [n for n in G.nodes if len([i for i in nx.all_neighbors(G, n)]) == 0]
    
    for n in isolated:
    
        G.remove_node(n)

    # k = node間反発係数
    pos = nx.spring_layout(G, k=coefficient_of_restitution)
    pr = nx.pagerank(G)
    # nodeの大きさ
    nx.draw_networkx_nodes(
        G, pos, node_color=list(pr.values()),
        cmap=plt.cm.Reds,
        alpha=0.7,
        node_size=[60000*v for v in pr.values()]
    )
    # 日本語ラベル
    nx.draw_networkx_labels(G, pos, font_size=fontsize, font_family=fontfamily, font_weight="bold")
    # エッジの太さ調節
    edge_width = [d["weight"] * 50 for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="darkgrey", width=edge_width)

    plt.axis('off')
    plt.tight_layout()
    
    if image_file_path:
        
        plt.savefig(image_file_path, dpi=300)