import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime


def find_mcps(dag):
    edge_list = [(f"{i} out", f"{j} in") for (i, j) in dag.edges()]
    top_nodes = [f"{i} out" for (i, j) in dag.edges()]
    B = nx.Graph(edge_list)
    matching = nx.bipartite.maximum_matching(B, top_nodes=top_nodes)
    k = len(matching) / 2
    return k


def tree_to_dag(tree):
    digraph = tree.to_directed()
    edge_list = [(u, v) for (u, v) in digraph.edges() if u < v]
    dag = nx.DiGraph(edge_list)
    return dag


def main():
    # with open("mcps_max_flow.txt", "w") as file:
    #     file.write(f"{datetime.datetime.now()}\n")
    #     file.write(f"test, size, bmatching size, bmatching time\n")

    for dag_size in [10]:
        for iteration in range(1):
            tree = nx.random_tree(dag_size)
            dag = tree_to_dag(tree)

            st = time.time()
            biparmatch_mpcs = find_mcps(tree)
            biparmatch_time = time.time() - st

            # with open("mcps_max_flow.txt", "a") as file:
            #     file.write(f"{iteration+1}, {dag_size}, {bmatching_size}, {bmatching_time}\n")


if __name__ == "__main__":
    main()
