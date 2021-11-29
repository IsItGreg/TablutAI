# all methods with an underscore modify in place
# tensors made from numpy arrays and numpy arrays made from tensors share the same memory location if operation done on CPU
# creating

import random
import sys
import torch
import numpy as np
import torch.nn as nn
import tablut
import pdb

'''
if torch.cuda.is_available():
    d = torch.device('cuda')
    x = torch.ones(5, device=d)
    
    or 
    
    x = x.to(device)
    
    now z = x + y is performed on the GPU 
    
    x = x.to('cpu') moves back to cpu. Numpy only works on CPU
    
    x = torch.ones(5, requires_grad=True) - Means we will calculate gradient and optimize this tensor, default is false
    
    
'''

# input is 1D array of the board state


'''
FC
2 Hidden Layers
    1st has 40 hidden nodes
    2nd has 10 hidden nodes

piece differential 
    
nonlinearity is hyperbolic tangent 
'''


class TablutModel(nn.Module):
    score = 0
    weights = 0  # TODO: replace with actual model

    # xavier initalizaiton
    def __init__(self, parent_weights=None, l=1e-3, hidden_size=(40, 10), input_size=82):
        super(TablutModel, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size[0])
        self.tanh1 = nn.Tanh()
        self.l2 = nn.Linear(hidden_size[0], hidden_size[1])
        self.tanh2 = nn.Tanh()

        # return a scalar
        self.l3 = nn.Linear(hidden_size[1], out_features=1)

        # operations done on gpu if cuda available else it is done on cpu
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 81 positions on the board plus the flag indicating which player
        shape = (82, 1)
        if parent_weights is not None:
            self.weights = parent_weights + l * nn.init.xavier_normal_(torch.ones(shape))
            # following this idea to add some variation to the child
            # might need to adjust the l value
        else:
            self.weights = nn.init.xavier_normal_(torch.ones(shape))

    # black is attacker
    # white is defender
    # outputs 0 to 1 inclusive
    # function
    def evaluate(self, board, p):
        num_pieces_player = len(tablut.getPiecesToMove(board, p))
        if p == 'b':
            opposing = 'w'
        else:
            opposing = 'b'
        num_pieces_opposing = len(tablut.getPiecesToMove(board, opposing))
        tanH = nn.Tanh()
        eval_score = tanH(torch.tensor(num_pieces_player - num_pieces_opposing))

        return eval_score

    # xavier initialization
    # weights saved to a text file
    # self.weights is the parent weights for the next created child
    def make_child(self) -> 'TablutModel':
        return TablutModel(self.weights)


def train(board, p):
    lossf = nn.MSELoss()

    board_np = np.array(board)
    input_nn = board_np.ravel()
    # creates new array with player designation at end of the input
    input_nn = np.append(input, p)

    model = TablutModel()

    optimizer = torch.optim.Adam(model.parameters(), lr=model.l)

    output = model(input_nn)


if __name__ == "__main__":
    pass
