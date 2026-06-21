from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget
)

from teachers_list_page import TeachersListPage
from teacher_profile_page import TeacherProfilePage


class TeachersModule(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.stack = QStackedWidget()

        self.list_page = TeachersListPage()
        self.profile_page = TeacherProfilePage()

        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.profile_page)

        layout.addWidget(self.stack)

        # =====================================
        # EVENTS
        # =====================================

        self.list_page.table.doubleClicked.connect(
            self.open_profile
        )

        self.profile_page.back_btn.clicked.connect(
            self.show_list
        )

    # =====================================
    # OPEN PROFILE
    # =====================================

    def open_profile(self):

        row = self.list_page.table.currentRow()

        if row < 0:
            return

        teacher_id = int(
            self.list_page.table.item(row, 0).text()
        )

        self.profile_page.load_teacher(
            teacher_id
        )

        self.stack.setCurrentWidget(
            self.profile_page
        )

    # =====================================
    # BACK
    # =====================================

    def show_list(self):

        self.stack.setCurrentWidget(
            self.list_page
        )

        self.list_page.load()
