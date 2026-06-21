import sys
from PySide6.QtWidgets import QApplication

from splash import SplashScreen
from main_window import MainWindow
from database import init_db
from theme import APP_STYLE


def start_app():

    init_db()

    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    def show_main():

        global window
        window = MainWindow()
        window.show()

    splash = SplashScreen(on_finish=show_main)
    splash.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    start_app()