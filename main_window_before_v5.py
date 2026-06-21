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

from students_page import StudentsPage
from teachers_module import TeachersModule
from subjects_page import SubjectsPage
from enrollment_page import EnrollmentPage
from requirements_page import RequirementsPage
from broadsheet_page import BroadsheetPage
from report_book_page import ReportBookPage
from results_dashboard import ResultsDashboard
from results_page import ResultsPage
from ranking import RankingPage
from academic_years import AcademicYearsPage
from terms_page import TermsPage
from exams import ExamsWindow
from school_profile import SchoolProfilePage
from settings_page import SettingsPage
from security_settings import SecuritySettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SRMS V5")
        self.resize(1300, 800)

        root = QWidget()
        self.setCentralWidget(root)

        self.main_layout = QVBoxLayout()
        root.setLayout(self.main_layout)

        # =====================================
        # TOP BAR
        # =====================================

        top_bar = QHBoxLayout()

        self.title = QLabel("SRMS V5 SYSTEM")

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

        self.refresh_btn = QPushButton("REFRESH")
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

        sidebar = QVBoxLayout()

        self.btn_students = QPushButton("Students")
        self.btn_subjects = QPushButton("Subjects")
        self.btn_enrollment = QPushButton("Subject Enrollment")
        self.btn_school_profile = QPushButton("School Profile")
        self.btn_settings = QPushButton("System Settings")
        self.btn_security = QPushButton("Security")
        self.btn_requirements = QPushButton("Requirements")
        self.btn_broadsheet = QPushButton("Broadsheet")
        self.btn_report_book = QPushButton("Report Book")
        self.btn_years = QPushButton("Academic Years")
        self.btn_terms = QPushButton("Terms")
        self.btn_exams = QPushButton("Exams")
        self.btn_results_dashboard = QPushButton(
            "Results Dashboard"
        )
        self.btn_results = QPushButton("Results Entry")
        self.btn_ranking = QPushButton("Ranking")

        self.nav_buttons = [
            self.btn_students,
            self.btn_subjects,
            self.btn_enrollment,
            self.btn_school_profile,
            self.btn_settings,
            self.btn_security,
            self.btn_requirements,
            self.btn_broadsheet,
            self.btn_report_book,
            self.btn_years,
            self.btn_terms,
            self.btn_exams,
            self.btn_results_dashboard,
            self.btn_results,
            self.btn_ranking
        ]

        for btn in self.nav_buttons:
            sidebar.addWidget(btn)

        sidebar.addStretch()

        # =====================================
        # STACK
        # =====================================

        self.stack = QStackedWidget()

        self.students = StudentsPage()
        self.subjects = SubjectsPage()
        self.enrollment = EnrollmentPage()
        self.school_profile = SchoolProfilePage()
        self.settings = SettingsPage()
        self.security = SecuritySettingsPage()
        self.requirements = RequirementsPage()
        self.broadsheet = BroadsheetPage()
        self.report_book = ReportBookPage()
        self.years = AcademicYearsPage()
        self.terms = TermsPage()
        self.exams = ExamsWindow()
        self.results_dashboard = ResultsDashboard()
        self.results = ResultsPage()
        self.ranking = RankingPage()

        self.stack.addWidget(self.students)
        self.stack.addWidget(self.subjects)
        self.stack.addWidget(self.enrollment)
        self.stack.addWidget(self.school_profile)
        self.stack.addWidget(self.settings)
        self.stack.addWidget(self.security)
        self.stack.addWidget(self.requirements)
        self.stack.addWidget(self.broadsheet)
        self.stack.addWidget(self.report_book)
        self.stack.addWidget(self.years)
        self.stack.addWidget(self.terms)
        self.stack.addWidget(self.exams)
        self.stack.addWidget(self.results_dashboard)
        self.stack.addWidget(self.results)
        self.stack.addWidget(self.ranking)

        # =====================================
        # NAVIGATION
        # =====================================

        self.btn_students.clicked.connect(
            lambda: self.switch_page(self.students, self.btn_students)
        )

        self.btn_subjects.clicked.connect(
            lambda: self.switch_page(self.subjects, self.btn_subjects)
        )

        self.btn_enrollment.clicked.connect(
            lambda: self.switch_page(self.enrollment, self.btn_enrollment)
        )

        self.btn_school_profile.clicked.connect(
            lambda: self.switch_page(self.school_profile, self.btn_school_profile)
        )

        self.btn_settings.clicked.connect(
            lambda: self.switch_page(self.settings, self.btn_settings)
        )

        self.btn_security.clicked.connect(
            lambda: self.switch_page(self.security, self.btn_security)
        )

        self.btn_requirements.clicked.connect(
            lambda: self.switch_page(self.requirements, self.btn_requirements)
        )

        self.btn_broadsheet.clicked.connect(
            lambda: self.switch_page(self.broadsheet, self.btn_broadsheet)
        )

        self.btn_report_book.clicked.connect(
            lambda: self.switch_page(self.report_book, self.btn_report_book)
        )

        self.btn_years.clicked.connect(
            lambda: self.switch_page(self.years, self.btn_years)
        )

        self.btn_terms.clicked.connect(
            lambda: self.switch_page(self.terms, self.btn_terms)
        )

        self.btn_exams.clicked.connect(
            lambda: self.switch_page(self.exams, self.btn_exams)
        )

        self.btn_results_dashboard.clicked.connect(
            lambda: self.switch_page(self.results_dashboard, self.btn_results_dashboard)
        )

        self.btn_results.clicked.connect(
            lambda: self.switch_page(self.results, self.btn_results)
        )

        self.btn_ranking.clicked.connect(
            lambda: self.switch_page(self.ranking, self.btn_ranking)
        )

        body.addLayout(sidebar, 1)
        body.addWidget(self.stack, 5)

        self.main_layout.addLayout(top_bar)
        self.main_layout.addLayout(body)

        # =====================================
        # EVENTS
        # =====================================



        EventBus.subscribe(
            "OPEN_RESULTS_ENTRY",
            self.open_results_entry
        )

        # Initial Page
        self.switch_page(self.students, self.btn_students)
        self.refresh_all()

    # =====================================
    # NAVIGATION HELPERS
    # =====================================

    def switch_page(self, page, button):
        self.stack.setCurrentWidget(page)
        self.update_highlight(button)

    def update_highlight(self, active_btn):
        active_style = (
            "background-color: #10b981; "
            "color: white; "
            "font-weight: bold; "
            "border-left: 5px solid #34d399;"
        )
        
        for btn in self.nav_buttons:
            if btn == active_btn:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet("")

    # =====================================
    # LEVEL SWITCH
    # =====================================

    def change_level(self, value):

        SystemState.set_level(value)

    def open_results_entry(
        self,
        exam_id,
        class_name,
        subject_name
    ):
        self.switch_page(self.results, self.btn_results)
        if hasattr(self, "results"):
            try:
                self.results.open_from_dashboard(exam_id, class_name, subject_name)
            except Exception as error:
                print(f"Failed to open results entry: {error}")

    # =====================================
    # REFRESH
    # =====================================

    def refresh_all(self):

        if hasattr(self, "students"):
            self._refresh_page(self.students)

        if hasattr(self, "subjects"):
            self._refresh_page(self.subjects)

        if hasattr(self, "enrollment"):
            self._refresh_page(self.enrollment)

        if hasattr(self, "school_profile"):
            self._refresh_page(self.school_profile)
            
        if hasattr(self, "settings"):
            self._refresh_page(self.settings)

        if hasattr(self, "security"):
            self._refresh_page(self.security)

        if hasattr(self, "requirements"):
            self._refresh_page(self.requirements)

        if hasattr(self, "broadsheet"):
            self._refresh_page(self.broadsheet)

        if hasattr(self, "report_book"):
            self._refresh_page(self.report_book)

        if hasattr(self, "years"):
            self._refresh_page(self.years)

        if hasattr(self, "terms"):
            self.terms.load_years()
            self._refresh_page(self.terms)

        if hasattr(self, "exams"):
            self._refresh_page(self.exams)

        if hasattr(self, "results_dashboard"):
            self._refresh_page(self.results_dashboard)

        if hasattr(self, "results"):
            self._refresh_page(self.results)

        if hasattr(self, "ranking"):
            self._refresh_page(self.ranking)

    @staticmethod
    def _refresh_page(page):
        for method_name in (
            "refresh_all",
            "load_data",
            "load",
            "load_years"
        ):
            method = getattr(page, method_name, None)

            if callable(method):
                method()
                return
