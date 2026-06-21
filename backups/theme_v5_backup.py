APP_STYLE = """
/* =========================
   GLOBAL
========================= */

QWidget {
    background-color: #0f172a;
    color: #e5e7eb;
    font-family: Arial;
    font-size: 13px;
}

/* =========================
   LABELS
========================= */

QLabel {
    color: #cbd5e1;
}

/* =========================
   INPUTS
========================= */

QLineEdit {
    padding: 10px;
    border: 1px solid #334155;
    border-radius: 6px;
    background-color: #111827;
    color: white;
}

QLineEdit:focus {
    border: 1px solid #3b82f6;
}

/* =========================
   COMBOBOX
========================= */

QComboBox {
    padding: 10px;
    border: 1px solid #334155;
    border-radius: 6px;
    background-color: #111827;
    color: white;
    min-height: 20px;
}

QComboBox:hover {
    border: 1px solid #3b82f6;
}

QComboBox:on {
    border: 1px solid #2563eb;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #111827;
    color: white;
    border: 1px solid #334155;
    selection-background-color: #2563eb;
    selection-color: white;
    outline: none;
}

/* =========================
   BUTTONS
========================= */

QPushButton {
    background-color: #2563eb;
    color: white;
    padding: 10px;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

/* =========================
   TABLES
========================= */

QTableWidget {
    background-color: #111827;
    color: white;
    gridline-color: #334155;
    border: 1px solid #334155;
    selection-background-color: #2563eb;
    selection-color: white;
}

QTableWidget::item {
    padding: 6px;
}

QTableWidget::item:selected {
    background-color: #2563eb;
    color: white;
}

/* =========================
   TABLE HEADERS
========================= */

QHeaderView::section {
    background-color: #1e293b;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

/* =========================
   SCROLLBARS
========================= */

QScrollBar:vertical {
    background: #0f172a;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background: #2563eb;
    border-radius: 5px;
    min-height: 25px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #0f172a;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background: #2563eb;
    border-radius: 5px;
    min-width: 25px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* =========================
   MESSAGE BOX
========================= */

QMessageBox {
    background-color: #0f172a;
}

/* =========================
   TOOLTIPS
========================= */

QToolTip {
    background-color: #111827;
    color: white;
    border: 1px solid #334155;
    padding: 5px;
}
"""