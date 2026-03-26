import pandas as pd

EXPORT_COLUMNS = [
    "Item Name",
    "Category",
    "Quantity",
    "Price",
    "Min Stock",
    "Supplier",
    "Date Added",
]


def export_excel(data: list[tuple], filepath: str) -> None:
    df = pd.DataFrame(data, columns=EXPORT_COLUMNS)
    df.to_excel(filepath, index=False)
