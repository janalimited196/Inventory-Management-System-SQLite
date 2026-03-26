import sqlite3
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# Dataclasses


@dataclass
class Item:
    id: int
    name: str
    category_id: int
    quantity: int
    price: float
    min_stock: int
    supplier: str = ""
    date_added: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    category_name: str = ""

    @property
    def is_low_stock(self) -> bool:
        return self.quantity <= self.min_stock

    @property
    def total_value(self) -> float:
        return self.quantity * self.price


@dataclass
class Category:
    id: int
    name: str
    description: str = ""


# SQL Queries

CREATE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role     TEXT NOT NULL DEFAULT 'staff'
    )"""

CREATE_CATEGORIES = """
    CREATE TABLE IF NOT EXISTS categories (
        id          INTEGER PRIMARY KEY,
        name        TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT ''
    )"""

CREATE_ITEMS = """
    CREATE TABLE IF NOT EXISTS items (
        id          INTEGER PRIMARY KEY,
        name        TEXT NOT NULL,
        category_id INTEGER,
        quantity    INTEGER DEFAULT 0,
        price       REAL    DEFAULT 0.0,
        min_stock   INTEGER DEFAULT 0,
        supplier    TEXT    DEFAULT '',
        date_added  TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )"""

INSERT_DEFAULT_ADMIN = "INSERT OR IGNORE INTO users VALUES (1, 'admin', ?, 'admin')"
GET_USER_ROLE = "SELECT role FROM users WHERE username=? AND password=?"

GET_ALL_CATEGORIES = "SELECT id, name FROM categories ORDER BY name"
GET_CATEGORY_BY_ID = "SELECT id, name, description FROM categories WHERE id=?"
INSERT_CATEGORY = "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)"
UPDATE_CATEGORY = "UPDATE categories SET name=?, description=? WHERE id=?"
DELETE_CATEGORY = "DELETE FROM categories WHERE id=?"
COUNT_CATEGORIES = "SELECT COUNT(*) FROM categories"

GET_ALL_ITEMS = """
    SELECT i.id, i.name, c.name, i.quantity, i.price,
    i.min_stock, i.supplier, i.date_added
    FROM items i LEFT JOIN categories c ON i.category_id = c.id
    ORDER BY i.name"""
INSERT_ITEM = """
    INSERT INTO items (name, category_id, quantity, price, min_stock, supplier, date_added)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
UPDATE_ITEM = """
    UPDATE items SET name=?, category_id=?, quantity=?, price=?, min_stock=?, supplier=?
    WHERE id=?"""
DELETE_ITEM = "DELETE FROM items WHERE id=?"
COUNT_ITEMS = "SELECT COUNT(*) FROM items"
COUNT_LOW_STOCK = "SELECT COUNT(*) FROM items WHERE quantity <= min_stock"
GET_LOW_STOCK_ITEMS = """
    SELECT i.name, c.name, i.quantity, i.min_stock
    FROM items i LEFT JOIN categories c ON i.category_id = c.id
    WHERE i.quantity <= i.min_stock ORDER BY i.quantity ASC"""
GET_FULL_INVENTORY = """
    SELECT i.name, c.name, i.quantity, i.price, i.supplier
    FROM items i LEFT JOIN categories c ON i.category_id = c.id ORDER BY i.name"""
GET_CATEGORY_REPORT = """
    SELECT c.name, COUNT(i.id), COALESCE(SUM(i.quantity * i.price), 0)
    FROM categories c LEFT JOIN items i ON c.id = i.category_id
    GROUP BY c.id, c.name ORDER BY 3 DESC"""
GET_TOP_ITEMS_BY_QTY = "SELECT name, quantity FROM items ORDER BY quantity DESC LIMIT ?"
GET_EXPORT_DATA = """
    SELECT i.name, c.name, i.quantity, i.price, i.min_stock, i.supplier, i.date_added
    FROM items i LEFT JOIN categories c ON i.category_id = c.id"""


# Seed Data

DEFAULT_CATEGORIES = [
    ("Electronics", "Mobile, laptop, TV, accessories"),
    ("Clothing", "Men, women, kids apparel"),
    ("Food & Grocery", "Packaged food, beverages, dairy"),
    ("Furniture", "Office and home furniture"),
    ("Stationery", "Pens, notebooks, office supplies"),
    ("Tools & Hardware", "Hand tools, power tools, fasteners"),
    ("Health & Beauty", "Medicines, cosmetics, personal care"),
    ("Sports", "Fitness equipment, outdoor gear"),
    ("Toys", "Kids toys and games"),
    ("Automotive", "Car/bike parts and accessories"),
]

SAMPLE_ITEMS = [
    ("Samsung Galaxy S23", "Electronics", 25, 45999.0, 5, "Samsung India"),
    ("HP Laptop 15s", "Electronics", 8, 52999.0, 3, "HP India"),
    ("Wireless Earbuds", "Electronics", 40, 2499.0, 10, "Boat"),
    ("Men's Formal Shirt", "Clothing", 60, 899.0, 15, "Raymond"),
    ("Women's Kurti Set", "Clothing", 45, 1299.0, 10, "Biba"),
    ("Basmati Rice 5kg", "Food & Grocery", 100, 450.0, 20, "India Gate"),
    ("Olive Oil 1L", "Food & Grocery", 35, 599.0, 8, "Figaro"),
    ("Office Chair", "Furniture", 12, 8500.0, 3, "Godrej Interio"),
    ("Notebook A4 Pack", "Stationery", 80, 199.0, 25, "Classmate"),
    ("Whey Protein 1kg", "Health & Beauty", 18, 2799.0, 5, "MuscleBlaze"),
    ("Cricket Bat", "Sports", 15, 1599.0, 4, "SS Cricket"),
    ("Car Phone Mount", "Automotive", 30, 349.0, 10, "Grab On"),
]


# Database Management


class DatabaseManager:
    def __init__(self, db_path: str = "inventory.db"):
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self):
        with self._connect() as conn:
            c = conn.cursor()
            c.execute(CREATE_USERS)
            c.execute(CREATE_CATEGORIES)
            c.execute(CREATE_ITEMS)
            c.execute(
                INSERT_DEFAULT_ADMIN, (hashlib.sha256("admin".encode()).hexdigest(),)
            )
            for name, desc in DEFAULT_CATEGORIES:
                c.execute(INSERT_CATEGORY, (name, desc))
            if c.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
                self._seed_items(c)

    def _seed_items(self, c):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for name, cat_name, qty, price, min_stock, supplier in SAMPLE_ITEMS:
            row = c.execute(
                "SELECT id FROM categories WHERE name=?", (cat_name,)
            ).fetchone()
            if row:
                c.execute(
                    INSERT_ITEM, (name, row[0], qty, price, min_stock, supplier, now)
                )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def fetchall(self, sql: str, params: tuple = ()) -> list:
        try:
            with self._connect() as conn:
                return conn.execute(sql, params).fetchall()
        except sqlite3.Error as e:
            print(f"[DB] {e}")
            return []

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[Any]:
        try:
            with self._connect() as conn:
                return conn.execute(sql, params).fetchone()
        except sqlite3.Error as e:
            print(f"[DB] {e}")
            return None

    def execute(self, sql: str, params: tuple = ()) -> bool:
        try:
            with self._connect() as conn:
                conn.execute(sql, params)
            return True
        except sqlite3.Error as e:
            print(f"[DB] {e}")
            return False

    def scalar(self, sql: str, params: tuple = ()) -> Any:
        row = self.fetchone(sql, params)
        return row[0] if row else None
