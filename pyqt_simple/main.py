#!/usr/bin/env python3
"""Simple PyQt5 application

Run: python main.py
"""
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple PyQt5 App")
        self.counter = 0

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        self.label = QLabel("Click the button:")
        layout.addWidget(self.label)

        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type something and press Enter")
        self.input.returnPressed.connect(self.on_enter)
        layout.addWidget(self.input)

    def on_click(self):
        self.counter += 1
        self.label.setText(f"Clicked {self.counter} times")

    def on_enter(self):
        text = self.input.text().strip()
        if text:
            QMessageBox.information(self, "Input received", f"You entered: {text}")
            self.input.clear()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
