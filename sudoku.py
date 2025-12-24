import random
import copy

def printBoard(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=' ')
            if (j + 1) % 3 == 0 and j != 8:
                print('|', end=' ')
        print()
        if (i + 1) % 3 == 0 and i != 8:
            print("----------------------")

def isValid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
        if board[i][col] == num and i != row:
            return False

    boxRow = (row // 3) * 3
    boxCol = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[boxRow + i][boxCol + j] == num and (boxRow+i, boxCol+j) != (row, col):
                return False
    return True

def findEmptyCell(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def solve(board):
    empty = findEmptyCell(board)
    if not empty:
        return True
    row, col = empty

    nums = list(range(1, 10))
    random.shuffle(nums)

    for n in nums:
        if isValid(board, row, col, n):
            board[row][col] = n
            if solve(board):
                return True
            board[row][col] = 0

    return False

def copyBoard(board):
    return copy.deepcopy(board)

def countSolutions(board):
    empty = findEmptyCell(board)
    if not empty:
        return 1
    r, c = empty

    count = 0
    for n in range(1, 10):
        if isValid(board, r, c, n):
            board[r][c] = n
            count += countSolutions(board)
            if count > 1:
                board[r][c] = 0
                return count
            board[r][c] = 0

    return count

def generatePuzzle(board, difficulty):
    solve(board)

    if difficulty == "easy":
        remove = 35
    elif difficulty == "medium":
        remove = 40
    elif difficulty == "hard":
        remove = 50
    else:
        remove = 35

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    removed = 0
    for r, c in cells:
        temp = board[r][c]
        board[r][c] = 0

        if countSolutions(copyBoard(board)) == 1:
            removed += 1
        else:
            board[r][c] = temp

        if removed >= remove:
            break

    fixed = [[board[r][c] != 0 for c in range(9)] for r in range(9)]

    return board, fixed

def checkMistakes(board):
    mistakes = [[False] * 9 for _ in range(9)]

    for r in range(9):
        for c in range(9):
            num = board[r][c]
            if num != 0:
                board[r][c] = 0
                if not isValid(board, r, c, num):
                    mistakes[r][c] = True
                board[r][c] = num

    return mistakes