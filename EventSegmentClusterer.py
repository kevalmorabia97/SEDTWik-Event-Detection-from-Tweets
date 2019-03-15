import networkx as nx


def get_events(bursty_segment_weights, segment_newsworthiness, seg_sim, n_neighbors=4, max_cluster_segments=20, threshold=4):
    """
    return event clusters from bursty_segment_scores(dict from seg_name to bursty_wt)
    using a variation of Jarvis Patrick Clustering Algo
    """    
    bursty_segments = list(bursty_segment_weights.keys())
    n = len(bursty_segments)
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    k_neighbors = {}
    for i in range(n):
        k_neighbors[i] = get_k_neighbors(n_neighbors, i, seg_sim)
    
    # add edge between a,b if both in k_neighbors of other
    for i in range(n):
        for j in range(i+1,n):
            if i in k_neighbors[j] and j in k_neighbors[i]:
                G.add_edge(i,j)
    
    clusters = [] # each cluster is a tuple of list(segments) and event_newsworthiness
    max_event_worthiness = 0
    for sg in nx.connected_component_subgraphs(G):
        n = len(sg.nodes)
        if(n < 1.5*n_neighbors): continue # remove clusters with size < 1.5*n_neighbors
        
        cluster_segments = [bursty_segments[i] for i in sg.nodes]
        
        event_newsworthiness = sum([segment_newsworthiness[s] for s in cluster_segments])/n
        event_newsworthiness *= sum([seg_sim[i][j] for i,j in sg.edges])/n
        
        max_event_worthiness = max(max_event_worthiness,event_newsworthiness)
        
        # keep top k=max_cluster_segments segments as per bursty_score
        cluster_segments = sorted(cluster_segments, key=lambda x:bursty_segment_weights[x], reverse=True)[:max_cluster_segments]
        
        clusters.append((cluster_segments, event_newsworthiness))
        
    clusters = sorted(clusters, key = lambda x:x[1], reverse=True)
    threshold_worthiness = max_event_worthiness/threshold
    
    return [c for c in clusters if c[1]>threshold_worthiness] 


def get_k_neighbors(k, seg, seg_sim):
    """
    return set of k nearest neighbors of 'seg'
    """
    neighbor_list = []
    sim_list = [] # sim_list[i] = similarity of seg with neighbor[i]
    for i in seg_sim:
        if i == seg: continue
        neighbor_list.append(i)
        sim_list.append(seg_sim[seg][i])
    return set([x for _,x in sorted(zip(sim_list,neighbor_list), reverse=True)][:k])


def get_seg_similarity(bursty_segment_weights, time_window):
    """
    return a dict of similarity between segments where keys are index of segment in bursty_segments
    """
    print('Computing similarity between bursty segments')
    seg_sim = {}
    bursty_segments = list(bursty_segment_weights.keys())
    n = len(bursty_segments)
    
    for i in range(n):
        seg_sim[i] = {}
        seg_sim[i][i] = 1
    
    for i in range(n):
        seg1_name = bursty_segments[i]
        print(i+1, seg1_name, str(bursty_segment_weights[seg1_name])[:7])
        for j in range(i+1, n):
            seg2_name = bursty_segments[j]
            sim = time_window.get_segment_similarity(seg1_name, seg2_name)
            seg_sim[i][j] = sim
            seg_sim[j][i] = sim
            
    return seg_sim