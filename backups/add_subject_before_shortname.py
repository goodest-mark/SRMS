from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox
)

from database import connect
from theme import APP_STYLE


class AddSubjectWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Subject")

        self.resize(500, 400)

        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # =========================
        # TITLE
        # =========================

        title = QLabel("Add Subject")

        # =========================
        # SUBJECT CODE
        # =========================

        code_label = QLabel("Subject Code")

        self.code = QLineEdit()
        self.code.setPlaceholderText(
            "e.g BIO"
        )

        # =========================
        # SUBJECT NAME
        # =========================

        name_label = QLabel("Subject Name")

        self.name = QLineEdit()
        self.name.setPlaceholderText(
            "e.g Biology"
        )

        # =========================
        # COUNTED
        # =========================

        counted_label = QLabel(
            "Count In Results?"
        )

        self.counted = QComboBox()

        self.counted.addItems([
            "Yes",
            "No"
        ])

        # =========================
        # SAVE BUTTON
        # =========================

        save_btn = QPushButton(
            "SAVE SUBJECT"
        )

        save_btn.clicked.connect(
            self.save
        )

        # =========================
        # LAYOUT
        # =========================

        layout.addWidget(title)

        layout.addWidget(code_label)
        layout.addWidget(self.code)

        layout.addWidget(name_label)
        layout.addWidget(self.name)

        layout.addWidget(counted_label)
        layout.addWidget(self.counted)

        layout.addSpacing(10)

        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save(self):

        code = self.code.text().strip().upper()

        name = self.name.text().strip()

        counted = self.counted.currentText()

        if not code or not name:

            QMessageBox.warning(
                self,
                "Error",
                "All fields required"
            )

            return

        conn = connect()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT subject_code
                FROM subjects
                WHERE subject_code=?
                """,
                (code,)
            )

            if cur.fetchone():
                QMessageBox.warning(
                    self,
                    "Error",
                    "Subject Code Already Exists"
                )
                return

            cur.execute(
                """
                INSERT INTO subjects(
                    subject_code,
                    subject_name,
                    is_counted
                )
                VALUES(?,?,?)
                """,
                (
                    code,
                    name,
                    counted
                )
            )

            conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Subject Saved Successfully"
            )

            self.code.clear()
            self.name.clear()
            self.counted.setCurrentIndex(0)

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )
        finally:
            conn.close()
        