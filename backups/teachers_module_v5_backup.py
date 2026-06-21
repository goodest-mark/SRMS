from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget
)

from teachers_list_page import TeachersListPage
from teacher_profile_page import TeacherProfilePage
from assign_subjects_page import AssignSubjectsPage
from assign_classes_page import AssignClassesPage


class TeachersModule(QWidget):

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)

        self.stack = QStackedWidget()

        self.list_page = TeachersListPage()
        self.profile_page = TeacherProfilePage()
        self.subjects_page = AssignSubjectsPage()
        self.classes_page = AssignClassesPage()

        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.profile_page)
        self.stack.addWidget(self.subjects_page)
        self.stack.addWidget(self.classes_page)

        root.addWidget(self.stack)

        # =====================================
        # LIST → PROFILE
        # =====================================

        self.list_page.table.doubleClicked.connect(
            self.open_profile
        )

        # =====================================
        # PROFILE → LIST
        # =====================================

        self.profile_page.back_btn.clicked.connect(
            self.show_list
        )

        # =====================================
        # ADD BUTTONS INSIDE PROFILE
        # =====================================

        try:

            self.profile_page.assign_subjects_btn.clicked.connect(
                self.open_subjects
            )

            self.profile_page.assign_classes_btn.clicked.connect(
                self.open_classes
            )

        except AttributeError:
            pass

    # =====================================
    # PROFILE
    # =====================================

    def open_profile(self):

        row = self.list_page.table.currentRow()

        if row < 0:
            return

        teacher_id = int(
            self.list_page.table.item(
                row,
                0
            ).text()
        )

        self.profile_page.load_teacher(
            teacher_id
        )

        self.stack.setCurrentWidget(
            self.profile_page
        )

    # =====================================
    # SUBJECTS
    # =====================================

    def open_subjects(self):

        teacher_id = self.profile_page.teacher_id

        if not teacher_id:
            return

        self.subjects_page.set_teacher(
            teacher_id
        )

        self.stack.setCurrentWidget(
            self.subjects_page
        )

    # =====================================
    # CLASSES
    # =====================================

    def open_classes(self):

        teacher_id = self.profile_page.teacher_id

        if not teacher_id:
            return

        self.classes_page.set_teacher(
            teacher_id
        )

        self.stack.setCurrentWidget(
            self.classes_page
        )

    # =====================================
    # BACK TO LIST
    # =====================================

    def show_list(self):

        self.list_page.load()

        self.stack.setCurrentWidget(
            self.list_page
        )

    # =====================================
    # LOAD
    # =====================================

    def load(self):

        try:
            self.list_page.load()
        except:
            pass
