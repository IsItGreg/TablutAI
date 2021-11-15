from tablut import *


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
