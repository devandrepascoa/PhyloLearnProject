# Convert folder of .npy to .png without showing image

import os
import numpy as np
from PIL import Image
import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert .npy to .png")
    parser.add_argument('input_dir', help='Path to input directory')
    parser.add_argument('output_dir', help='Path to output directory')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    for filename in os.listdir(input_dir):
        if filename.endswith(".npy"):
            adj_matrix = np.load(input_dir + filename)
            adj_matrix = adj_matrix * 255

            if not os.path.exists(os.path.dirname(output_dir)):
                os.makedirs(os.path.dirname(output_dir))

            img = Image.fromarray(adj_matrix)
            img = img.convert('RGB')
            img.save(output_dir + filename[:-4] + '.png')

if __name__ == "__main__":
    main()