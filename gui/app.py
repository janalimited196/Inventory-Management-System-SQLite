import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QDialog,
    QAction,
    QFileDialog,
    QMessageBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt

from core.database.manager import DatabaseManager
from core.services.auth_service import AuthService
from core.services.item_service import ItemService
from core.services.category_service import CategoryService
from core.services.report_service import ReportService
from core.exporters.excel_exporter import export_excel
from core.exporters.pdf_exporter import export_pdf

from gui.theme import APP_STYLE
from gui.panels.dashboard_panel import DashboardPanel
from gui.panels.items_panel import ItemsPanel
from gui.panels.categories_panel import CategoriesPanel
from gui.panels.reports_panel import ReportsPanel


class LoginDialog(QDialog):
    def __init__(self, auth_svc: AuthService):
        super().__init__()
        self.auth_svc = auth_svc
        self.user_role = None
        self.setWindowTitle("Inventory Management — Login")
        self.setFixedSize(380, 260)
        layout = QVBoxLayout(self)
        title = QLabel("INVENTORY MANAGER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #2196F3; margin: 16px;"
        )
        fl = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self._login)
        fl.addRow("Username:", self.username)
        fl.addRow("Password:", self.password)
        btn = QPushButton("Login")
        btn.clicked.connect(self._login)
        layout.addWidget(title)
        layout.addLayout(fl)
        layout.addWidget(btn)

    def _login(self):
        role = self.auth_svc.verify_login(self.username.text(), self.password.text())
        if role:
            self.user_role = role
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials!")


class MainWindow(QMainWindow):
    def __init__(self, db: DatabaseManager, user_role: str):
        super().__init__()
        self.db = db
        self.item_svc = ItemService(db)
        self.cat_svc = CategoryService(db)
        self.report_svc = ReportService(db)
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1200, 800)
        self._build_tabs()
        self._build_toolbar()
        self.statusBar().showMessage(f"Logged in as: {user_role}")

    def _build_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.dashboard = DashboardPanel(self.item_svc, self.cat_svc)
        self.items = ItemsPanel(self.item_svc, self.cat_svc)
        self.categories = CategoriesPanel(self.cat_svc)
        self.reports = ReportsPanel(self.report_svc)
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.items, "Items")
        self.tabs.addTab(self.categories, "Categories")
        self.tabs.addTab(self.reports, "Reports")
        self.categories.categories_changed.connect(self.items.reload_categories)
        self.categories.categories_changed.connect(self.dashboard.refresh)
        self.items.data_changed.connect(self.dashboard.refresh)

    def _build_toolbar(self):
        tb = self.addToolBar("Main")
        for lbl, slot in [
            ("Refresh", self._refresh),
            ("Export Excel", self._excel),
            ("Export PDF", self._pdf),
            ("Logout", self._logout),
        ]:
            a = QAction(lbl, self)
            a.triggered.connect(slot)
            tb.addAction(a)

    def _refresh(self):
        self.dashboard.refresh()
        self.items.reload_items()
        self.items.reload_categories()
        self.categories.reload()
        self.statusBar().showMessage("Refreshed", 2000)

    def _excel(self):
        data = self.item_svc.get_export_data()
        if not data:
            QMessageBox.warning(self, "Warning", "No data to export!")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel", "inventory.xlsx", "Excel (*.xlsx)"
        )
        if path:
            try:
                export_excel(data, path)
                QMessageBox.information(self, "Success", f"Saved: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _pdf(self):
        data = self.item_svc.get_export_data()
        if not data:
            QMessageBox.warning(self, "Warning", "No data to export!")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "inventory.pdf", "PDF (*.pdf)"
        )
        if path:
            try:
                export_pdf(data, path)
                QMessageBox.information(self, "Success", f"Saved: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _logout(self):
        if (
            QMessageBox.question(
                self,
                "Logout",
                "Are you sure you want to logout?",
                QMessageBox.Yes | QMessageBox.No,
            )
            == QMessageBox.Yes
        ):
            self.close()
            run_app()


def run_app() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Inventory Management System")
    app.setStyleSheet(APP_STYLE)
    db = DatabaseManager()
    login = LoginDialog(AuthService(db))
    if login.exec_() != QDialog.Accepted:
        return 0
    window = MainWindow(db, login.user_role)
    window.show()
    return app.exec_()
