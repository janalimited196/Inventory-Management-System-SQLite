from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from core.services.item_service import ItemService
from core.services.category_service import CategoryService
from gui.components.stat_card import StatCard
from gui.components.chart_widget import ChartWidget
from gui.theme import COLOR_INFO, COLOR_DANGER, COLOR_SUCCESS


class DashboardPanel(QWidget):
    def __init__(self, item_svc: ItemService, cat_svc: CategoryService, parent=None):
        super().__init__(parent)
        self.item_svc = item_svc
        self.cat_svc = cat_svc
        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        self.c_items = StatCard("Total Items", "0", COLOR_INFO)
        self.c_low = StatCard("Low Stock", "0", COLOR_DANGER)
        self.c_cats = StatCard("Categories", "0", COLOR_SUCCESS)
        row.addWidget(self.c_items)
        row.addWidget(self.c_low)
        row.addWidget(self.c_cats)
        self.chart = ChartWidget()
        layout.addLayout(row)
        layout.addWidget(self.chart)
        self.refresh()

    def refresh(self):
        self.c_items.set_value(str(self.item_svc.count()))
        self.c_low.set_value(str(self.item_svc.count_low_stock()))
        self.c_cats.set_value(str(self.cat_svc.count()))
        self.chart.plot_stock_levels(self.item_svc.top_by_quantity())
