from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QFormLayout,
    QListWidget,
    QListWidgetItem
)

from database import connect


class TeacherProfilePage(QWidget):

    def __init__(self):
        super().__init__()

        self.teacher_id = None

        root = QVBoxLayout(self)

        # =====================================
        # HEADER
        # =====================================

        header = QHBoxLayout()

        self.back_btn = QPushButton("← Back To Teachers")

        self.title = QLabel("Teacher Profile")

        self.title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        header.addWidget(self.back_btn)
        header.addStretch()
        header.addWidget(self.title)

        root.addLayout(header)

        # =====================================
        # PERSONAL INFO
        # =====================================

        info_group = QGroupBox("Personal Information")

        info_form = QFormLayout()

        self.teacher_no_lbl = QLabel("-")
        self.name_lbl = QLabel("-")
        self.gender_lbl = QLabel("-")
        self.phone_lbl = QLabel("-")
        self.email_lbl = QLabel("-")
        self.status_lbl = QLabel("-")
        self.level_lbl = QLabel("-")

        info_form.addRow("Teacher No:", self.teacher_no_lbl)
        info_form.addRow("Full Name:", self.name_lbl)
        info_form.addRow("Gender:", self.gender_lbl)
        info_form.addRow("Phone:", self.phone_lbl)
        info_form.addRow("Email:", self.email_lbl)
        info_form.addRow("Status:", self.status_lbl)
        info_form.addRow("Level:", self.level_lbl)

        info_group.setLayout(info_form)

        root.addWidget(info_group)

        # =====================================
        # ASSIGNED SUBJECTS
        # =====================================

        subject_group = QGroupBox("Assigned Subjects")

        subject_layout = QVBoxLayout()

        self.subjects_list = QListWidget()

        subject_layout.addWidget(
            self.subjects_list
        )

        subject_group.setLayout(
            subject_layout
        )

        root.addWidget(subject_group)

        # =====================================
        # ASSIGNED CLASSES
        # =====================================

        class_group = QGroupBox("Assigned Classes")

        class_layout = QVBoxLayout()

        self.classes_list = QListWidget()

        class_layout.addWidget(
            self.classes_list
        )

        class_group.setLayout(
            class_layout
        )

        root.addWidget(class_group)

        root.addStretch()

    # =====================================
    # LOAD TEACHER
    # =====================================

    def load_teacher(self, teacher_id):

        self.teacher_id = teacher_id

        conn = connect()
        cur = conn.cursor()

        # ==========================
        # TEACHER DETAILS
        # ==========================

        cur.execute("""
            SELECT
                teacher_no,
                full_name,
                gender,
                phone,
                email,
                status,
                level
            FROM teachers
            WHERE id=?
        """, (teacher_id,))

        teacher = cur.fetchone()

        if teacher:

            self.teacher_no_lbl.setText(
                str(teacher[0] or "")
            )

            self.name_lbl.setText(
                str(teacher[1] or "")
            )

            self.gender_lbl.setText(
                str(teacher[2] or "")
            )

            self.phone_lbl.setText(
                str(teacher[3] or "")
            )

            self.email_lbl.setText(
                str(teacher[4] or "")
            )

            self.status_lbl.setText(
                str(teacher[5] or "")
            )

            self.level_lbl.setText(
                str(teacher[6] or "")
            )

            self.title.setText(
                f"Teacher Profile - {teacher[1]}"
            )

        # ==========================
        # SUBJECTS
        # ==========================

        self.subjects_list.clear()

        cur.execute("""
            SELECT subject_name
            FROM teacher_subjects
            WHERE teacher_id=?
            ORDER BY subject_name
        """, (teacher_id,))

        for row in cur.fetchall():

            self.subjects_list.addItem(
                QListWidgetItem(row[0])
            )

        # ==========================
        # CLASSES
        # ==========================

        self.classes_list.clear()

        cur.execute("""
            SELECT class_name
            FROM teacher_classes
            WHERE teacher_id=?
            ORDER BY class_name
        """, (teacher_id,))

        for row in cur.fetchall():

            self.classes_list.addItem(
                QListWidgetItem(row[0])
            )

        conn.close()