import numpy as np
import sys
from enum import Enum

np.set_printoptions(threshold=sys.maxsize)

bit_matrix = np.random.randint(0, 2, 10000)

inStateGood = bool(True);

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

encoded_bits = []
original_encoded_bits = [];
errorProbability = 0;

#Encoding The bits
for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i + 4]
    encoded_bits.extend(encodeFourBits(four_bits))
    original_encoded_bits = encoded_bits.copy()


numOfError = 0;
for encodedBits in encoded_bits:

    for i in range(len(encodedBits)):

        bitErrorRandomNumber = round(np.random.rand(), 2)  
        #GOOD STATE
        if inStateGood == True:
            stateRandomNumber = round(np.random.rand(), 2)

            if stateRandomNumber <= .9:   
                errorProbability = .01
                inStateGood = bool(True);

                if bitErrorRandomNumber <= .01:
                    numOfError = numOfError + 1    
                    print("recieved error in good state with errorRandom as", bitErrorRandomNumber)
                    if encodedBits[i] == 1:
                        encodedBits[i] = 0
                    else:
                        encodedBits[i] = 1


            else:
                errorProbability = .1
                inStateGood = bool(False);
                if bitErrorRandomNumber <= .1:
                            numOfError = numOfError + 1
                            print("recieved error in bad state", bitErrorRandomNumber)
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
        
        #BAD STATE
        else:
            errorProbability = .1
            stateRandomNumber = round(np.random.rand(), 2)
            
            
            if stateRandomNumber <= .6:
                errorProbability = .01
                inStateGood = bool(True);
                if bitErrorRandomNumber <= .01:
                            numOfError = numOfError + 1
                            print("recieved error in good state with errorRandom as", bitErrorRandomNumber)
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1

            else:
                errorProbability = .1
                inStateGood = bool(False);
                if bitErrorRandomNumber <= .1:    
                            numOfError = numOfError + 1
                            print("recieved error in bad state", bitErrorRandomNumber)
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
    
print(numOfError)