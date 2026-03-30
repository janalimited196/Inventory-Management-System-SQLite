from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.services.category_service import CategoryService


def _require_text(widget, field, parent=None) -> bool:
    if not widget.text().strip():
        QMessageBox.warning(parent, "Error", f"{field} required!")
        widget.setFocus()
        return False
    return True


def _confirm_delete(parent, name="this item") -> bool:
    return (
        QMessageBox.question(
            parent,
            "Confirm Delete",
            f"Delete {name}? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        == QMessageBox.Yes
    )


class CategoriesPanel(QWidget):
    categories_changed = pyqtSignal()

    def __init__(self, cat_svc: CategoryService, parent=None):
        super().__init__(parent)
        self.cat_svc = cat_svc
        layout = QHBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._load_detail)

        fg = QGroupBox("Add / Edit Category")
        fl = QFormLayout()
        self.f_name = QLineEdit()
        self.f_desc = QTextEdit()
        self.f_desc.setMaximumHeight(90)
        fl.addRow("Name:", self.f_name)
        fl.addRow("Description:", self.f_desc)

        btns = QHBoxLayout()
        for lbl, slot, style in [
            ("Add", self._add, ""),
            ("Update", self._update, ""),
            ("Delete", self._delete, "QPushButton{background:#f44336;}"),
        ]:
            b = QPushButton(lbl)
            b.clicked.connect(slot)
            if style:
                b.setStyleSheet(style)
            btns.addWidget(b)
        fl.addRow(btns)
        fg.setLayout(fl)
        layout.addWidget(self.list_widget)
        layout.addWidget(fg)
        self.reload()

    def reload(self):
        self.list_widget.clear()
        for cat in self.cat_svc.get_all():
            item = QListWidgetItem(cat.name)
            item.setData(Qt.UserRole, cat.id)
            self.list_widget.addItem(item)

    def _load_detail(self, item):
        cat = self.cat_svc.get_by_id(item.data(Qt.UserRole))
        if cat:
            self.f_name.setText(cat.name)
            self.f_desc.setPlainText(cat.description)

    def _clear(self):
        self.f_name.clear()
        self.f_desc.clear()

    def _add(self):
        if not _require_text(self.f_name, "Category name", self):
            return
        try:
            self.cat_svc.add(self.f_name.text(), self.f_desc.toPlainText())
            self._clear()
            self.reload()
            self.categories_changed.emit()
            QMessageBox.information(self, "Success", "Category added!")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def _update(self):
        cur = self.list_widget.currentItem()
        if not cur:
            QMessageBox.warning(self, "Error", "Select a category to update!")
            return
        self.cat_svc.update(
            cur.data(Qt.UserRole), self.f_name.text(), self.f_desc.toPlainText()
        )
        self._clear()
        self.reload()
        self.categories_changed.emit()
        QMessageBox.information(self, "Success", "Category updated!")

    def _delete(self):
        cur = self.list_widget.currentItem()
        if not cur:
            QMessageBox.warning(self, "Error", "Select a category to delete!")
            return
        if _confirm_delete(self, f'"{cur.text()}"'):
            self.cat_svc.delete(cur.data(Qt.UserRole))
            self._clear()
            self.reload()
            self.categories_changed.emit()
            QMessageBox.information(self, "Success", "Category deleted!")
