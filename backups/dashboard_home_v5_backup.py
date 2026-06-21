from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout
)

from database import connect


class DashboardCard(QFrame):

    def __init__(self, title, value="0"):
        super().__init__()

        self.setObjectName("dashboardCard")

        layout = QVBoxLayout(self)

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setAlignment(Qt.AlignCenter)

        self.title_lbl = QLabel(title)
        self.title_lbl.setAlignment(Qt.AlignCenter)

        self.value_lbl.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
        """)

        self.title_lbl.setStyleSheet("""
            font-size: 14px;
            color: #cbd5e1;
        """)

        layout.addStretch()
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.title_lbl)
        layout.addStretch()

        self.setStyleSheet("""
            QFrame#dashboardCard{
                background: rgba(30,41,59,0.95);
                border-radius:18px;
                border:1px solid rgba(255,255,255,0.08);
            }
        """)

    def set_value(self, value):
        self.value_lbl.setText(str(value))


class DashboardHome(QWidget):

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)

        title = QLabel("SRMS V5 DASHBOARD")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:white;
            padding:10px;
        """)

        root.addWidget(title)

        # =================================
        # REGISTRATION CARD
        # =================================

        self.registration_card = QFrame()
        self.registration_card.setStyleSheet("""
            background: rgba(15,23,42,0.95);
            border-radius:20px;
            border:1px solid rgba(255,255,255,0.08);
        """)

        reg_layout = QVBoxLayout(self.registration_card)

        reg_title = QLabel("REGISTRATION")
        reg_title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:white;
        """)

        reg_layout.addWidget(reg_title)

        stats_row = QHBoxLayout()

        self.students_card = DashboardCard("Students")
        self.teachers_card = DashboardCard("Teachers")
        self.subjects_card = DashboardCard("Subjects")
        self.classes_card = DashboardCard("Classes")

        stats_row.addWidget(self.students_card)
        stats_row.addWidget(self.teachers_card)
        stats_row.addWidget(self.subjects_card)
        stats_row.addWidget(self.classes_card)

        reg_layout.addLayout(stats_row)

        root.addWidget(self.registration_card)

        # =================================
        # SECOND GRID
        # =================================

        grid = QGridLayout()

        self.exams_card = DashboardCard("Examinations")
        self.results_card = DashboardCard("Results")
        self.reports_card = DashboardCard("Reports")
        self.academic_card = DashboardCard("Academic")

        grid.addWidget(self.exams_card, 0, 0)
        grid.addWidget(self.results_card, 0, 1)
        grid.addWidget(self.reports_card, 1, 0)
        grid.addWidget(self.academic_card, 1, 1)

        root.addLayout(grid)

        # =================================
        # QUICK ACTIONS
        # =================================

        actions = QFrame()
        actions.setStyleSheet("""
            background: rgba(15,23,42,0.95);
            border-radius:20px;
            border:1px solid rgba(255,255,255,0.08);
        """)

        actions_layout = QVBoxLayout(actions)

        actions_title = QLabel("QUICK ACTIONS")

        actions_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            color:white;
        """)

        actions_layout.addWidget(actions_title)

        btn_row = QHBoxLayout()

        self.new_student_btn = QPushButton("New Student")
        self.new_teacher_btn = QPushButton("New Teacher")
        self.new_exam_btn = QPushButton("New Exam")
        self.import_btn = QPushButton("Import Marks")
        self.report_btn = QPushButton("Print Reports")

        for btn in [
            self.new_student_btn,
            self.new_teacher_btn,
            self.new_exam_btn,
            self.import_btn,
            self.report_btn
        ]:
            btn.setMinimumHeight(45)
            btn_row.addWidget(btn)

        actions_layout.addLayout(btn_row)

        root.addWidget(actions)

        root.addStretch()

        self.load_dashboard()

    def load_dashboard(self):

        conn = connect()
        cur = conn.cursor()

        try:

            cur.execute("SELECT COUNT(*) FROM students")
            students = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM teachers")
            teachers = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM subjects")
            subjects = cur.fetchone()[0]

            cur.execute("SELECT COUNT(DISTINCT class) FROM students")
            classes = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM exams")
            exams = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM results")
            results = cur.fetchone()[0]

        except Exception:
            students = 0
            teachers = 0
            subjects = 0
            classes = 0
            exams = 0
            results = 0

        finally:
            conn.close()

        self.students_card.set_value(students)
        self.teachers_card.set_value(teachers)
        self.subjects_card.set_value(subjects)
        self.classes_card.set_value(classes)

        self.exams_card.set_value(exams)
        self.results_card.set_value(results)
        self.reports_card.set_value("Ready")
        self.academic_card.set_value("2026")
