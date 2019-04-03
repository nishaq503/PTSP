# HMMERD

The team is trying to recreate the results of the Cowen paper. They are trying to wrap the BLOSSUM62 matrix into HMMER. The sequences are classified into super-families by a probability score derived from the BLOSUM matrix. The team is having some problems getting the altered probabilities to sum to one.

Once the mathematical underpinnings of the probability calculations are done, the team can move on to updating the source code. The matrices need to be constrained correctly to stay within a tight neighborhood of real examples.