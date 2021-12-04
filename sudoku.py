# The code has been been created for a 9x9 sudoku puzzle
import random


def create_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for _ in range(random.randint(6, 8)):
        i = random.randint(0, 8)
        j = random.randint(0, 8)

        board[i][j] = random.choice(values)
        values.remove(board[i][j])

    solve(board)
    data_dict = {key: [0, 1, 2, 3, 4, 5, 6, 7, 8] for key in range(9)}

    for _ in range(random.randint(30, 54)):
        i = random.randint(0, 8)

        if len(data_dict[i]) == 0:
            continue

        j = random.choice(data_dict[i])

        board[i][j] = 0
        data_dict[i].remove(j)

    return board


def show_sudoku(matrix):
    for i in range(len(matrix)):
        if i != 0 and i % 3 == 0:
            print("-------------------------")

        for j in range(len(matrix[0])):
            if j != 0 and j % 3 == 0:
                print(" | ", end="")

            if j == 8:
                print(matrix[i][j])
            else:
                print(str(matrix[i][j]) + " ", end="")


def empty_space(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                return [i, j]

    return None


def valid_num(matrix, num, pos):
    # Check in row
    for i in range(len(matrix[0])):
        if pos[1] != i and matrix[pos[0]][i] == num:
            return False

    # Check in column
    for j in range(len(matrix)):
        if pos[0] != j and matrix[j][pos[1]] == num:
            return False

    # Check in box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, (box_y * 3) + 3):
        for j in range(box_x * 3, (box_x * 3) + 3):
            if [i, j] != pos and matrix[i][j] == num:
                return False

    return True


def solve(matrix):
    if not empty_space(matrix):
        return True

    row, col = empty_space(matrix)

    for num in range(1, 10):
        if valid_num(matrix, num, [row, col]):
            matrix[row][col] = num

            if solve(matrix):
                return True

        matrix[row][col] = 0

    return False


# sample = create_board()

# print("\nUnsolved Sudoku(sudoku.py) :\n")
# show_sudoku(sample)
# print("\n\nSolved Sudoku(sudoku.py) :\n")
# solve(sample)
# show_sudoku(sample)
