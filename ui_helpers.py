"""Shared UI helper functions to eliminate repeated dialog/widget boilerplate."""

from PySide6.QtWidgets import QMessageBox, QComboBox


def confirm_action(parent, title, message):
    """Show a Yes/No confirmation dialog. Returns True if user clicked Yes."""
    reply = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.Yes | QMessageBox.No,
    )
    return reply == QMessageBox.Yes


def show_error(parent, message, title="Error"):
    """Show a warning message box."""
    QMessageBox.warning(parent, title, message)


def show_info(parent, message, title="Success"):
    """Show an informational message box."""
    QMessageBox.information(parent, title, message)


def load_combo(combo, items, block_signals=True):
    """Reload a QComboBox with (text, data) tuples.

    Args:
        combo: QComboBox instance
        items: list of (display_text, user_data) tuples, or plain strings
        block_signals: temporarily block signals during reload
    """
    if block_signals:
        combo.blockSignals(True)
    combo.clear()
    for item in items:
        if isinstance(item, (list, tuple)):
            combo.addItem(str(item[0]), item[1] if len(item) > 1 else None)
        else:
            combo.addItem(str(item))
    if block_signals:
        combo.blockSignals(False)
