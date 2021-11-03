# The code has been been created for a 9x9 sudoku puzzle

sample = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


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


show_sudoku(sample)
solve(sample)
print("\n")
show_sudoku(sample)
