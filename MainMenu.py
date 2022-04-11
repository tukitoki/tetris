from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from AboutWindow import AboutWindow


class MainMenu:

    _BUTTONS_STYLE = "QPushButton {" \
                    "border-radius: 10;" \
                    "border : 1px solid black;" \
                    "font-family: Arial;" \
                    "font-size: 20px;" \
                    "color: black;" \
                    "background-color: #aa93fa;}" \
                    "QPushButton:hover {background-color: #9984e1;}" \
                    "QPushButton:pressed {background-color: #d4c9fc;}"

    def __init__(self):
        self.grid_layout = QGridLayout()
        self.board_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self._init_info_dialog()

    def init_main_layout(self):
        tetris_name = QLabel('T E T R I S')
        tetris_name.setMinimumSize(150, 50)
        tetris_name.setAlignment(Qt.AlignCenter)
        tetris_name.setStyleSheet("border-radius: 0;"
                                  "font-family: Сomic Sans MS;"
                                  "color: #9984e1;"
                                  "font-size: 30px;"
                                  )
        self.play_button = self._create_button(100, 50, 'Play', self._BUTTONS_STYLE)
        info_button = self._create_button(100, 50, 'Info', self._BUTTONS_STYLE)
        info_button.clicked.connect(self._show_info_action)
        self.quit_button = self._create_button(100, 50, 'Quit', self._BUTTONS_STYLE)
        self.grid_layout.addWidget(tetris_name, 0, 1)
        label = QLabel(" ")
        label1 = QLabel(" ")
        label.setFixedSize(50, 50)
        label1.setFixedSize(50, 50)
        self.grid_layout.addWidget(label, 0, 0)
        self.grid_layout.addWidget(label1, 0, 2)
        self.grid_layout.addWidget(self.play_button, 1, 1)
        self.grid_layout.addWidget(info_button, 2, 1)
        self.grid_layout.addWidget(self.quit_button, 3, 1)

    def init_escape_layout(self):
        escape_layout = QGridLayout()
        tetris_name = QLabel('T E T R I S')
        tetris_name.setMinimumSize(150, 50)
        tetris_name.setAlignment(Qt.AlignCenter)
        tetris_name.setStyleSheet("border-radius: 0;"
                                  "font-family: Сomic Sans MS;"
                                  "color: #9984e1;"
                                  "font-size: 30px;"
                                  )
        self.continue_button = self._create_button(100, 50, 'Continue', self._BUTTONS_STYLE)
        self.restart_button = self._create_button(100, 50, 'Restart', self._BUTTONS_STYLE)
        info_button = self._create_button(100, 50, 'Info', self._BUTTONS_STYLE)
        info_button.clicked.connect(self._show_info_action)
        self.menu_button = self._create_button(100, 50, 'Menu', self._BUTTONS_STYLE)
        label = QLabel(" ")
        label1 = QLabel(" ")
        label.setFixedSize(50, 50)
        label1.setFixedSize(50, 50)
        escape_layout.addWidget(tetris_name, 0, 1)
        escape_layout.addWidget(label, 0, 0)
        escape_layout.addWidget(label1, 0, 2)
        escape_layout.addWidget(self.continue_button, 1, 1)
        escape_layout.addWidget(self.restart_button, 2, 1)
        escape_layout.addWidget(info_button, 3, 1)
        escape_layout.addWidget(self.menu_button, 4, 1)
        return escape_layout

    def _init_info_dialog(self):
        self._dialog = QtWidgets.QDialog()
        ui = AboutWindow(self._dialog)

    def _show_info_action(self):
        self._dialog.show()

    @staticmethod
    def _create_button(min_width, min_height, button_name, style):
        button = QPushButton(button_name)
        button.setStyleSheet(style)
        button.setMinimumSize(min_width, min_height)
        return button
