from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView
)

from database import connect
from event_bus import EventBus
from security_settings import authorize_action
from theme import APP_STYLE
from add_exam import AddExamWindow
from system_state import SystemState

class ExamsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Examinations")

        self.resize(1000, 650)

        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.add_btn = QPushButton(
            "ADD EXAM"
        )

        self.add_btn.clicked.connect(
            self.open_add
        )

        self.delete_btn = QPushButton(
            "DELETE EXAM"
        )

        self.delete_btn.clicked.connect(
            self.delete_exam
        )

        self.status_btn = QPushButton(
            "TOGGLE STATUS"
        )

        self.status_btn.clicked.connect(
            self.toggle_status
        )

        self.refresh_btn = QPushButton(
            "REFRESH"
        )

        self.refresh_btn.clicked.connect(
            self.load_data
        )

        top.addWidget(self.add_btn)
        top.addWidget(self.delete_btn)
        top.addWidget(self.status_btn)
        top.addWidget(self.refresh_btn)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Exam",
            "Term",
            "Year",
            "Level",
            "Status"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addLayout(top)
        layout.addWidget(self.table)

        self.setLayout(layout)

        EventBus.subscribe(
            "EXAMS_UPDATED",
            self.load_data
        )
        EventBus.subscribe(
            "LEVEL_CHANGED",
            self.load_data
        )

        self.load_data()

    def open_add(self):

        self.win = AddExamWindow()
        self.win.show()

    def load_data(self):

        conn = connect()
        cur = conn.cursor()
        level = SystemState.get_level()

        cur.execute("""
            SELECT
                e.id,
                e.exam_name,
                t.term_name,
                a.year_name,
                e.level,
                e.status
            FROM exams e
            JOIN terms t
            ON e.term_id=t.id
            JOIN academic_years a
            ON t.academic_year_id=a.id
            WHERE e.level=?
            ORDER BY e.id DESC
        """, (level,))

        rows = cur.fetchall()

        conn.close()

        self.table.setRowCount(
            len(rows)
        )

        for r, row in enumerate(rows):

            for c, value in enumerate(row):

                self.table.setItem(
                    r,
                    c,
                    QTableWidgetItem(
                        str(value)
                    )
                )

    def delete_exam(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Error",
                "Select exam first"
            )

            return

        exam_id = self.table.item(
            row,
            0
        ).text()

        reply = QMessageBox.question(
            self,
            "Delete",
            "Delete selected exam?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        if not authorize_action(self, "Delete Exam"):
            return

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM exams WHERE id=?",
            (exam_id,)
        )

        conn.commit()
        conn.close()

        EventBus.emit("EXAMS_UPDATED")

    def toggle_status(self):

        row = self.table.currentRow()

        if row < 0:
            return

        exam_id = self.table.item(
            row,
            0
        ).text()

        status = self.table.item(
            row,
            5
        ).text()

        level = self.table.item(
            row,
            4
        ).text()

        new_status = "OPEN"

        if status == "OPEN":
            new_status = "CLOSED"

        conn = connect()
        cur = conn.cursor()

        if new_status == "OPEN":
            cur.execute("""
                UPDATE exams
                SET status='CLOSED'
                WHERE level=?
                  AND id<>?
                  AND status='OPEN'
            """, (
                level,
                exam_id
            ))

        cur.execute("""
            UPDATE exams
            SET status=?
            WHERE id=?
        """, (
            new_status,
            exam_id
        ))

        conn.commit()
        conn.close()

        EventBus.emit("EXAMS_UPDATED")
