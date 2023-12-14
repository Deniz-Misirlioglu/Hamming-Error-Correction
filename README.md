
Abstract
This project explores Hamming Error correction with two different models. Hamming error
correction is an error correction method designed to resolve single-bit errors. When transmitting
and receiving data, errors can regularly occur and this represents a wrong set of data compared to
what was originally transmitted. Hamming Error correction is designed to add parity bits to the
original data, thus allowing for single error correction capabilities. This idea was proposed by
Richard Hamming in the late 1940s. For this project, we focus on (7,4) Hamming codes, which
take in 4 binary bits of data, and encodes them with 3 parity bits.

Overview
In this project, Python is used to simulate the transmission and reception of 10, 20, and 50
thousand bits for channel 1, and 10000 and 50000 bits for channel 2. Bits are taken in pairs of 4,
and encoded using a Hamming generator matrix. With a given transmission, a bit of error
probability is added introducing random noise to the transmission. A bit could have been
transmitted as a 1, but the receiver could read it as a 0 given the bit is in error. However, in (7,4)
Hamming codes, a single bit in error can be detected and corrected by using the decoder matrix.
In this project, two channels were simulated, each with its specific requirements. In this project,
we added some more error probability parameters to gain more accurate data. All data for
channel 1 and channel 2 was calculated as an average of 3 iterations to gain more accurate
numerical values.
