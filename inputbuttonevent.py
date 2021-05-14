import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Set Name")
        self.init_ui()
        self.counter = 0

    def init_ui(self):
        self.text_label = QLabel("There has been no name entered. so I can't do anything")
        label = QLabel("Name: ")
        self.name_input = QLineEdit()

        hlayout = QHBoxLayout()
        #hlayout.addStretch(1)

        hlayout.addWidget(label)
        hlayout.addWidget(self.name_input)

        vlayout =QVBoxLayout()
        #vlayout.addStretch(1)
        vlayout.addWidget(self.text_label)
        vlayout.addLayout(hlayout)

        self.button.clicked.connect(self.alterName)


        vlayout.addWidget(self.button)


        self.setLayout(vlayout)
        self.setWindowTitle("Horizontal Layout")
        self.show()

    def alterName(self):
        inputted_text = self.name_input.text()
        our_string = "You've entered " + inputted_text
        self.text_label.setText(our_string)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    sys.exit(app.exec_())
