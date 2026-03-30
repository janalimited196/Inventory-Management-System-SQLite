from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(8, 5), facecolor="white")
        super().__init__(self.figure)
        self.setParent(parent)

    def plot_stock_levels(self, data: list[tuple]):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if data:
            names, qtys = zip(*data)
            colors = [
                "#f44336" if q < 10 else "#FF9800" if q < 20 else "#4CAF50"
                for q in qtys
            ]
            ax.bar(range(len(names)), qtys, color=colors)
            ax.set_xticks(range(len(names)))
            ax.set_xticklabels(names, rotation=40, ha="right", fontsize=9)
            ax.set_ylabel("Quantity")
            ax.set_title("Stock Levels (Top 10)")
        self.figure.tight_layout()
        self.draw()
