import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime


def find_mcps(dag):
    n = dag.number_of_nodes()
    v_edge_list = [
        (f"{v} in", f"{v} out", {"weight": 0, "capacity": 1}) for v in dag.nodes()
    ]
    s_edge_list = [("s", f"{v} in", {"weight": 0, "capacity": 1}) for v in dag.nodes()]
    t_edge_list = [(f"{v} out", "t", {"weight": 0, "capacity": 1}) for v in dag.nodes()]
    e_edge_list = [
        (f"{u} out", f"{v} in", {"weight": -1, "capacity": 1}) for (u, v) in dag.edges()
    ]
    N = nx.DiGraph(v_edge_list)
    N.add_node("s", demand=-n / 2)
    N.add_node("t", demand=n / 2)
    N.add_edges_from(s_edge_list)
    N.add_edges_from(t_edge_list)
    N.add_edges_from(e_edge_list)
    N.add_edge("s", "t", weight=0, capacity=n / 2)

    flow = nx.min_cost_flow_cost(N)

    return -flow


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

            # st = time.time()
            # minflow_mcps = find_mcps(dag)
            # minflow_time = time.time() - st

            # with open("mcps_max_flow.txt", "a") as file:
            #     file.write(f"{iteration+1}, {dag_size}, {bmatching_size}, {bmatching_time}\n")


if __name__ == "__main__":
    main()
