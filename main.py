from model import TablutModel
from tablut import *
import multiprocessing as mp
import random


def model_predict(model, nboards, p):
    # check if one board is winning move
    for board in nboards:
        if checkGameEnd(board, None) == p:
            return board
    return max([(model.evaluate(board, p), board) for board in nboards])[1]


def play_game(model_b, model_w, max_moves = 80):
    board = emptyBoard()
    initBoard(board)

    boards = [board]

    p, np = 'b', 'w'

    while checkGameEnd(boards, max_moves) == 'in progress':
        nboards = getAllNextBoards(boards[-1], p)
        boards.append(model_predict(model_b, nboards, p) if p == 'b' else model_predict(model_w, nboards, p))

        p, np = np, p

    return checkGameEnd(boards, max_moves)


# returns difference between score_b and score_w
def run_games(model_b, model_w, num_games = 20, max_moves = 120):

    # with mp.Pool(mp.cpu_count()) as pool:
    #     results = pool.starmap(play_game, [(model_b, model_w, max_moves) for _ in range(num_games)])
    results = [play_game(model_b, model_w, max_moves) for _ in range(num_games)]

    score_b = sum([1 if result == 'b' else -2 if result == 'w' else 0 for result in results])
    score_w = sum([1 if result == 'w' else -2 if result == 'b' else 0 for result in results])

    model_b.score += score_b
    model_w.score += score_w

    return score_b, score_w


def set_up_models(num_models = 10, loadFromFile = None):
    if loadFromFile is not None:
        models = [TablutModel(fromFile=loadFromFile)]
        for _ in range(num_models - 1):
            models.append(models[0].make_child())
    else:
        models  = [TablutModel() for _ in range(num_models)]

    return models
    

def train_models(models, num_games = 20, max_moves = 80, v=False):
    # for (i, model_b) in enumerate(models):
    #     for (j, model_w) in enumerate(models):
    #         if i == j:
    #             continue
    #         score_b, score_w = run_games(model_b, model_w, num_games, max_moves)
    #         model_b.score += score_b
    #         model_w.score += score_w
    #         if v:
    #             print(str(i) + ' vs ' + str(j) + ' : ' + str(score_b) + ' ' + str(score_w))
    args = []
    for (i, model_b) in enumerate(models):
        for (j, model_w) in enumerate(models):
            if i == j or random.random() > 0.5:
                continue
            args.append((model_b, model_w, num_games, max_moves))
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(run_games, args)



def main():
    num_iterations = 40
    num_models = 30  # must be even
    max_moves = 160
    num_games = 1
    loadFromFile = 2

    models = set_up_models(num_models, loadFromFile)

    start = (loadFromFile + 1) if loadFromFile is not None else 0
    end = start + num_iterations

    for i in range(start, end):
        print('Iteration ' + str(i))

        for model in models:
                model.score = 0

        train_models(models, num_games=num_games, max_moves=max_moves, v=False)

        models.sort(key = lambda x: x.score, reverse = True)

        for j, model in enumerate(models):
            print(str(j) + ' : ' + str(model.score))

        
        # best models
        
        models = models[:len(models)//2]
        for j in range(len(models)):
            models.append(models[j].make_child())

        #TODO: save/load models to file
        # if i % 10 == 0:
        models[0].saveToFiles(i)

        #TODO: make player v model capability


if __name__ == '__main__':
    main()
