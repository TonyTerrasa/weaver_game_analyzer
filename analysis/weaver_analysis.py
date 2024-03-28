import networkx as nx
import pickle
from typing import List, Tuple


def get_paths(G: nx.Graph, s1: str, s2: str):
    s1 = s1.lower()
    s2 = s2.lower()
    return list(nx.all_shortest_paths(G, s1, s2))


def paths_with_correctness(G: nx.Graph, s1: str, s2: str):
    """
    G (nx.Graph) graph to use to find paths
    s1 (str) starting string
    s1 (str) ending string

    Returns an array of paths where each path is an array like
    [[("W","C"), ("O", "I"), ("R","C"), ("O", "I")], ...]

    Where "C" means the letter is in the correct place relative
    to the end string and "I" means that letter is not correct
    """

    paths = get_paths(G, s1, s2)

    correctness_paths = []

    for p in paths:
        path = []
        for w in p:
            word = []
            for i, letter in enumerate(w):
                word.append((letter, "C" if s2[i] == letter else "I"))
            path.append(word)
        correctness_paths.append(path)

    return correctness_paths




def gui_paths(G: nx.Graph, s1: str, s2: str):
    paths = get_paths(G, s1, s2)
    result = ["#" * 20]
    result.append(f'Solutions between "{s1}" and "{s2}"')
    result.append(
        f"Optimal path length: {len(paths[0])} ({len(paths[0]) -1} steps)"
    )
    for i, p in enumerate(paths):
        result.append(f"path {i+1:02d}: " + ", ".join(p))
    result.append("#" * 20)

    return result


def gui_paths_4(s1: str, s2: str):
    with open("./analysis/weaver-graph-4.pkl", "rb") as f:
        G4 = pickle.load(f)
    return gui_paths(G4, s1, s2)


def gui_paths_5(s1: str, s2: str):
    with open("./analysis/weaver-graph-5.pkl", "rb") as f:
        G5 = pickle.load(f)
    return gui_paths(G5, s1, s2)

def correctness_paths(s1: str, s2: str) -> tuple[List, Tuple]:

    if len(s1) == 4:
        with open("./analysis/weaver-graph-4.pkl", "rb") as f:
            G = pickle.load(f)
    else:
        with open("./analysis/weaver-graph-5.pkl", "rb") as f:
            G = pickle.load(f)


    errors = tuple()
    if s1 not in G:
        errors += (f'"{s1}" not in dictionary', )
    if s2 not in G:
        errors += (f'"{s2}" not in dictionary', )

    if len(errors):
        return [], errors
    else:
        return paths_with_correctness(G, s1, s2), tuple()

