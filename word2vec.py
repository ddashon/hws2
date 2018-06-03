import sys
import gensim, logging
import matplotlib.pyplot as plt
import networkx as nx


m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'


def begin(m):
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)
    model.init_sims(replace=True)
    return model

words = ['мокасины_NOUN', 'сабо_NOUN', 'ботинки_NOUN', 'кроссовки_NOUN', 'кеды_NOUN', 'конверсы_NOUN', 'тапочки_NOUN', 'тапки_NOUN','обувь_NOUN', 'каблуки_NOUN', 'туфли_NOUN', 'найки_NOUN','босоножки_NOUN', 'балетки_NOUN', 'сапоги_NOUN']

def graph(model, words):
    a = nx.Graph()
    a.add_nodes_from(words)
    for i in words:
        for e in words:
            if i !=e:
                if model.similarity(i, e) > 0.5:
                    a.add_edge(i,e )
    return a

def pic(a):
    pos = nx.spring_layout(a)
    nx.draw_networkx_nodes(a, pos, node_color='blue', node_size=20)
    nx.draw_networkx_labels(a, pos, font_size=12, font_family='Times New Roman')
    nx.draw_networkx_edges(a, pos, edge_color='red')
    plt.axis('off')
    plt.show()
    return

def extra(a):
    cent_graph = nx.degree_centrality(a)
    i = 0
    cent = 0
    print('center:')
    for nodeid in sorted(cent_graph, key=cent_graph.get, reverse=True):
        if cent_graph[nodeid] < cent:
            break
        else:
            cent = cent_graph[nodeid]
            print(nodeid, round(cent_graph[nodeid], 3))
    print ('radius:')
    print(nx.radius(a))
    print(nx.average_clustering(a))
    return


def final(m, words):
    a = graph(begin(m), words)
    pic(a)
    extra(a)
    return

