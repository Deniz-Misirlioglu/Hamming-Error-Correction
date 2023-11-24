import numpy as np
import sys
import matplotlib.pyplot as plt

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

def correctionMethod(bit_error_position):
    for index, row in enumerate(D):
        comparison = row == bit_error_position
        equal_arrays = comparison.all()
        if equal_arrays:
            return index
    return -1 


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


def compareMatrix(A,B):
    error_count = np.sum(A != B) 
    
    return error_count

##############################################################################

encoded_bits = []
original_encoded_bits = [];


#Encoding the bits and setting encoded_bits to a 7,2500 matrix of bits
for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i + 4]
    encoded_bits.extend(encodeFourBits(four_bits))
    original_encoded_bits = encoded_bits.copy()

p = [0.01, 0.05, 0.1, 0.2, .3, .5]
error_rates_before_correction = []
error_rates_after_correction = []

for i in p:
    tempMatrix = np.copy(encoded_bits)
    errorMatrix = errorCalculation(i, tempMatrix)
    
    error_before_correction = compareMatrix(tempMatrix, original_encoded_bits) / 17500
    error_rates_before_correction.append(error_before_correction)
    print("Error before correction for p =", i, ":", round(error_before_correction, 5))

    decoded_bits = [] 
    for seven_bits in errorMatrix:
        decodePostion = decodeSevenBits(seven_bits)
        bit_corrected = correctionMethod(decodePostion)
        
        if bit_corrected >= 0:
            if seven_bits[bit_corrected] == 0:
                seven_bits[bit_corrected] = 1
            else:
                seven_bits[bit_corrected] = 0

    error_after_correction = compareMatrix(errorMatrix, original_encoded_bits) / 17500
    error_rates_after_correction.append(error_after_correction)
    print("Error after correction for p =", i, ":", round(error_after_correction, 5))

# Plotting the data
plt.figure(figsize=(8, 6))
plt.plot(p, error_rates_before_correction, marker='o', label='Error Before Correction')
plt.plot(p, error_rates_after_correction, marker='x', label='Error After Correction')
plt.xlabel('Error Probability (p)')
plt.ylabel('Error Rate')
plt.title('Error Rates Before and After Correction')
plt.legend()
plt.grid(True)
plt.show()