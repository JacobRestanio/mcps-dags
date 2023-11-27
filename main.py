import linprog_cplex as cplex
import minflow
import biparmatch
import networkx as nx
import tracemalloc
import datetime
import time


def tree_to_dag(tree):
    digraph = tree.to_directed()
    edge_list = [(u, v) for (u, v) in digraph.edges() if u < v]
    dag = nx.DiGraph(edge_list)
    return dag


def main():
    with open("memory.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"Memory usage in KiB\n")
        file.write(f"size, minflow, bipartmatch, cplex\n")
    with open("time.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"Execution time in seconds\n")
        file.write(f"size, minflow, bipartmatch, cplex\n")
    with open("solution.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"The solution returned by each algorithm\n")
        file.write(f"size, minflow, bipartmatch, cplex\n")

    size = (int(i / 2 * 10**exp) for exp in range(2, 6) for i in range(2, 20))
    for dag_size in size:
        for i in range(100):
            print(f"test #{i+1}, size {dag_size}")
            tree = nx.random_tree(dag_size)
            dag = tree_to_dag(tree)

            tracemalloc.start()
            st = time.time()
            minflow_mcps = minflow.find_mcps(dag)
            minflow_time = time.time() - st
            current, minflow_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            biparmatch_mcps = biparmatch.find_mcps(dag)
            biparmatch_time = time.time() - st
            current, biparmatch_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            cplex_mcps = cplex.find_mcps(dag)
            cplex_time = time.time() - st
            current, cplex_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            with open("memory.txt", "a") as file:
                file.write(
                    f"{dag_size}, {minflow_mem / 1024}, {biparmatch_mem / 1024}, {cplex_mem / 1024}\n"
                )
            with open("time.txt", "a") as file:
                file.write(
                    f"{dag_size}, {minflow_time}, {biparmatch_time}, {cplex_time}\n"
                )
            with open("solution.txt", "a") as file:
                file.write(
                    f"{dag_size}, {minflow_mcps}, {biparmatch_mcps}, {cplex_mcps}\n"
                )


if __name__ == "__main__":
    main()
