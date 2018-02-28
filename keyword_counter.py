from PyQt5.QtWidgets import (QApplication)
from classes.keyword_counter_window import KeywordCounterWindow

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    keyword_counter_window = KeywordCounterWindow()

sys.exit(keyword_counter_window.exec_())