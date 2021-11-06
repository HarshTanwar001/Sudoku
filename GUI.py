import pygame
from sudoku import create_board, empty_space, solve, valid_num
import time
pygame.font.init()


class Grid:
    board = create_board()

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def matrix(self):
        return self.board

    def update_matrix(self, val, i, j):
        self.board[i][j] = val

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid_num(self.model, val, [row, col]) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)

        return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), True, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), True, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time_taken):
    win.fill((255, 255, 255))

    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)

    text = fnt.render("Time -> " + format_time(time_taken), True, (0, 0, 0))
    win.blit(text, (0, 550))

    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = str(hour) + ":" + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540, 620))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    required = True
    start = time.time()

    while run:
        if required:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    required = False
                    while not board.is_finished():
                        row, col = empty_space(board.matrix())

                        for num in range(1, 10):
                            if valid_num(board.matrix(), num, [row, col]):
                                key = num
                                board.select(row, col)
                                board.sketch(key)

                                i, j = board.selected
                                if board.cubes[i][j].temp != 0:
                                    if board.place(board.cubes[i][j].temp):
                                        board.update_matrix(num, row, col)

                if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    i, j = board.selected

                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            board.update_matrix(board.cubes[i][j].temp, i, j)
                            print("Correct")
                        else:
                            print("Wrong")
                        key = None

                        if board.is_finished():
                            print("\nGame over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)

                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board, play_time)
        pygame.display.update()


print()
main()
pygame.quit()
