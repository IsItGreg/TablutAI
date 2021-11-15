from tablut import *
import multiprocessing as mp


def model_predict(model, nboards, p):
    return random.choice(nboards)
    # return max([(model.evaluate(board, p)[0], board) for board in nboards])[1]


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
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply(play_game, args=(model_b, model_w, max_moves)) for _ in range(num_games)]
    pool.close()
    score_b = sum([1 if result == 'b' else -2 if result == 'w' else 0 for result in results])
    score_w = sum([1 if result == 'w' else -2 if result == 'b' else 0 for result in results])

    return score_b - score_w


def main():
    print("Hello World!")
    board = emptyBoard()
    initBoard(board)

    printBoard(board)

    boards = [board]

    p, np = 'b', 'w'

    while checkGameEnd(boards) == 'in progress':
        nboards = getAllNextBoards(boards[-1], p)
        boards.append(random.choice(nboards))

        print('-----------------')
        printBoard(boards[-1])
        print('-----------------\n')

        p, np = np, p

    print('Game end - ' + checkGameEnd(boards))
    print('Num moves - ' + str(len(boards)))




if __name__ == '__main__':
    main()
