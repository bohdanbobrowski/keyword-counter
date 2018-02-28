from PyQt5.QtWidgets import (QApplication)
from keyword_counter_lib.keyword_counter_window import KeywordCounterWindow
import sys


def main():
    app = QApplication(sys.argv)
    keyword_counter_window = KeywordCounterWindow()
    keyword_counter_window.show()
    sys.exit(app.exec_())
