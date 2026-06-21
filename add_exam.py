from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from database import connect
from event_bus import EventBus
from system_state import SystemState
from theme import APP_STYLE


class AddExamWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Examination")
        self.resize(500, 300)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        title = QLabel("Create Examination")

        exam_label = QLabel("Exam Name")

        self.exam_name = QLineEdit()
        self.exam_name.setPlaceholderText(
            "e.g Midterm"
        )

        save_btn = QPushButton(
            "SAVE EXAM"
        )

        save_btn.clicked.connect(
            self.save_exam
        )

        layout.addWidget(title)
        layout.addWidget(exam_label)
        layout.addWidget(self.exam_name)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_exam(self):

        exam_name = (
            self.exam_name.text()
            .strip()
        )

        if not exam_name:

            QMessageBox.warning(
                self,
                "Error",
                "Enter exam name"
            )

            return

        conn = connect()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT id
                FROM terms
                WHERE is_active=1
                LIMIT 1
            """)

            row = cur.fetchone()

            if not row:

                QMessageBox.warning(
                    self,
                    "Error",
                    "No active term"
                )

                conn.close()
                return

            term_id = row[0]
            level = SystemState.get_level()

            cur.execute("""
                UPDATE exams
                SET status='CLOSED'
                WHERE level=?
                  AND status='OPEN'
            """, (level,))

            cur.execute("""
                INSERT INTO exams(
                    exam_name,
                    term_id,
                    level,
                    status
                )
                VALUES (?, ?, ?, ?)
            """, (
                exam_name,
                term_id,
                level,
                "OPEN"
            ))

            conn.commit()
            EventBus.emit("EXAMS_UPDATED")

            QMessageBox.information(
                self,
                "Success",
                "Exam Saved Successfully"
            )

            self.exam_name.clear()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

        conn.close()
