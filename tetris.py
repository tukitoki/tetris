import copy

from board import *
from gamestate import *


class Tetris:
    _game_state = GameState

    def __init__(self, board=Board(20, 10)):
        self._board = board
        self._score = 0
        self._lines = 0
        self._level = 0

    def restart(self):
        self._board = Board(20, 10)
        self._score = 0
        self._lines = 0
        self._level = 0
        self._board.spawn_figure(self.figures_array().get_figure)
        self._game_state = GameState.RUNNING

    def pause(self):
        self._game_state = GameState.PAUSE

    def continue_game(self):
        self._game_state = GameState.RUNNING

    def score_update(self, finished_rows, old_level):
        self._lines += len(finished_rows)
        if len(finished_rows) == 1:
            self._score += 100
        elif len(finished_rows) == 2:
            self._score += 300
        elif len(finished_rows) == 3:
            self._score += 700
        elif len(finished_rows) == 4:
            self._score += 1200
        if self._lines >= 1 and self._level == 0:
            self._level += 1
        elif self._lines % 10 == 0 and self._level != 0:
            self._level += 1

    @property
    def board(self) -> Board:
        return self._board

    @property
    def score(self) -> int:
        return self._score

    @property
    def level(self) -> int:
        return self._level

    @property
    def lines(self) -> int:
        return self._lines

    @property
    def game_state(self) -> GameState:
        return self._game_state

    def set_game_state(self, game_state):
        self._game_state = game_state

    def set_tetris_score(self, score):
        self._score += score

    @staticmethod
    def figures_array():
        #  oo
        # oO
        S = Figure([(0, 0), (-1, 0), (0, -1), (-1, 1)], color='#32e82e')

        # oo
        #  Oo
        Z = Figure([(0, 0), (0, 1), (-1, -1), (-1, 0)], color='#f20a0a')

        # oOo
        #  o
        T = Figure([(0, 0), (0, 1), (0, -1), (1, 0)], color='#b72ee8')

        # oOoo
        #
        I = Figure([(0, 0), (0, -1), (0, 1), (0, 2)], color='#2edce8')

        # oo
        # Oo
        O = Figure([(0, 0), (-1, 0), (-1, -1), (0, -1)], rotatable=False, color='#e5e82e')

        # oOo
        # o
        L = Figure([(0, 0), (0, -1), (0, 1), (1, -1)], color='#e8aa2e')

        # oOo
        #   o
        J = Figure([(0, 0), (0, -1), (0, 1), (1, 1)], color='#2e35e8')

        return FigureTypes([S, Z, T, I, O, L, J])