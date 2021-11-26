from model import TablutModel
from tablut import *
import multiprocessing as mp


def model_predict(model, nboards, p):
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
def run_games(model_b, model_w, num_games = 20, max_moves = 80):
    args = [(model_b, model_w, max_moves) for _ in range(num_games)]
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(play_game, [(model_b, model_w, max_moves) for _ in range(num_games)])

    score_b = sum([1 if result == 'b' else -2 if result == 'w' else 0 for result in results])
    score_w = sum([1 if result == 'w' else -2 if result == 'b' else 0 for result in results])

    return score_b, score_w


def set_up_models(num_models = 10):
    models  = [TablutModel() for _ in range(num_models)]

    return models
    

def train_models(models, num_games = 20, max_moves = 80):
    for (i, model_b) in enumerate(models):
        for (j, model_w) in enumerate(models):
            if i == j:
                continue
            score_b, score_w = run_games(model_b, model_w, num_games, max_moves)
            model_b.score += score_b
            model_w.score += score_w
            print(str(i) + ' vs ' + str(j) + ' : ' + str(score_b) + ' ' + str(score_w))


def main():
    num_iterations = 2
    models = set_up_models(4)

    for i in range(num_iterations):
        print('Iteration ' + str(i))

        for model in models:
                model.score = 0

        train_models(models, num_games = 20, max_moves = 80)

        models.sort(key = lambda x: x.score, reverse = True)

        for model in models:
            print(model.score)
        
        # best models
        models = models[:len(models)//2]
        for model in models[:len(models)//2]:
            models.append(model.make_child())

        #TODO: save/load models to file

        #TODO: make player v model capability


if __name__ == '__main__':
    main()
