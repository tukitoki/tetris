from PyQt5.Qt import *
from MainMenu import *
from tetris import *
from TetrisCell import TetrisCell


class TetrisMainWindow(QMainWindow):
    WIDTH = 200
    HEIGHT = 600

    def __init__(self, parent=None):
        super(TetrisMainWindow, self).__init__(parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.tetris = Tetris()
        self.menu = MainMenu()
        self.setStyleSheet("QMainWindow {background: #85144b;}")

        self.menu.init_main_layout()
        self.menu.play_button.clicked.connect(self.play_action)

        widget = QWidget()
        widget.setLayout(self.menu.grid_layout)

        menu_widget = QWidget()
        menu_widget.setLayout(self.menu.init_escape_layout())
        self.menu.restart_button.clicked.connect(self.restart_action)
        self.menu.menu_button.clicked.connect(self.menu_exit_action)

        self.msg = self.init_gameover_message()

        self.widgets = QStackedWidget()
        self.widgets.addWidget(widget)
        self.widgets.addWidget(menu_widget)
        self.widgets.setCurrentIndex(0)
        self.setCentralWidget(self.widgets)

        self.timer = QTimer()
        self.timer_interval = 1000
        self.timer.timeout.connect(self.update_timer)
        self.keyPressEvent = self.key_control

        self.show()

    def update_timer(self):
        if self.tetris.game_state == GameState.RUNNING:
            prev_coords = copy.deepcopy(self.tetris.board.figure.coordinates)
            fig_center = copy.deepcopy(self.tetris.board.figure_center)
            figure_state = self.tetris.board.move_figure_down()
            if figure_state:
                self.repaint_after_move_figure(fig_center, prev_coords)
                self.tetris.set_game_state(GameState.RUNNING)
            else:
                finished_rows = self.tetris.board.finish_fall()
                if len(finished_rows) > 0:
                    old_level = self.tetris.level
                    self.tetris.score_update(finished_rows, old_level)
                    if old_level != self.tetris.level:
                        self.timer_interval = 1000 - self.tetris.level * 100
                        if self.timer_interval < 100:
                            self.timer_interval = 100
                    self.repaint_board(finished_rows)
                if self.tetris.board.spawn_figure(self.tetris.figures_array().get_figure):
                    self.draw_figure()
                    self.tetris.set_game_state(GameState.RUNNING)
                else:
                    self.tetris.set_game_state(GameState.GAMEOVER)
                    self.timer.stop()
                    self.display_gameover_message()
                    return
            self.update_score_label()

    def play_action(self):
        self.init_game_layout()
        self.tetris.restart()
        self.draw_figure()
        self.timer_interval = 1000
        self.timer.start(self.timer_interval)

    def continue_action(self):
        self.widgets.setCurrentIndex(2)
        if self.tetris.game_state != GameState.GAMEOVER:
            self.tetris.set_game_state(GameState.RUNNING)
            self.draw_figure()
            self.tetris.continue_game()
            self.timer.start(self.timer_interval)

    def restart_action(self):
        self.tetris.restart()
        self.init_game_layout()
        self.widgets.setCurrentIndex(2)
        self.draw_figure()
        self.tetris.continue_game()
        self.timer.start(self.timer_interval)

    def escape_menu(self):
        if self.tetris.game_state != GameState.GAMEOVER:
            self.tetris.set_game_state(GameState.PAUSE)
        self.widgets.setCurrentIndex(1)
        self.menu.continue_button.clicked.connect(self.continue_action)

    def menu_exit_action(self):
        self.widgets.setCurrentIndex(0)

    def init_game_layout(self):
        self.menu.board_layout = QGridLayout()
        self.main_play_layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(self.main_play_layout)
        self.menu.board_layout.setSpacing(0)
        widget.setStyleSheet("background-color: white;}")

        for row in range(self.tetris.board.rows):
            for col in range(self.tetris.board.columns):
                self.menu.board_layout.addWidget(TetrisCell(), row, col)
        self.score_label = QLabel("Score: " + str(self.tetris.score))
        self.score_label.setStyleSheet("border-radius: 0;"
                                       "font-family: Сomic Sans MS;"
                                       "color: #9984e1;"
                                       "font-size: 30px;")
        self.level_label = QLabel("Level: " + str(self.tetris.level))
        self.level_label.setStyleSheet("border-radius: 0;"
                                       "font-family: Сomic Sans MS;"
                                       "color: #9984e1;"
                                       "font-size: 30px;")
        self.lines_label = QLabel("Lines: " + str(self.tetris.lines))
        self.lines_label.setStyleSheet("border-radius: 0;"
                                       "font-family: Сomic Sans MS;"
                                       "color: #9984e1;"
                                       "font-size: 30px;")
        label1 = QLabel(" ")
        self.score_label.setMinimumSize(50, 50)
        self.lines_label.setMinimumSize(50, 50)
        self.level_label.setMinimumSize(50, 50)
        label1.setMinimumSize(50, 50)
        label1.setMaximumSize(1000, 1000)
        self.main_play_layout.setSpacing(0)
        self.main_play_layout.addWidget(self.score_label, 0, 0)
        self.main_play_layout.addWidget(self.level_label, 1, 0)
        self.main_play_layout.addWidget(self.lines_label, 2, 0)
        # self.main_play_layout.addWidget(label1, 1, 1)
        self.main_play_layout.addLayout(self.menu.board_layout, 3, 0)
        self.widgets.insertWidget(2, widget)
        self.widgets.setCurrentIndex(2)

    def update_score_label(self):
        self.score_label.setText("Score: " + str(self.tetris.score))
        self.level_label.setText("Level: " + str(self.tetris.level))
        self.lines_label.setText("Lines: " + str(self.tetris.lines))

    def draw_figure(self):
        fig_center = self.tetris.board.figure_center
        figure = self.tetris.board.figure
        for row, col in figure.coordinates:
            replaced = self.menu.board_layout.itemAtPosition(row + fig_center[0], col + fig_center[1]).widget()
            self.menu.board_layout.removeWidget(replaced)
            self.menu.board_layout.addWidget(TetrisCell(figure.color),
                                             row + fig_center[0],
                                             col + fig_center[1])

    def repaint_after_move_figure(self, prev_fig_center, prev_coords):
        for row, col in prev_coords:
            replaced = self.menu.board_layout.itemAtPosition(row + prev_fig_center[0],
                                                             col + prev_fig_center[1]).widget()
            self.menu.board_layout.removeWidget(replaced)
            self.menu.board_layout.addWidget(TetrisCell(),
                                             row + prev_fig_center[0],
                                             col + prev_fig_center[1])
        self.draw_figure()

    def repaint_board(self, finished_rows):
        if len(finished_rows) == 0:
            return
        for row in finished_rows:
            for new_row in range(row, 0, -1):
                for new_col in range(self.tetris.board.columns):
                    if self.menu.board_layout.itemAtPosition(new_row, new_col) is not None:
                        replaced = self.menu.board_layout.itemAtPosition(new_row, new_col).widget()
                        self.menu.board_layout.removeWidget(replaced)
                        new_cell_color = self.menu.board_layout.itemAtPosition(new_row - 1, new_col).widget().color
                        self.menu.board_layout.addWidget(TetrisCell(new_cell_color), new_row, new_col)
                    else:
                        self.menu.board_layout.addWidget(TetrisCell(), new_row, new_col)

    def key_control(self, event):
        if event.key() == Qt.Key_Escape:
            self.escape_menu()
            self.timer.stop()
            self.tetris.pause()
            return

        if self.tetris.game_state == GameState.GAMEOVER:
            return

        fig_center = copy.deepcopy(self.tetris.board.figure_center)
        prev_coords = copy.deepcopy(self.tetris.board.figure.coordinates)
        if_successful = False
        if event.key() == Qt.Key_Left:
            if_successful = self.tetris.board.move_figure_left()
        elif event.key() == Qt.Key_Right:
            if_successful = self.tetris.board.move_figure_right()
        elif event.key() == Qt.Key_Down:
            if_successful = self.tetris.board.move_figure_down()
            self.tetris.set_tetris_score(1)
        elif event.key() == Qt.Key_Up:
            if_successful = self.tetris.board.move_figure_rotate(True)
        elif event.key() == Qt.Key_Z:
            if_successful = self.tetris.board.move_figure_rotate(False)
        elif event.key() == Qt.Key_Space:
            while self.tetris.board.move_figure_down():
                self.tetris.set_tetris_score(2)
                if_successful = True
        if if_successful:
            self.repaint_after_move_figure(fig_center, prev_coords)
            self.update_score_label()

    def init_gameover_message(self):
        msg = QMessageBox()
        msg.setFixedSize(200, 200)
        msg.setWindowTitle("Game Over")
        restart_button = msg.addButton('Restart', QMessageBox.YesRole)
        main_button = msg.addButton('Menu', QMessageBox.YesRole)
        restart_button.clicked.connect(self.restart_action)
        main_button.clicked.connect(self.menu_exit_action)
        return msg

    def display_gameover_message(self):
        self.msg.setText("Congrats, your score: " + str(self.tetris.score))
        self.msg.exec_()
