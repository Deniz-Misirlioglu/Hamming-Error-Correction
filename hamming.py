import numpy as np

#Generation
bit_matrix = np.random.randint(2, size=(1, 10000))
print(bit_matrix)

#Encode
for bits in bit_matrix:
    print(bits)
