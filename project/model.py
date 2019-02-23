import tensorflow as tf


class Model:
    """
    A class containing the computational graph for protein tertiary structure prediction using supervised learning
    """

    def __init__(self, primary, pssm, mask, answer, keep_prob):
        """
        Model initializer

        :param primary: ammino acid sequence. length n
        :param pssm: position specific scoring matrix. shape 21 x n
        :param mask: string of one-bit indicators showing which ammino acids are not to be penalized when computing loss. length n
        :param answer: correct tertiary structure
        :param keep_prob: contains dropout probability
        """

        self.primary = primary
        self.pssm = pssm
        self.mask = mask
        self.answer = answer
        self.keep_prob = keep_prob

        self.secondary = self.predict_secondary_structure()
        self.tertiary = self.predict_tertiary_structure()
        self.loss = self.loss_function()
        self.optimize = self.optimizing_function()
        self.accuracy = self.accuracy_function()

    def predict_secondary_structure(self):
        """
        This will use DeepCNF.

        :return: predicted secondary structure
        """
        pass

    def predict_tertiary_structure(self):
        """
        I haven't decided how yet.

        :return: predicted tertiary structure
        """
        pass
    
    def loss_function(self):
        """
        calculate the potential energy of the predicted tertiary structure and compare it to that of the answer

        :return: measure of how far the prediction is from the known structure
        """
        pass
    
    def optimizing_function(self):
        """
        optimizer for training the model. Leaning towards a momentum optimizer

        :return: optimizer for minimizing loss
        """
        pass

    def accuracy_function(self):
        """
        Calculate accuracy of predicted tertiary structure against the actual answer

        :return: measure of accuracy of prediction
        """
        pass
