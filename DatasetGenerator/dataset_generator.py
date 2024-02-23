#!/usr/bin/env python
import math
import sys
import numpy as np
import os
import argparse
from goe_burst import kruskal, calc_lvs
from tqdm import tqdm

def load_profiles(profiles_in):
    profiles = []
    ct = 0
    fp = open(profiles_in, 'r')
    for line in fp:
        ct += 1
        profiles.append(line.rstrip().split('\t'))
    fp.close()

    profiles.pop(0)
    for i in range(len(profiles)):
        profiles[i].pop(0)

    return profiles


# Class UF from 	https://www.ics.uci.edu/~eppstein/PADS/UnionFind.py


def generate_adjacency_matrix(tree, num_nodes):
    adj_matrix = np.zeros((num_nodes, num_nodes))
    for edge in tree:
        adj_matrix[edge[0], edge[1]] = 1
        adj_matrix[edge[1], edge[0]] = 1
    return adj_matrix


def write_adj_matrix_to_file(adj_matrix, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    # Write the adjacency matrix to a png file

    np.save(output_file, adj_matrix)


def write_chunk_to_file(profiles_chunk, output_file):
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(output_file, "w") as fp:
        for profile in profiles_chunk:
            for i in range(len(profile)):
                fp.write(profile[i] + " ")
            fp.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Generate adjacency matrix from profiles.")
    parser.add_argument('profiles_in', help='Path to profiles file')
    parser.add_argument('output_dir', help='Path to output directory')
    parser.add_argument('chunk_size', help='Number of profiles in each chunk')

    args = parser.parse_args()

    profiles = load_profiles(args.profiles_in)

    num_chunks = math.ceil(len(profiles) / int(args.chunk_size))

    profile_chunks = np.array_split(profiles, num_chunks)

    for i, profiles_chunk in enumerate(tqdm(profile_chunks)):
        write_chunk_to_file(profiles_chunk, args.output_dir + "/profiles/profiles_" + str(i) + ".txt")

        lvs, max_len = calc_lvs(profiles_chunk)
        tree = kruskal(profiles_chunk, lvs, max_len)

        adj_matrix = generate_adjacency_matrix(tree, len(profiles_chunk))

        write_adj_matrix_to_file(adj_matrix, args.output_dir + "/adjacency_matrix/adj_matrix_" + str(i))

    # iterates over all possible chunk combinations
    # for i in tqdm(range(num_chunks)):
    #     for j in tqdm(range(i+1, num_chunks)):
    #         profiles_chunk = np.concatenate((profile_chunks[i], profile_chunks[j]), axis=0)
    #         write_chunk_to_file(profiles_chunk, args.output_dir + "/profiles/profiles_" + str(i) + "_" + str(j) + ".txt")
    #
    #         lvs, max_len = calc_lvs(profiles_chunk)
    #         tree = kruskal(profiles_chunk, lvs, max_len)
    #
    #         adj_matrix = generate_adjacency_matrix(tree, len(profiles_chunk))
    #
    #         write_adj_matrix_to_file(adj_matrix, args.output_dir + "/adjacency_matrix/adj_matrix_" + str(i) + "_" + str(j))
    #
if __name__ == "__main__":
    main()
