import random


class TablutModel:
    score = 0
    weights = 0 # TODO: replace with actual model

    def __init__(self, parent_weights=None, l=1e-3):
        if parent_weights is not None:
            self.weights = parent_weights + l * random.random() 
            # following this idea to add some variation to the child
            # might need to adjust the l value
        else:
            self.weights = random.random()
        

    def evaluate(self, board, p):
        #TODO: implement
        return random.random()

    def make_child(self) -> 'TablutModel':
        return TablutModel(self.weights)