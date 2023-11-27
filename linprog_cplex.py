import pulp as lp
import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime


def find_mcps(dag):
    node_list = list(dag.nodes)
    edge_list = list(dag.edges)
    C = set()

    model = lp.LpProblem(name="mpcs-problem", sense=lp.LpMaximize)

    # decision variables
    X = {
        (u, v): lp.LpVariable(name=f"x_({u},{v})", lowBound=0, upBound=1)
        for (u, v) in edge_list
    }

    # objective function
    model += lp.lpSum(X.values())

    # constraints
    for n in node_list:
        model += (
            lp.lpSum(
                [x for (u, v), x in X.items() if (u, v) in dag.out_edges(nbunch=n)]
            )
            <= 1,
            f"c_out_{n}",
        )
        model += (
            lp.lpSum([x for (u, v), x in X.items() if (u, v) in dag.in_edges(nbunch=n)])
            <= 1,
            f"c_in_{n}",
        )

    model.solve(lp.CPLEX_CMD(msg=False, timeLimit=1800))

    return model.objective.value()


def tree_to_dag(tree):
    digraph = tree.to_directed()
    edge_list = [(u, v) for (u, v) in digraph.edges() if u < v]
    dag = nx.DiGraph(edge_list)
    return dag


def main():
    # file = open("mcps_linprog_cplex.txt", "w")
    # file.write(f"{datetime.datetime.now()}\n")
    # file.write(f"test, size, cplex size, cplex time\n")

    for dag_size in [10]:
        for iteration in range(1):
            tree = nx.random_tree(dag_size)
            dag = tree_to_dag(tree)

            find_mcps(dag)

    #         st = time.time()
    #         cplex_mcps = find_mcps(tree)
    #         cplex_time = time.time() - st
    #         cplex_size = len(cplex_mcps)

    #         file.write(f"{iteration+1}, {tree_size}, {cplex_size}, {cplex_time}\n")

    # file.close()


if __name__ == "__main__":
    main()
