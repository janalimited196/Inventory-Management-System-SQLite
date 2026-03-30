from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from core.services.report_service import ReportService


class ReportsPanel(QWidget):
    def __init__(self, report_svc: ReportService, parent=None):
        super().__init__(parent)
        self.report_svc = report_svc
        layout = QVBoxLayout(self)
        btns = QHBoxLayout()
        for lbl, slot in [
            ("Low Stock", self._low),
            ("Full Inventory", self._full),
            ("By Category", self._cat),
        ]:
            b = QPushButton(lbl)
            b.clicked.connect(slot)
            btns.addWidget(b)
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        layout.addLayout(btns)
        layout.addWidget(self.display)

    def _low(self):
        self.display.setText(self.report_svc.low_stock())

    def _full(self):
        self.display.setText(self.report_svc.full_inventory())

    def _cat(self):
        self.display.setText(self.report_svc.by_category())
