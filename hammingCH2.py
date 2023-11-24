import numpy as np
import sys
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

bit_matrix = np.random.randint(0, 2, 10000)
allChannelStates = []
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
                allChannelStates.append("good")
                errorProbability = .01
                inStateGood = bool(True);

                if bitErrorRandomNumber <= .01:
                    numOfError = numOfError + 1    
                    if encodedBits[i] == 1:
                        encodedBits[i] = 0
                    else:
                        encodedBits[i] = 1    


            else:
                allChannelStates.append("bad")
                errorProbability = .1
                inStateGood = bool(False);
                if bitErrorRandomNumber <= .1:
                            numOfError = numOfError + 1
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
        
        #BAD STATE
        else:
            errorProbability = .1
            stateRandomNumber = round(np.random.rand(), 2)
            
            if stateRandomNumber <= .6:
                allChannelStates.append("good")
                errorProbability = .01
                inStateGood = bool(True);
                if bitErrorRandomNumber <= .01:
                            numOfError = numOfError + 1
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1

            else:
                allChannelStates.append("bad")
                errorProbability = .1
                inStateGood = bool(False);
                if bitErrorRandomNumber <= .1:    
                            numOfError = numOfError + 1
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
    

#######Decoding
tempMatrix = np.copy(encoded_bits)
for sevenBits in tempMatrix:
    decodePostion = decodeSevenBits(sevenBits)
    bit_corrected = correctionMethod(decodePostion)

    if bit_corrected >= 0:
                if sevenBits[bit_corrected] == 0:
                    sevenBits[bit_corrected] = 1
                else:
                    sevenBits[bit_corrected] = 0


error_after_correction = compareMatrix(encoded_bits, tempMatrix)

print("The error count is",error_after_correction);

numeric_states = [0 if state == 'good' else 1 for state in allChannelStates]

interval = 500
aggregated_states = [numeric_states[i:i + interval] for i in range(0, len(numeric_states), interval)]

proportions_bad = [sum(interval_states) / len(interval_states) for interval_states in aggregated_states]
proportions_good = [1 - p for p in proportions_bad]


plt.figure(figsize=(12, 6))
plt.plot(proportions_good, 'o-', color='green')
plt.plot(proportions_bad, 'o-', color='red')
plt.xlabel('Interval (each representing {} bits)'.format(interval))
plt.ylabel('Proportion of Good State')
plt.title('Proportion of Good State Over Time')
plt.ylim(0, 1) 
plt.show()


plt.figure(figsize=(8, 6))
plt.bar(["Errors Before Corrections", "Errors After Correction"], [numOfError, error_after_correction], color=['red', 'black'])
plt.xlabel('Metrics')
plt.ylabel('Errors')
plt.title('Comparison of Error After Correction and Number of Errors')
plt.ylim(0, max(error_after_correction, numOfError) * 1.2)
plt.show()