from copy import deepcopy
import random


def emptyBoard():
    board = []
    for _ in range(9):
        board.append([' '] * 9)
    return board


def initBoard(board):
    board[4][4] = 'K'
    board[3][0] = 'b'
    board[4][0] = 'b'
    board[5][0] = 'b'
    board[4][1] = 'b'
    board[0][3] = 'b'
    board[0][4] = 'b'
    board[0][5] = 'b'
    board[1][4] = 'b'
    board[3][8] = 'b'
    board[4][8] = 'b'
    board[5][8] = 'b'
    board[4][7] = 'b'
    board[8][3] = 'b'
    board[8][4] = 'b'
    board[8][5] = 'b'
    board[7][4] = 'b'
    board[4][2] = 'w'
    board[4][3] = 'w'
    board[4][5] = 'w'
    board[4][6] = 'w'
    board[2][4] = 'w'
    board[3][4] = 'w'
    board[5][4] = 'w'
    board[6][4] = 'w'
    board[0][0] = 'e'
    board[0][8] = 'e'
    board[8][0] = 'e'
    board[8][8] = 'e'


def getMovesForPiece(board, x, y):
    moves = []
    p = board[x][y]
    nx = x
    while nx < 8:
        nx += 1
        if board[nx][y] == ' ' or p == 'K' and board[nx][y] == 'e':
            moves.append((nx, y))
        else:
            break
    nx = x
    while nx > 0:
        nx -= 1
        if board[nx][y] == ' ' or p == 'K' and board[nx][y] == 'e':
            moves.append((nx, y))
        else:
            break
    ny = y
    while ny < 8:
        ny += 1
        if board[x][ny] == ' ' or p == 'K' and board[x][ny] == 'e':
            moves.append((x, ny))
        else:
            break
    ny = y
    while ny > 0:
        ny -= 1
        if board[x][ny] == ' ' or p == 'K' and board[x][ny] == 'e':
            moves.append((x, ny))
        else:
            break

    if (4, 4) in moves:
        moves.remove((4, 4))

    return moves


def getPiecesToMove(board, p):
    pieces = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == p or p == 'w' and board[i][j] == 'K':
                pieces.append((i, j))
    return pieces


def getAllPossibleMoves(board, p):
    moves = []
    for piece in getPiecesToMove(board, p):
        for move in getMovesForPiece(board, piece[0], piece[1]):
            moves.append((piece, move))
    return moves


def getNextBoard(board, move):
    nextBoard = deepcopy(board)
    old = move[0]
    new = move[1]
    nextBoard[new[0]][new[1]] = nextBoard[old[0]][old[1]]
    nextBoard[old[0]][old[1]] = ' '
    if old[0] == 4 and old[1] == 4:
        nextBoard[4][4] = 'c'

    p = 'w' if nextBoard[new[0]][new[1]] != 'b' else 'b'
    np = 'b' if p == 'w' else 'w'

    # Capturing
    if nextBoard[new[0]][new[1]] == 'K':
        pass
    else:
        try:
            if nextBoard[new[0] + 1][new[1]] == np and nextBoard[new[0] + 2][new[1]] == p or nextBoard[new[0] + 2][new[1]] == 'e':
                nextBoard[new[0] + 1][new[1]] = ' '
        except:
            pass
            
        try:
            if nextBoard[new[0] - 1][new[1]] == np and nextBoard[new[0] - 2][new[1]] == p or nextBoard[new[0] - 2][new[1]] == 'e':
                nextBoard[new[0] - 1][new[1]] = ' '
        except:
            pass

        try:
            if nextBoard[new[0]][new[1] + 1] == np and nextBoard[new[0]][new[1] + 2] == p or nextBoard[new[0]][new[1] + 2] == 'e':
                nextBoard[new[0]][new[1] + 1] = ' '
        except:
            pass

        try:
            if nextBoard[new[0]][new[1] - 1] == np and nextBoard[new[0]][new[1] - 2] == p or nextBoard[new[0]][new[1] - 2] == 'e':
                nextBoard[new[0]][new[1] - 1] = ' '
        except:
            pass

    return nextBoard


def getAllNextBoards(board, p):
    moves = getAllPossibleMoves(board, p)
    boards = []
    for move in moves:
        boards.append(getNextBoard(board, move))
    return boards


def checkGameEnd(boards, max_moves = 80):
    p = 'w' if len(boards) % 2 == 0 else 'b'
    np = 'b' if p == 'w' else 'w'

    if len(boards) > 4 and boards[-1] == boards[-5] or len(boards) >= max_moves:
        return 'draw'
    
    if len(getAllPossibleMoves(boards[-1], np)) == 0:
        return np
    
    if boards[-1][0][0] == 'K' or \
        boards[-1][8][0] == 'K' or \
        boards[-1][0][8] == 'K' or \
        boards[-1][8][8] == 'K':
        return 'w'

    return 'in progress'


def printBoard(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=' ')
        print()