
class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []
        self.figure_center = None
        self.figure = None
        for i in range(rows):
            self.board.insert(0, [0] * columns)

    def spawn_figure(self, figure):
        board_col = self.columns
        board_row = 0
        fig_row = (-figure.min_row) + board_row
        fig_col = int((board_col - figure.get_width) / 2) + (-figure.min_col)
        if (board_col - figure.get_width) / 2 == 0:
            fig_col -= 1
        figure_center = fig_row, fig_col
        if self.figure_collision(figure, figure_center):
            return False

        self.figure_center = figure_center
        self.figure = figure
        return True

    def reset_board(self, board):
        self.board = board
        self.figure = None
        self.figure_center = None

    def move_figure(self, offset):
        if not self.figure_center:
            return False

        new_row = self.figure_center[0] + offset[0]
        new_col = self.figure_center[1] + offset[1]

        if self.figure_collision(self.figure, (new_row, new_col)):
            return False

        self.figure_center = new_row, new_col
        return True

    def move_figure_right(self):
        return self.move_figure((0, 1))

    def move_figure_left(self):
        return self.move_figure((0, -1))

    def move_figure_down(self):
        return self.move_figure((1, 0))

    def move_figure_rotate(self, clockwise):
        figure = self.figure.__copy__()
        figure.rotate(clockwise)

        if self.figure_collision(figure, self.figure_center):
            return False
        self.figure = figure
        return True

    def is_row_complete(self, row):
        for col in range(self.columns):
            if self.board[row][col] == 0:
                return False
        return True

    def remove_finished_row(self, finished_row):
        del self.board[finished_row]
        self.board.insert(0, [0] * self.columns)

    def if_figure_can_move_down(self):
        row, col = self.figure_center[0] + 1, self.figure_center[1]
        return not self.figure_collision(self.figure, (row, col))

    def finish_fall(self):
        finished_rows = []

        for row, col in self.figure.coordinates:
            self.board[row + self.figure_center[0]][col + self.figure_center[1]] = 1
        for row in range(self.rows):
            if self.is_row_complete(row):
                finished_rows.append(row)
        for finished_row in finished_rows:
            self.remove_finished_row(finished_row)

        self.figure = None
        self.figure_center = None
        return finished_rows

    def figure_collision(self, figure, figure_center):
        for (row, col) in figure.coordinates:
            check_row, check_col = figure_center[0] + row, figure_center[1] + col
            if 0 > check_col or check_col >= self.columns:
                return True
            if 0 > check_row or check_row >= self.rows:
                return True
            if self.board[check_row][check_col] == 1:
                return True
            if self.board[check_row][check_col] == 1:
                return True
        return False





