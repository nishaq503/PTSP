# Notes and Ideas for project
## Najib Ishaq and Tom Howard

### Training data includes:
* Protein primary structure: amino acid sequence. anywhere from 21 to 3500 units long. (length n)

* PSSM: position specific scoring matrix. stores propensity of amino acids to morph into other amino acids. (shape 21 x n)

* Tertiary Structure: 3D structure of N, C_alpha, and C' atoms in the backbone of the protein after it is done folding up. This is made up of n 3x3 matrices where the rows are x, y, and z coordinates respectively and the columns correspond to N, C_alpha, and C' atoms respectively. (shape 3 x 3n).

* Mask: one-bit indicator of when protein residue information is present. This is to keep the loss function from penalizing predictions made for atoms for which residue information is not present. (length n)

### Current Ideas:
* The training set haas ~87k samples. These may not be enough so we may build upon the paper on "Feedback GAN for generating DNA sequences" to generate more amino acid sequences.
* Go from Primary to Secondary structure using DEEPCNF. This can be replaced later with our own implementation of DEEPCNF.
* Use Primary and Secondary structures along with PSSM to predict Tertiary structure. Tertiary structure must not violate primary and secondary structure constraints. 
* This can be treated as supervised learning because tertiary structure is given for proteins in training set.
* This can also be treated as unsupervised learning by minimizing folding time and potential energy as metrics.
* This can possibly be treated as a hybrid model by using training examples to learn a relationship between primary structure and potential energy of tertiary structure. We could then use generated amino acid sequences to train the model using reinforcement learning.
* As Tom pointed out, the tertiary structure screams graph. I guess a grad course on graph theory CAN be useful in real life. The idea is very good and will almost certainly be used here. At the very least, it will allow for rotational and translational invariance when comparing tertiary structures.

**Are there partial-sequences for which the model predicts very accurate tertiary structures?**
* Calculate the accuracy for partial sequences to see if there are sections for which the model makes excellent predictions.
* If there are such partial sequences, incorporate them into further predictions and use a vector of "edit costs" to discourage changing these partial strictures in the full prediction.
* Could use partial sequences and partial structures to train model.
