from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView,
    QComboBox
)

from database import connect
from system_state import SystemState
from event_bus import EventBus


class TeachersListPage(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_teacher_id = None

        layout = QVBoxLayout(self)

        # ==================================
        # HEADER
        # ==================================

        title = QLabel("TEACHERS MANAGEMENT")

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        # ==================================
        # FORM
        # ==================================

        form = QHBoxLayout()

        self.teacher_no = QLineEdit()
        self.teacher_no.setPlaceholderText("Teacher No")

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")

        self.gender = QComboBox()
        self.gender.addItems([
            "Male",
            "Female"
        ])

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.save_btn = QPushButton("SAVE")
        self.save_btn.clicked.connect(
            self.save_teacher
        )

        self.clear_btn = QPushButton("CLEAR")
        self.clear_btn.clicked.connect(
            self.clear_form
        )

        form.addWidget(self.teacher_no)
        form.addWidget(self.full_name)
        form.addWidget(self.gender)
        form.addWidget(self.phone)
        form.addWidget(self.email)
        form.addWidget(self.save_btn)
        form.addWidget(self.clear_btn)

        layout.addLayout(form)

        # ==================================
        # SEARCH
        # ==================================

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search teacher..."
        )

        self.search.textChanged.connect(
            self.load
        )

        layout.addWidget(self.search)

        # ==================================
        # TABLE
        # ==================================

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Teacher No",
            "Full Name",
            "Gender",
            "Phone",
            "Email",
            "Status"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.doubleClicked.connect(
            self.load_selected
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        EventBus.subscribe(
            "TEACHERS_UPDATED",
            self.load
        )

        EventBus.subscribe(
            "LEVEL_CHANGED",
            self.load
        )

        self.load()

    # ==================================
    # LOAD
    # ==================================

    def load(self):

        conn = connect()
        cur = conn.cursor()

        search = self.search.text().strip()

        if search:

            cur.execute("""
                SELECT
                    id,
                    teacher_no,
                    full_name,
                    gender,
                    phone,
                    email,
                    status
                FROM teachers
                WHERE
                    teacher_no LIKE ?
                    OR full_name LIKE ?
                ORDER BY id DESC
            """, (
                f"%{search}%",
                f"%{search}%"
            ))

        else:

            cur.execute("""
                SELECT
                    id,
                    teacher_no,
                    full_name,
                    gender,
                    phone,
                    email,
                    status
                FROM teachers
                ORDER BY id DESC
            """)

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

    # ==================================
    # SAVE
    # ==================================

    def save_teacher(self):

        teacher_no = self.teacher_no.text().strip()
        full_name = self.full_name.text().strip()

        gender = self.gender.currentText()

        phone = self.phone.text().strip()
        email = self.email.text().strip()

        level = SystemState.get_level()

        if not teacher_no or not full_name:

            QMessageBox.warning(
                self,
                "Error",
                "Teacher No and Name required"
            )

            return

        conn = connect()
        cur = conn.cursor()

        try:

            if self.selected_teacher_id:

                cur.execute("""
                    UPDATE teachers
                    SET
                        teacher_no=?,
                        full_name=?,
                        gender=?,
                        phone=?,
                        email=?
                    WHERE id=?
                """, (
                    teacher_no,
                    full_name,
                    gender,
                    phone,
                    email,
                    self.selected_teacher_id
                ))

            else:

                cur.execute("""
                    INSERT INTO teachers(
                        teacher_no,
                        full_name,
                        gender,
                        phone,
                        email,
                        status,
                        level
                    )
                    VALUES(
                        ?,?,?,?,?,?,?
                    )
                """, (
                    teacher_no,
                    full_name,
                    gender,
                    phone,
                    email,
                    "ACTIVE",
                    level
                ))

            conn.commit()

            EventBus.emit(
                "TEACHERS_UPDATED"
            )

            self.clear_form()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                str(e)
            )

        finally:

            conn.close()

    # ==================================
    # SELECT
    # ==================================

    def load_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.selected_teacher_id = int(
            self.table.item(row, 0).text()
        )

        self.teacher_no.setText(
            self.table.item(row, 1).text()
        )

        self.full_name.setText(
            self.table.item(row, 2).text()
        )

        self.gender.setCurrentText(
            self.table.item(row, 3).text()
        )

        self.phone.setText(
            self.table.item(row, 4).text()
        )

        self.email.setText(
            self.table.item(row, 5).text()
        )

        self.save_btn.setText(
            "UPDATE"
        )

    # ==================================
    # CLEAR
    # ==================================

    def clear_form(self):

        self.selected_teacher_id = None

        self.teacher_no.clear()
        self.full_name.clear()
        self.phone.clear()
        self.email.clear()

        self.gender.setCurrentIndex(0)

        self.save_btn.setText(
            "SAVE"
        )
