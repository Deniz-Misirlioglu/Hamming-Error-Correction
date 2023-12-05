import numpy as np
import sys
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

#Randomly setting the bit for a 10000 1D Array
bit_matrix = np.random.randint(0, 2, 50000)

allChannelStates = []
inStateGood = bool(True);

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

#Comparing matrix A to B
def compareMatrix(A,B):
    error_count = np.sum(A != B) 
    return error_count


#Original arrays of bits
encoded_bits = []
original_encoded_bits = [];
errorProbability = 0;

#Encoding The bits
for i in range(0, len(bit_matrix), 4):
    four_bits = bit_matrix[i:i + 4]
    encoded_bits.extend(encodeFourBits(four_bits))


#Copying the bits to original_encode_bits
original_encoded_bits = np.copy(encoded_bits)
numOfError = 0;


#Calculating the state and error for the encoded bits
for encodedBits in encoded_bits:
    for i in range(len(encodedBits)):

        #Random error integer 0-1 for error probability
        bitErrorRandomNumber = round(np.random.rand(), 2)  
        
        #If satemenet for State = GOOD
        if inStateGood == True:

            #Random number for the State probability
            stateRandomNumber = round(np.random.rand(), 2)
            
            if stateRandomNumber <= .9: 
                allChannelStates.append("good")
                errorProbability = .01
                inStateGood = bool(True);

                #Bit error occuring on good state
                if bitErrorRandomNumber <= .01:
                    numOfError = numOfError + 1    
                    if encodedBits[i] == 1:
                        encodedBits[i] = 0
                    else:
                        encodedBits[i] = 1    

            #Converting to bad State given probability
            else:
                allChannelStates.append("bad")
                errorProbability = .1
                inStateGood = bool(False);
                #Bit error occuring on bad state
                if bitErrorRandomNumber <= .1:
                            numOfError = numOfError + 1
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
        
        #Else satemenet for State = BAD
        else:
            errorProbability = .1
            stateRandomNumber = round(np.random.rand(), 2)
            
            #Converting to good state
            if stateRandomNumber <= .6:
                allChannelStates.append("good")
                errorProbability = .01
                inStateGood = bool(True);
                #Bit error occuring on good state
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
                #Bit error occuring on bad state
                if bitErrorRandomNumber <= .1:    
                            numOfError = numOfError + 1
                            if encodedBits[i] == 1:
                                encodedBits[i] = 0
                            else:
                                encodedBits[i] = 1
    
numofErrorCorrected = 0;


# Decoding the matrix and correcting the found bit errors
for sevenBits in encoded_bits:
    decodePostion = decodeSevenBits(sevenBits)
    bit_corrected = correctionMethod(decodePostion)
    
    #If index of bit error is greater or equal to zero
    if bit_corrected >= 0:
                numofErrorCorrected = numofErrorCorrected + 1;
                if sevenBits[bit_corrected] == 0:
                    sevenBits[bit_corrected] = 1
                else:
                    sevenBits[bit_corrected] = 0

#The ammount of errors in the new matrix after correction
error_after_correction = compareMatrix(original_encoded_bits, encoded_bits)

#Plot Definition for states
numeric_states = [0 if state == 'good' else 1 for state in allChannelStates]
interval = 500
aggregated_states = [numeric_states[i:i + interval] for i in range(0, len(numeric_states), interval)]


proportions_bad = [sum(interval_states) / len(interval_states) for interval_states in aggregated_states]
proportions_good = [1 - p for p in proportions_bad]

#First plot showing the good vs bad state diagrams
plt.figure(figsize=(12, 6))
plt.plot(proportions_good, 'o-', color='green')
plt.plot(proportions_bad, 'o-', color='red')
plt.xlabel('Interval (each representing {} bits)'.format(interval))
plt.ylabel('Proportion of Good State')
plt.title('Proportion of Good State Over Time')
plt.ylim(0, 1) 
plt.show()

#Second plot showing the number of errors before and after correction
plt.figure(figsize=(8, 6))
plt.bar(["Errors Before Corrections " + numOfError.__str__(), "Errors After Correction " + error_after_correction.__str__()], [numOfError, error_after_correction], color=['red', 'black'])
plt.xlabel('Metrics')
plt.ylabel('Errors')
plt.title('Comparison of Error After Correction and Number of Errors')
plt.ylim(0, max(error_after_correction, numOfError) * 1.2)
plt.show()
