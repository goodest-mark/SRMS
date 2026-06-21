from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QComboBox,
    QSizePolicy
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

        
        self.level_btn = QPushButton()

        current_level = SystemState.get_level()

        if current_level == "A_LEVEL":
            self.level_btn.setText("🎓 A-Level")
        else:
            self.level_btn.setText("🎓 O-Level")

        self.level_btn.clicked.connect(
            self.toggle_level
        )

        self.level_btn.setStyleSheet("""
            QPushButton{
                background:rgba(37,99,235,0.18);
                border:1px solid rgba(59,130,246,0.50);
                border-radius:18px;
                padding:10px 18px;
                color:white;
                font-weight:700;
            }

            QPushButton:hover{
                background:rgba(59,130,246,0.30);
            }
        """)

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon("assets/icons/refresh.svg"))
        self.refresh_btn.setToolTip("Refresh")
        self.refresh_btn.setIconSize(QSize(20,20))
        self.refresh_btn.setFixedSize(42,42)
        self.refresh_btn.setStyleSheet("""
            QPushButton{
                background:rgba(255,255,255,0.08);
                border:none;
                border-radius:12px;
                color:#E2E8F0;
            }
            QPushButton:hover{
                background:rgba(255,255,255,0.16);
            }
        """)
        self.refresh_btn.clicked.connect(
            self.refresh_all
        )

        top_bar.addWidget(self.title)
        top_bar.addStretch()
        top_bar.addWidget(self.level_btn)
        top_bar.addWidget(self.refresh_btn)

        # =====================================
        # BODY
        # =====================================

        body = QHBoxLayout()
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(16)

        # =====================================
        # SIDEBAR
        # =====================================

        
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMinimumWidth(88)
        self.sidebar_widget.setMaximumWidth(240)
        self.sidebar_widget.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.sidebar_widget.setStyleSheet("""
        QWidget{
            background:#0F172A;
            border:1px solid rgba(148,163,184,0.15);
            border-radius:22px;
        }
        """)

        self.sidebar_animation = QPropertyAnimation(
            self.sidebar_widget,
            b"maximumWidth"
        )
        self.sidebar_animation.setDuration(240)
        self.sidebar_animation.setEasingCurve(
            QEasingCurve.InOutQuad
        )

        sidebar = QVBoxLayout(self.sidebar_widget)
        sidebar.setSpacing(10)
        sidebar.setContentsMargins(16,16,16,16)

        self.sidebar_collapsed = False

        self.sidebar_toggle_btn = QPushButton("≡")
        self.sidebar_toggle_btn.setFixedSize(36,36)
        self.sidebar_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.sidebar_toggle_btn.setStyleSheet("""
            QPushButton{
                color:#CBD5E1;
                background:rgba(255,255,255,0.06);
                border:none;
                border-radius:12px;
                font-size:16px;
                font-weight:700;
            }
            QPushButton:hover{
                background:rgba(255,255,255,0.12);
            }
        """)
        self.sidebar_toggle_btn.clicked.connect(self.toggle_sidebar)

        toggle_row = QHBoxLayout()
        toggle_row.addStretch()
        toggle_row.addWidget(self.sidebar_toggle_btn)
        sidebar.addLayout(toggle_row)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_students = QPushButton("Students")
        self.btn_teachers = QPushButton("Teachers")
        self.btn_academics = QPushButton("Academics")
        self.btn_exams = QPushButton("Exams")
        self.btn_results = QPushButton("Results")
        self.btn_school = QPushButton("School")
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

        self.sidebar_button_style = """
            QPushButton{
                text-align:left;
                padding:12px 18px 12px 20px;
                border-radius:16px;
                font-weight:700;
                color:#E2E8F0;
                font-size:14px;
                background:transparent;
                border:none;
            }
            QPushButton:hover{
                background:rgba(255,255,255,0.08);
            }
        """

        self.sidebar_button_style_collapsed = """
            QPushButton{
                padding:12px;
                border-radius:16px;
                font-weight:700;
                color:#E2E8F0;
                font-size:14px;
                background:transparent;
                border:none;
            }
            QPushButton:hover{
                background:rgba(255,255,255,0.08);
            }
        """

        self.sidebar_button_active_style = """
            QPushButton{
                background:qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #2563eb,
                    stop:1 #3b82f6
                );
                color:#ffffff;
                font-weight:700;
                border:none;
                border-radius:16px;
                padding:12px 18px 12px 20px;
                text-align:left;
            }
        """

        self.sidebar_button_active_style_collapsed = """
            QPushButton{
                background:qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 #2563eb,
                    stop:1 #3b82f6
                );
                color:#ffffff;
                font-weight:700;
                border:none;
                border-radius:16px;
                padding:12px;
                text-align:center;
            }
        """

        self.active_btn = None

        for btn in self.nav_buttons:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIconSize(QSize(28,28))
            btn.setMinimumHeight(54)
            btn.setStyleSheet(self.sidebar_button_style)
            btn.setToolTip(btn.text())
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

        self.dashboard.open_students.connect(
            lambda: self.switch_page(
                self.students,
                self.btn_students
            )
        )

        self.dashboard.open_teachers.connect(
            lambda: self.switch_page(
                self.teachers,
                self.btn_teachers
            )
        )

        self.dashboard.open_exams.connect(
            lambda: self.switch_page(
                self.exams,
                self.btn_exams
            )
        )

        self.dashboard.open_results.connect(
            lambda: self.switch_page(
                self.results,
                self.btn_results
            )
        )

        self.dashboard.open_school.connect(
            lambda: self.switch_page(
                self.school,
                self.btn_school
            )
        )

        self.dashboard.open_reports.connect(
            lambda: (
                self.switch_page(
                    self.results,
                    self.btn_results
                ),
                self.results.open_report_book()
            )
        )


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

        body.addWidget(self.sidebar_widget)
        body.addWidget(self.stack)
        body.setStretch(0, 0)
        body.setStretch(1, 1)

        self.update_sidebar_state()

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
        self.active_btn = button
        self.update_highlight(button)

    def update_highlight(
        self,
        active_btn
    ):
        for btn in self.nav_buttons:
            if btn == active_btn:
                style = (
                    self.sidebar_button_active_style_collapsed
                    if self.sidebar_collapsed
                    else self.sidebar_button_active_style
                )
                btn.setStyleSheet(style)
            else:
                btn.setStyleSheet(
                    self.sidebar_button_style_collapsed
                    if self.sidebar_collapsed
                    else self.sidebar_button_style
                )

    # =====================================
    # LEVEL SWITCH
    # =====================================

    def change_level(
        self,
        value
    ):
        SystemState.set_level(value)

    # =====================================
    # SIDEBAR COLLAPSE
    # =====================================

    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed
        self.update_sidebar_state()

    def update_sidebar_state(self):
        if self.sidebar_collapsed:
            start_width = 240
            end_width = 88
        else:
            start_width = 88
            end_width = 240

        self.sidebar_animation.stop()
        self.sidebar_animation.setStartValue(start_width)
        self.sidebar_animation.setEndValue(end_width)
        self.sidebar_animation.start()

        if self.sidebar_collapsed:
            self.sidebar_widget.setMaximumWidth(88)
            self.sidebar_widget.setMinimumWidth(88)
        else:
            self.sidebar_widget.setMaximumWidth(240)
            self.sidebar_widget.setMinimumWidth(88)

        for btn in self.nav_buttons:
            btn.setIconSize(QSize(28,28))
            if self.sidebar_collapsed:
                btn.setMinimumHeight(54)
                btn.setStyleSheet(self.sidebar_button_style_collapsed)
                btn.setText("")
            else:
                btn.setMinimumHeight(54)
                btn.setStyleSheet(self.sidebar_button_style)
                btn.setText(btn.toolTip())

        self.update_highlight(self.active_btn)

    def toggle_level(self):

        current = SystemState.get_level()

        if current == "O_LEVEL":
            SystemState.set_level("A_LEVEL")
            self.level_btn.setText("🎓 A-Level")
        else:
            SystemState.set_level("O_LEVEL")
            self.level_btn.setText("🎓 O-Level")

        self.refresh_all()


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
