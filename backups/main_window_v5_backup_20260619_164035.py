from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QComboBox
)

from event_bus import EventBus
from system_state import SystemState

from dashboard_home import DashboardHome
from students_page import StudentsPage
from teachers_module import TeachersModule
from academics_page import AcademicsPage
from exams import ExamsWindow
from results_center import ResultsCenter
from school_center import SchoolCenter
from settings_page import SettingsPage
from security_settings import SecuritySettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SRMS V5")
        self.resize(1400, 850)

        root = QWidget()
        self.setCentralWidget(root)

        self.main_layout = QVBoxLayout(root)

        # =====================================
        # TOP BAR
        # =====================================

        top_bar = QHBoxLayout()

        self.title = QLabel("SRMS V5")
        self.title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.level_switch = QComboBox()
        self.level_switch.addItems([
            "O_LEVEL",
            "A_LEVEL"
        ])

        self.level_switch.setCurrentText(
            SystemState.get_level()
        )

        self.level_switch.currentTextChanged.connect(
            self.change_level
        )

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(
            self.refresh_all
        )

        top_bar.addWidget(self.title)
        top_bar.addStretch()
        top_bar.addWidget(QLabel("Level"))
        top_bar.addWidget(self.level_switch)
        top_bar.addWidget(self.refresh_btn)

        # =====================================
        # BODY
        # =====================================

        body = QHBoxLayout()

        # =====================================
        # SIDEBAR
        # =====================================

        sidebar = QVBoxLayout()

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_students = QPushButton("Students")
        self.btn_teachers = QPushButton("Teachers")
        self.btn_academics = QPushButton("Academics")
        self.btn_exams = QPushButton("Exams")
        self.btn_results = QPushButton("Results Center")
        self.btn_school = QPushButton("School Center")
        self.btn_settings = QPushButton("Settings")

        self.btn_security = QPushButton("Security")

        self.btn_dashboard.setIcon(
            QIcon("assets/icons/dashboard.svg")
        )

        self.btn_students.setIcon(
            QIcon("assets/icons/students.svg")
        )

        self.btn_teachers.setIcon(
            QIcon("assets/icons/teachers.svg")
        )

        self.btn_academics.setIcon(
            QIcon("assets/icons/academics.svg")
        )

        self.btn_exams.setIcon(
            QIcon("assets/icons/exams.svg")
        )

        self.btn_results.setIcon(
            QIcon("assets/icons/results.svg")
        )

        self.btn_school.setIcon(
            QIcon("assets/icons/school.svg")
        )

        self.btn_settings.setIcon(
            QIcon("assets/icons/settings.svg")
        )

        self.btn_security.setIcon(
            QIcon("assets/icons/security.svg")
        )


        self.nav_buttons = [
            self.btn_dashboard,
            self.btn_students,
            self.btn_teachers,
            self.btn_academics,
            self.btn_exams,
            self.btn_results,
            self.btn_school,
            self.btn_settings,
            self.btn_security
        ]

        for btn in self.nav_buttons:
            sidebar.addWidget(btn)

        sidebar.addStretch()

        # =====================================
        # STACK
        # =====================================

        self.stack = QStackedWidget()

        self.dashboard = DashboardHome()
        self.students = StudentsPage()
        self.teachers = TeachersModule()
        self.academics = AcademicsPage()
        self.exams = ExamsWindow()
        self.results = ResultsCenter()
        self.school = SchoolCenter()
        self.settings = SettingsPage()
        self.security = SecuritySettingsPage()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.students)
        self.stack.addWidget(self.teachers)
        self.stack.addWidget(self.academics)
        self.stack.addWidget(self.exams)
        self.stack.addWidget(self.results)
        self.stack.addWidget(self.school)
        self.stack.addWidget(self.settings)
        self.stack.addWidget(self.security)

        # =====================================
        # NAVIGATION
        # =====================================

        self.btn_dashboard.clicked.connect(
            lambda: self.switch_page(
                self.dashboard,
                self.btn_dashboard
            )
        )

        self.btn_students.clicked.connect(
            lambda: self.switch_page(
                self.students,
                self.btn_students
            )
        )

        self.btn_teachers.clicked.connect(
            lambda: self.switch_page(
                self.teachers,
                self.btn_teachers
            )
        )

        self.btn_academics.clicked.connect(
            lambda: self.switch_page(
                self.academics,
                self.btn_academics
            )
        )

        self.btn_exams.clicked.connect(
            lambda: self.switch_page(
                self.exams,
                self.btn_exams
            )
        )

        self.btn_results.clicked.connect(
            lambda: self.switch_page(
                self.results,
                self.btn_results
            )
        )

        self.btn_school.clicked.connect(
            lambda: self.switch_page(
                self.school,
                self.btn_school
            )
        )

        self.btn_settings.clicked.connect(
            lambda: self.switch_page(
                self.settings,
                self.btn_settings
            )
        )

        self.btn_security.clicked.connect(
            lambda: self.switch_page(
                self.security,
                self.btn_security
            )
        )

        body.addLayout(sidebar, 1)
        body.addWidget(self.stack, 6)

        self.main_layout.addLayout(top_bar)
        self.main_layout.addLayout(body)

        # =====================================
        # EVENTS
        # =====================================

        EventBus.subscribe(
            "OPEN_RESULTS_ENTRY",
            self.open_results_entry
        )

        # =====================================
        # DEFAULT PAGE
        # =====================================

        self.switch_page(
            self.dashboard,
            self.btn_dashboard
        )

        self.refresh_all()

    # =====================================
    # NAVIGATION
    # =====================================

    def switch_page(
        self,
        page,
        button
    ):
        self.stack.setCurrentWidget(page)
        self.update_highlight(button)

    def update_highlight(
        self,
        active_btn
    ):
        active_style = """
            background-color:#10b981;
            color:white;
            font-weight:bold;
            border-left:4px solid #34d399;
        """

        for btn in self.nav_buttons:

            if btn == active_btn:
                btn.setStyleSheet(
                    active_style
                )
            else:
                btn.setStyleSheet("")

    # =====================================
    # LEVEL SWITCH
    # =====================================

    def change_level(
        self,
        value
    ):
        SystemState.set_level(value)

    # =====================================
    # RESULTS DASHBOARD OPEN
    # =====================================

    def open_results_entry(
        self,
        exam_id,
        class_name,
        subject_name
    ):

        self.switch_page(
            self.results,
            self.btn_results
        )

        try:
            self.results.open_from_dashboard(
                exam_id,
                class_name,
                subject_name
            )
        except Exception as error:
            print(
                "MainWindow error:",
                error
            )

    # =====================================
    # REFRESH
    # =====================================

    def refresh_all(self):

        for page in [
            self.dashboard,
            self.students,
            self.teachers,
            self.academics,
            self.exams,
            self.results,
            self.school,
            self.settings,
            self.security
        ]:

            self._refresh_page(page)

    @staticmethod
    def _refresh_page(page):

        for method_name in (
            "refresh_all",
            "load_data",
            "load",
            "load_years"
        ):

            method = getattr(
                page,
                method_name,
                None
            )

            if callable(method):

                try:
                    method()
                except Exception as error:
                    print(error)

                break
