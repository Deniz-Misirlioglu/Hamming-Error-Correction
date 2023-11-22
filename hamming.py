import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
#Generation
bit_matrix = np.random.randint(0,2,10000)

G = np.array([[1, 0, 0, 0, 1, 1, 0],
              [0, 1, 0, 0, 1, 0, 1], 
              [0, 0, 1, 0, 0, 1, 1], 
              [0, 0, 0, 1, 1, 1, 1]])


def encodeFourBits(four_bits):
    return np.dot(four_bits, G) % 2
   
encoded_bits= []

for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i+4];
    print(four_bits)
    encoded_bits += encodeFourBits(four_bits)
    print(encoded_bits)
    

