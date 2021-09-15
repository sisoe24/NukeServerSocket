"""Fake emulation of the internal nuke script editor layout/widgets."""
# coding: utf-8
from __future__ import print_function

import sys
import random
import subprocess


from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence, QKeyEvent

from PySide2.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
    QSplitter,
    QTextEdit,
    QPushButton,
    QApplication, QMainWindow
)


class OutputEditor(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)


class InputEditor(QPlainTextEdit):
    def __init__(self):
        QPlainTextEdit.__init__(self)
        r = random.randint(1, 50)
        self.setPlainText("print('Hello From Internal SE %s')" % r)


class FakeScriptEditor(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('uk.co.thefoundry.scripteditor.1')

        self.run_btn = QPushButton('Run')
        self.run_btn.setToolTip('Run the current')
        self.run_btn.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return))
        self.run_btn.clicked.connect(self.run_code)

        self.input_console = InputEditor()

        self.output_console = OutputEditor()

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.output_console)
        self.splitter.addWidget(self.input_console)

        _layout = QVBoxLayout()
        _layout.addWidget(self.run_btn)
        _layout.addWidget(self.splitter)
        self.setLayout(_layout)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if isinstance(event, QKeyEvent):
            if event.modifiers() == Qt.CTRL and event.key() == Qt.Key_Return:
                print('shortcut pressed')
                self.run_code()
                event.accept()
                return True
        return super(FakeScriptEditor, self).eventFilter(obj, event)

    def run_code(self):
        code = self.input_console.toPlainText()
        call = subprocess.check_output(['python', '-c', code])
        self.output_console.setPlainText(call)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.script_editor = FakeScriptEditor()
        self.setCentralWidget(self.script_editor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.script_editor.run_btn.click()
    app.exec_()
