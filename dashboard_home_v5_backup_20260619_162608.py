from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout
)
from database import connect


class GlassCard(QFrame):
    def __init__(self, title="", value="0"):
        super().__init__()
        self.setObjectName("glassCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setAlignment(Qt.AlignCenter)

        self.title_lbl = QLabel(title)
        self.title_lbl.setAlignment(Qt.AlignCenter)

        self.value_lbl.setStyleSheet(
            "font-size:30px;font-weight:800;color:white;background:transparent;"
        )
        self.title_lbl.setStyleSheet(
            "font-size:13px;color:#94a3b8;background:transparent;"
        )

        layout.addStretch()
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.title_lbl)
        layout.addStretch()

        self.setStyleSheet("""
        QFrame#glassCard{
            background: rgba(15,23,42,0.92);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:22px;
        }
        """)

    def set_value(self, value):
        self.value_lbl.setText(str(value))


class DashboardHome(QWidget):

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        self.hero = QFrame()
        self.hero.setStyleSheet("""
        QFrame{
            background: rgba(15,23,42,0.95);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:24px;
        }
        """)

        hero_layout = QVBoxLayout(self.hero)

        self.school_lbl = QLabel("School")
        self.school_lbl.setStyleSheet(
            "font-size:28px;font-weight:800;color:white;background:transparent;"
        )

        self.exam_lbl = QLabel("Active Exam")
        self.exam_lbl.setStyleSheet(
            "font-size:14px;color:#10b981;background:transparent;"
        )

        hero_layout.addWidget(self.school_lbl)
        hero_layout.addWidget(QLabel("School Report Management System"))
        hero_layout.addWidget(self.exam_lbl)
        hero_layout.addWidget(QLabel("Powered by Mark Deals"))

        root.addWidget(self.hero)

        grid = QGridLayout()

        self.students_card = GlassCard("Students")
        self.teachers_card = GlassCard("Teachers")
        self.subjects_card = GlassCard("Subjects")
        self.classes_card = GlassCard("Classes")
        self.exams_card = GlassCard("Exams")
        self.results_card = GlassCard("Results")

        cards = [
            self.students_card, self.teachers_card, self.subjects_card,
            self.classes_card, self.exams_card, self.results_card
        ]

        pos = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]
        for c,p in zip(cards,pos):
            grid.addWidget(c,*p)

        root.addLayout(grid)

        lower = QHBoxLayout()

        self.info = QFrame()
        self.info.setStyleSheet("""
        QFrame{
            background: rgba(15,23,42,0.95);
            border-radius:22px;
            border:1px solid rgba(255,255,255,0.08);
        }
        """)

        info_layout = QVBoxLayout(self.info)
        self.school_info = QLabel("School Information")
        info_layout.addWidget(self.school_info)

        self.actions = QFrame()
        self.actions.setStyleSheet(self.info.styleSheet())

        act_layout = QGridLayout(self.actions)

        for i, txt in enumerate([
            "New Student",
            "Teachers",
            "Exams",
            "Results",
            "School Center",
            "Reports"
        ]):
            btn = QPushButton(txt)
            btn.setMinimumHeight(50)
            act_layout.addWidget(btn, i//2, i%2)

        lower.addWidget(self.info, 2)
        lower.addWidget(self.actions, 3)

        root.addLayout(lower)
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

            cur.execute("SELECT school_name, head_teacher, academic_master, school_phone, school_email FROM school_profile LIMIT 1")
            row = cur.fetchone()

            if row:
                school, head, academic, phone, email = row
                self.school_lbl.setText(school)
                self.school_info.setText(
                    f"School: {school}\n\nHead Teacher: {head}\nAcademic Master: {academic}\nPhone: {phone}\nEmail: {email}"
                )

            cur.execute("SELECT exam_name FROM exams WHERE status='OPEN' LIMIT 1")
            exam = cur.fetchone()
            if exam:
                self.exam_lbl.setText(f"Active Exam: {exam[0]}")

            self.students_card.set_value(students)
            self.teachers_card.set_value(teachers)
            self.subjects_card.set_value(subjects)
            self.classes_card.set_value(classes)
            self.exams_card.set_value(exams)
            self.results_card.set_value(results)

        finally:
            conn.close()
