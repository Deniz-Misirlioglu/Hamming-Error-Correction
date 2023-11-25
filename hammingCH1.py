#Created by Deniz and Riley
import numpy as np
import sys
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

#Randomly setting the bit for a 10000 1D Array
bit_matrix = np.random.randint(0, 2, 10000)

#The encoder matrix 4x7
G = np.array([[1, 0, 0, 0, 1, 1, 1],
              [0, 1, 0, 0, 1, 1, 0],
              [0, 0, 1, 0, 1, 0, 1],
              [0, 0, 0, 1, 0, 1, 1]])

#The decoder matrix 7x3
D = np.array([[1,1,1],
              [1,1,0],
              [1,0,1],
              [0,1,1],
              [1,0,0],
              [0,1,0],
              [0,0,1]])

#Encoding the four bits, and returning 7 [X,X,X,X] -> [X,X,X,X,X,X,X]
def encodeFourBits(four_bits):
    four_bits = four_bits.reshape(1, -1)
    return np.dot(four_bits, G) % 2

#Decoing the seven bits, and recieving the error code [X,X,X,X,X,X,X] -> [X,X,X]
def decodeSevenBits(seven_bits):
    seven_bits = seven_bits.reshape(1, -1)
    return np.dot(seven_bits, D) % 2

#Finding the index of the bit which needs correcting based off the of the D matrix, -1 otherwise
def correctionMethod(bit_error_position):
    for index, row in enumerate(D):
        comparison = row == bit_error_position
        equal_arrays = comparison.all()
        if equal_arrays:
            return index
    return -1 

#Performing the error operation in the matrix by a given prob P, and matrix
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

#Comparing matrix A to B
def compareMatrix(A,B):
    error_count = np.sum(A != B) 
    
    return error_count


#__main_()-----------------------------------------------------------------------------

#Empty arrays for the encoded bits
encoded_bits = []
original_encoded_bits = []


#Encoding the bits and setting encoded_bits to a 7,2500 matrix of bits
for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i + 4]
    encoded_bits.extend(encodeFourBits(four_bits))
    original_encoded_bits = np.copy(encoded_bits)

#Probabilities P for the given matricies
p = [0.01, 0.05, 0.1, 0.2, .3, .5]

error_rates_before_correction = []
error_rates_after_correction = []


#Calculating the bit errors and their position in given [X,X,X] and swapping the error
for i in p:
    tempMatrix = np.copy(encoded_bits)
    errorMatrix = errorCalculation(i, tempMatrix)
    
    error_before_correction = compareMatrix(tempMatrix, original_encoded_bits) / 17500
    error_rates_before_correction.append(error_before_correction)
    print("Error before correction for p =", i, ":", round(error_before_correction, 5))

    decoded_bits = [] 

    for seven_bits in errorMatrix:
        #Decoding the given [X,X,X,X,X,X,X] -> [X,X,X]
        decodePostion = decodeSevenBits(seven_bits)
        bit_corrected = correctionMethod(decodePostion)
        
        #Swapping here if index is >= 0
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