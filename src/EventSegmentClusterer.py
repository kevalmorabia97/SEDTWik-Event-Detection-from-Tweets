import networkx as nx

def get_seg_similarity(bursty_segment_weights, time_window):
    """
    return a dict of similarity between segments where keys are index of segment in bursty_segments
    """
    print('Computing similarity between bursty segments')
    seg_sim = {}
    bursty_segments = list(bursty_segment_weights.keys())
    n = len(bursty_segments)
    for i in range(n):
        seg1_name = bursty_segments[i]
        print(i+1,seg1_name,str(bursty_segment_weights[seg1_name])[:7])
        for j in range(i,n):
            seg2_name = bursty_segments[j]
            if i not in seg_sim: seg_sim[i] = {}
            if j not in seg_sim: seg_sim[j] = {}
            sim = time_window.get_segment_similarity(seg1_name, seg2_name)
            seg_sim[i][j] = sim
            seg_sim[j][i] = sim
            
    return seg_sim

def get_events(bursty_segment_weights, seg_sim, n_neighbors=3, min_cluster_segments=5):
    """
    return event clusters from bursty_segment_scores(dict from seg_name to bursty_wt) in time_window using a variation of Jarvis Patrick Clustering Algo
    """
    bursty_segments = list(bursty_segment_weights.keys())
    n = len(bursty_segments)
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    k_neighbors = {}
    for i in range(n):
        k_neighbors[i] = get_k_neighbors(n_neighbors, i, seg_sim)
        
    for i in range(n):
        for j in range(i+1,n):
            if i in k_neighbors[j] and j in k_neighbors[i]:
                G.add_edge(i,j)
    
    clusters = []
    for comp in nx.connected_components(G):
        if(len(comp) >= min_cluster_segments):
            avg_cluster_bursty_score = sum([bursty_segment_weights[bursty_segments[i]] for i in comp]) / len(comp)
            clusters.append( ([bursty_segments[i] for i in comp], avg_cluster_bursty_score) )

    return get_most_newsworthy_cluters(clusters)
            
def get_k_neighbors(k, seg, seg_sim):
    """
    return set of k nearest neighbors of 'seg'
    """
    neighbor_list = []
    sim_list = [] # sim_list[i] = similarity of seg with neighbors[i]
    for i in seg_sim:
        if i == seg: continue
        neighbor_list.append(i)
        sim_list.append(seg_sim[seg][i])
    return set([x for _,x in sorted(zip(sim_list,neighbor_list), reverse=True)][:k])

def get_most_newsworthy_cluters(clusters):
    """
    return those clusters that pass the threshold of news worthiness
    """
    return sorted(clusters, key = lambda x : x[1], reverse=True)
