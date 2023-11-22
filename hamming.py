import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

bit_matrix = np.random.randint(0, 2, 10000)

G = np.array([[1, 0, 0, 0, 1, 1, 1],
              [0, 1, 0, 0, 1, 1, 0],
              [0, 0, 1, 0, 1, 0, 1],
              [0, 0, 0, 1, 0, 1, 1]])

D = np.array([[1,1,1],
              [1,1,0],
              [1,0,1],
              [0,1,1],
              [1,0,0],
              [0,1,0],
              [0,0,1]])

def encodeFourBits(four_bits):
    four_bits = four_bits.reshape(1, -1)
    return np.dot(four_bits, G) % 2

def decodeSevenBits(seven_bits):
    seven_bits = seven_bits.reshape(1, -1)
    return np.dot(seven_bits, D) % 2

encoded_bits = []

#Encoding the bits and setting encoded_bits to a 7,2500 matrix of bits
for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i + 4]
    encoded_bits.extend(encodeFourBits(four_bits))


def errorCalculation(p, matrix):
    errorCount = 0;
    for seven_bits in matrix:
        for i in range(len(seven_bits)):
            random_number_np = round(np.random.rand(), 2)
            if random_number_np <= p:
                errorCount = errorCount + 1
                if seven_bits[i] == 1:
                    seven_bits[i] = 0
                else:
                    seven_bits[i] = 1
    return matrix



p = [0.01]

for i in p:
    tempMatrix = np.copy(encoded_bits)
    errorMatrix = errorCalculation(i, tempMatrix)

    decoded_bits = [] 
    for seven_bits in errorMatrix:
        decoded_bits.extend(decodeSevenBits(seven_bits))

    decoded_bits = np.vstack(decoded_bits) 

    print(decoded_bits)







encoded_bits = np.vstack(encoded_bits)

