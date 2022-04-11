from PyQt5.QtWidgets import *


class TetrisCell(QLabel):
    BASE_CELL_STYLE = "border: 0.5px solid black;" \
                      "border-radius: 1;" \
                      "background-color: white;"

    def __init__(self, color='white'):
        super(TetrisCell, self).__init__()
        self.color = color
        self.setText(' ')
        self.setMinimumSize(30, 30)
        self.setStyleSheet("border: 0.5px solid black;"
                           "background-color: " + color + ';')

    def figure_style(self, color):
        self.color = color
        label = TetrisCell()
        label.setStyleSheet("border: 0.5px solid black;"
                            "background-color: " + color + ';')
        return label
