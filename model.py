import random
import numpy as np
import os.path


class TablutModel:
    score = 0
    # weights = 0 # TODO: replace with actual model

    w1 = np.zeros((82, 128))
    b1 = np.zeros((128,))
    w2 = np.zeros((128, 32))
    b2 = np.zeros((32,))
    w3 = np.zeros((32, 1))
    b3 = np.zeros((1,))


    def __init__(self, parent_weights=None, l=1e-2, fromFile=None):
        if fromFile:
            self.w1 = np.genfromtxt('saves/' + str(fromFile) + '/w1.csv', delimiter=',')
            self.b1 = np.genfromtxt('saves/' + str(fromFile) + '/b1.csv', delimiter=',')
            self.w2 = np.genfromtxt('saves/' + str(fromFile) + '/w2.csv', delimiter=',')
            self.b2 = np.genfromtxt('saves/' + str(fromFile) + '/b2.csv', delimiter=',')
            self.w3 = np.genfromtxt('saves/' + str(fromFile) + '/w3.csv', delimiter=',')
            self.b3 = np.genfromtxt('saves/' + str(fromFile) + '/b3.csv', delimiter=',')
            pass

        
        elif parent_weights is not None:
            w1, b1, w2, b2, w3, b3 = parent_weights
            self.w1 = w1 + l * np.random.randn(*w1.shape)
            self.b1 = b1 + l * np.random.randn(*b1.shape)
            self.w2 = w2 + l * np.random.randn(*w2.shape)
            self.b2 = b2 + l * np.random.randn(*b2.shape)
            self.w3 = w3 + l * np.random.randn(*w3.shape)
            self.b3 = b3 + l * np.random.randn(*b3.shape)

            # self.weights = parent_weights + l * random.random() 
            # following this idea to add some variation to the child
            # might need to adjust the l value
        else:
            self.w1 = np.random.randn(82, 128)
            self.b1 = np.random.randn(128,)
            self.w2 = np.random.randn(128, 32)
            self.b2 = np.random.randn(32,)
            self.w3 = np.random.randn(32, 1)
            self.b3 = np.random.randn(1,)
        

    def evaluate(self, board, p):
        #TODO: implement
        flat_board = np.array(board).flatten()
        flat_board = np.append(flat_board, p)
        # flat_board.append(p)
        
        # print(flat_board)

        x = np.zeros_like(flat_board, dtype=np.float64)
        x = x + (flat_board == 'b') * 1
        x = x + (flat_board == 'w') * 2
        x = x + (flat_board == 'K') * 3

        # print(x)

        x = x.dot(self.w1) + self.b1
        x = np.maximum(x, 0)
        x = x.dot(self.w2) + self.b2
        x = np.maximum(x, 0)
        x = x.dot(self.w3) + self.b3

        # print(x)

        return x

        # return random.random()


    def make_child(self) -> 'TablutModel':
        weights = (self.w1, self.b1, self.w2, self.b2, self.w3, self.b3)
        return TablutModel(weights)

    
    def saveToFiles(self, iteration):
        if not os.path.exists('saves/' + str(iteration)):
            os.makedirs('saves/' + str(iteration))
        np.savetxt('saves/' + str(iteration) + '/w1.csv', self.w1, delimiter=',')
        np.savetxt('saves/' + str(iteration) + '/b1.csv', self.b1, delimiter=',')
        np.savetxt('saves/' + str(iteration) + '/w2.csv', self.w2, delimiter=',')
        np.savetxt('saves/' + str(iteration) + '/b2.csv', self.b2, delimiter=',')
        np.savetxt('saves/' + str(iteration) + '/w3.csv', self.w3, delimiter=',')
        np.savetxt('saves/' + str(iteration) + '/b3.csv', np.array(self.b3, ndmin=1), delimiter=',')

        
