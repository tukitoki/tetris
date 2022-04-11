import random
import copy


class Figure:

    def __init__(self, coordinates=[], rotatable=True, color=None):
        self.coordinates = coordinates
        self.rotatable = rotatable
        self.color = color
        self.max_row = self.max_col = -100
        self.min_row = self.min_col = 100
        self.set_max_col_min_col_max_row_min_row()

    @property
    def get_width(self):
        return self.max_col - self.min_col

    @property
    def get_height(self):
        return self.max_row - self.min_row

    def set_max_col_min_col_max_row_min_row(self):
        for (row, col) in self.coordinates:
            if row > self.max_row:
                self.max_row = row
            if row < self.min_row:
                self.min_row = row
            if col > self.max_col:
                self.max_col = col
            if col < self.min_col:
                self.min_col = col

    def __copy__(self):
        return copy.deepcopy(self)

    def rotate(self, clockwise):

        if not self.rotatable:
            return

        new_coords = []

        for (row, col) in self.coordinates:
            if clockwise:
                row, col = col, -row
            else:
                row, col = -col, row
            new_coords.append((row, col))
        self.coordinates = new_coords


class FigureTypes:

    def __init__(self, figures):
        self.figures = figures

    @property
    def get_figure(self):
        return self.figures[(random.randint(0, 6))]

    def get_ss(self):
        return self.figures[3]