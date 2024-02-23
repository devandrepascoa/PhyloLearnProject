import argparse
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def main():
    parser = argparse.ArgumentParser(description="Visualize dataset.")
    parser.add_argument('adj_matrix', help='Path to adjacency matrix file')
    args = parser.parse_args()

    adj_matrix = np.load(args.adj_matrix, allow_pickle=True)
    print(adj_matrix)
    plt.imshow(adj_matrix, cmap='hot', interpolation='nearest')
    plt.show()

    G = nx.from_numpy_array(adj_matrix)
    pos = nx.spring_layout(G)
    print("Graph is tree: ", nx.is_tree(G))
    nx.draw(G, pos,  with_labels=True, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    main()