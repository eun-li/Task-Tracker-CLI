# Building a Task Tracker CLI with Python
### A Beginner's Step-by-Step Guide

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Overview](#project-overview)
4. [Setting Up Your Project](#setting-up-your-project)
5. [Core Concepts You'll Learn](#core-concepts-youll-learn)
6. [Building the App — Step by Step](#building-the-app--step-by-step)
   - [Step 1: Create the Project Files](#step-1-create-the-project-files)
   - [Step 2: Define the Task Structure](#step-2-define-the-task-structure)
   - [Step 3: Save and Load Tasks](#step-3-save-and-load-tasks)
   - [Step 4: Add a Task](#step-4-add-a-task)
   - [Step 5: List All Tasks](#step-5-list-all-tasks)
   - [Step 6: Complete a Task](#step-6-complete-a-task)
   - [Step 7: Delete a Task](#step-7-delete-a-task)
   - [Step 8: Build the CLI Menu](#step-8-build-the-cli-menu)
   - [Step 9: The Entry Point](#step-9-the-entry-point)
7. [Full Source Code](#full-source-code)
8. [Running Your App](#running-your-app)
9. [Example Session](#example-session)
10. [Exercises to Go Further](#exercises-to-go-further)
11. [Common Errors & Fixes](#common-errors--fixes)
12. [Glossary](#glossary)

---

## Introduction

A **Task Tracker CLI** (Command-Line Interface) is a program you run in your terminal to manage a to-do list. You can add tasks, mark them as done, delete them, and view them — all without leaving the command line.

This project is perfect for beginners because it teaches:

- How Python programs are structured
- How to read input from a user
- How to save data to a file so it persists between runs
- How to organize code into functions

By the end of this guide, you'll have a working app you built yourself.

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.8 or higher** installed. Check by running:
  ```bash
  python --version
  ```
  or
  ```bash
  python3 --version
  ```
  You should see something like `Python 3.11.0`.

- A **text editor** or IDE. Recommended options for beginners:
  - [VS Code](https://code.visualstudio.com/) (free, beginner-friendly)
  - [PyCharm Community](https://www.jetbrains.com/pycharm/download/) (free)
  - Even Notepad works in a pinch!

- Basic familiarity with opening a terminal/command prompt.

> **No prior Python knowledge required** — every concept is explained as it's introduced.

---

## Project Overview

Here is what the finished app can do:

| Command | What It Does |
|---|---|
| Add a task | Creates a new task with a title |
| List tasks | Shows all tasks with their status |
| Complete a task | Marks a task as ✅ done |
| Delete a task | Removes a task permanently |
| Quit | Exits the program |

Tasks are stored in a file called `tasks.json` so they are saved even after you close the program.

---

## Setting Up Your Project

Create a folder for your project. Open your terminal and run:

```bash
mkdir task_tracker
cd task_tracker
```

Inside this folder, you will create two files:

```
task_tracker/
├── task_tracker.py   ← your main Python file
└── tasks.json        ← created automatically when you add your first task
```

That's it — no installation of third-party packages needed. This project only uses Python's **standard library**.

---

## Core Concepts You'll Learn

### Functions
A function is a reusable block of code. You define it once and call it whenever you need it.

```python
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")  # prints: Hello, Alice!
```

### Lists and Dictionaries
A **list** stores multiple items in order. A **dictionary** stores key-value pairs (like a real dictionary: word → definition).

```python
# List
fruits = ["apple", "banana", "cherry"]

# Dictionary
task = {"id": 1, "title": "Buy groceries", "done": False}
```

### JSON Files
JSON (JavaScript Object Notation) is a simple file format for saving structured data. Python has a built-in `json` module to read and write it.

```python
import json

# Saving data
with open("data.json", "w") as f:
    json.dump({"name": "Alice"}, f)

# Loading data
with open("data.json", "r") as f:
    data = json.load(f)
```

### The `os` Module
The `os` module lets you interact with the operating system — for example, checking if a file exists.

```python
import os
os.path.exists("tasks.json")  # Returns True or False
```

---

## Building the App — Step by Step

### Step 1: Create the Project Files

Open your text editor and create a new file called `task_tracker.py` inside your `task_tracker` folder.

At the very top of the file, add the imports your program will need:

```python
import json
import os
```

- `json` — to save and load tasks from a file
- `os` — to check if the tasks file already exists

---

### Step 2: Define the Task Structure

Every task in our app will be a dictionary with three fields:

```python
{
    "id": 1,
    "title": "Buy groceries",
    "done": False
}
```

| Field | Type | Description |
|---|---|---|
| `id` | Integer | A unique number that identifies the task |
| `title` | String | The text description of the task |
| `done` | Boolean | `True` if complete, `False` if pending |

We will store all tasks together in a **list** of these dictionaries.

---

### Step 3: Save and Load Tasks

We need two helper functions: one to **load** tasks from the file, and one to **save** them back.

```python
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save the list of tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
```

**What's happening here?**

- `TASKS_FILE = "tasks.json"` — a constant that holds the filename. Using a constant means if you ever rename the file, you only change it in one place.
- `os.path.exists(TASKS_FILE)` — checks if the file exists before trying to open it (avoids an error on the first run).
- `json.dump(..., indent=4)` — saves the JSON in a human-readable format with 4-space indentation.

---

### Step 4: Add a Task

```python
def add_task(title):
    """Add a new task with the given title."""
    tasks = load_tasks()

    # Generate a new unique ID
    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added: [{new_id}] {title}")
```

**Key detail — generating a unique ID:**

```python
new_id = max((task["id"] for task in tasks), default=0) + 1
```

This line finds the highest existing ID and adds 1. The `default=0` handles the case where the list is empty (so the first task gets ID 1).

---

### Step 5: List All Tasks

```python
def list_tasks():
    """Display all tasks in a formatted list."""
    tasks = load_tasks()

    if not tasks:
        print("📋 No tasks yet. Add one!")
        return

    print("\n📋 Your Tasks:")
    print("-" * 35)
    for task in tasks:
        status = "✅" if task["done"] else "⬜"
        print(f"  {status} [{task['id']}] {task['title']}")
    print("-" * 35)
    print()
```

**What's happening here?**

- `if not tasks:` — checks if the list is empty.
- `"✅" if task["done"] else "⬜"` — this is a **ternary expression** (a compact if/else). It picks an emoji based on the task's `done` status.
- `"-" * 35` — Python lets you multiply a string to repeat it. This creates a divider line.

---

### Step 6: Complete a Task

```python
def complete_task(task_id):
    """Mark a task as done by its ID."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"ℹ️  Task [{task_id}] is already marked as done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"✅ Task [{task_id}] marked as complete!")
            return

    print(f"❌ No task found with ID {task_id}.")
```

**What's happening here?**

- We loop through all tasks to find the one with a matching `id`.
- If we find it, we set `done` to `True` and save.
- If no task matches, we inform the user.
- The `return` inside the loop stops the function once the task is found.

---

### Step 7: Delete a Task

```python
def delete_task(task_id):
    """Remove a task permanently by its ID."""
    tasks = load_tasks()
    original_count = len(tasks)

    tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) == original_count:
        print(f"❌ No task found with ID {task_id}.")
    else:
        save_tasks(tasks)
        print(f"🗑️  Task [{task_id}] deleted.")
```

**Key detail — list comprehension:**

```python
tasks = [task for task in tasks if task["id"] != task_id]
```

This is a **list comprehension** — a compact way to build a new list. It keeps every task *except* the one with the matching ID. Comparing the list length before and after tells us whether anything was actually removed.

---

### Step 8: Build the CLI Menu

This is the function that shows the interactive menu and handles user input:

```python
def show_menu():
    """Display the main menu."""
    print("\n=== Task Tracker ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Quit")
    print("====================")

def run():
    """Main loop: show the menu and handle user choices."""
    print("Welcome to Task Tracker! 🗒️")

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("⚠️  Task title cannot be empty.")

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to complete: "))
                complete_task(task_id)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "4":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "5":
            print("Goodbye! 👋")
            break

        else:
            print("⚠️  Invalid choice. Please enter a number from 1 to 5.")
```

**Key concepts used here:**

- `while True:` — an infinite loop that keeps the menu running until the user chooses to quit.
- `input(...).strip()` — `strip()` removes any accidental leading/trailing spaces from what the user types.
- `try / except ValueError` — protects against the user typing letters when a number is expected.
- `break` — exits the `while True` loop when the user picks "Quit".

---

### Step 9: The Entry Point

This is the standard Python pattern for running code only when the file is executed directly (not when imported as a module):

```python
if __name__ == "__main__":
    run()
```

Always add this at the very bottom of your file.

---

## Full Source Code

Here is the complete `task_tracker.py` file — all steps combined:

```python
import json
import os

TASKS_FILE = "tasks.json"


# ── File I/O ──────────────────────────────────────────────────────────────────

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save the list of tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# ── Task Operations ───────────────────────────────────────────────────────────

def add_task(title):
    """Add a new task with the given title."""
    tasks = load_tasks()
    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added: [{new_id}] {title}")


def list_tasks():
    """Display all tasks in a formatted list."""
    tasks = load_tasks()
    if not tasks:
        print("📋 No tasks yet. Add one!")
        return
    print("\n📋 Your Tasks:")
    print("-" * 35)
    for task in tasks:
        status = "✅" if task["done"] else "⬜"
        print(f"  {status} [{task['id']}] {task['title']}")
    print("-" * 35)
    print()


def complete_task(task_id):
    """Mark a task as done by its ID."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"ℹ️  Task [{task_id}] is already marked as done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"✅ Task [{task_id}] marked as complete!")
            return
    print(f"❌ No task found with ID {task_id}.")


def delete_task(task_id):
    """Remove a task permanently by its ID."""
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == original_count:
        print(f"❌ No task found with ID {task_id}.")
    else:
        save_tasks(tasks)
        print(f"🗑️  Task [{task_id}] deleted.")


# ── Menu & Main Loop ──────────────────────────────────────────────────────────

def show_menu():
    """Display the main menu."""
    print("\n=== Task Tracker ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Quit")
    print("====================")


def run():
    """Main loop: show the menu and handle user choices."""
    print("Welcome to Task Tracker! 🗒️")
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("⚠️  Task title cannot be empty.")

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to complete: "))
                complete_task(task_id)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "4":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("⚠️  Please enter a valid number.")

        elif choice == "5":
            print("Goodbye! 👋")
            break

        else:
            print("⚠️  Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    run()
```

---

## Running Your App

Open your terminal, navigate to your project folder, and run:

```bash
python task_tracker.py
```

or, on some systems:

```bash
python3 task_tracker.py
```

---

## Example Session

```
Welcome to Task Tracker! 🗒️

=== Task Tracker ===
1. Add task
2. List tasks
3. Complete a task
4. Delete a task
5. Quit
====================
Enter your choice (1-5): 1
Enter task title: Buy groceries
✅ Task added: [1] Buy groceries

Enter your choice (1-5): 1
Enter task title: Write Python docs
✅ Task added: [2] Write Python docs

Enter your choice (1-5): 2

📋 Your Tasks:
-----------------------------------
  ⬜ [1] Buy groceries
  ⬜ [2] Write Python docs
-----------------------------------

Enter your choice (1-5): 3
Enter the task ID to complete: 1
✅ Task [1] marked as complete!

Enter your choice (1-5): 2

📋 Your Tasks:
-----------------------------------
  ✅ [1] Buy groceries
  ⬜ [2] Write Python docs
-----------------------------------

Enter your choice (1-5): 5
Goodbye! 👋
```

---

## Exercises to Go Further

Once your basic app is working, try these challenges to level up:

**Beginner**
- Add a "due date" field to each task (store it as a string like `"2025-12-31"`).
- Add a way to edit a task's title.

**Intermediate**
- Add a "priority" field (low, medium, high) and sort tasks by priority when listing.
- Allow filtering: show only pending tasks, or only completed ones.
- Add a `clear_completed` option that removes all finished tasks at once.

**Advanced**
- Replace the numbered menu with command-line arguments using Python's `argparse` module. For example: `python task_tracker.py add "Buy milk"`.
- Add colors to the output using the `colorama` library (`pip install colorama`).
- Add timestamps: record when a task was created and when it was completed.

---

## Common Errors & Fixes

| Error | Likely Cause | Fix |
|---|---|---|
| `SyntaxError` | Typo in your code | Read the error line number carefully and check for missing colons, quotes, or parentheses |
| `FileNotFoundError` | Wrong working directory | Make sure your terminal is inside the `task_tracker` folder when you run the script |
| `json.decoder.JSONDecodeError` | `tasks.json` is corrupted | Delete `tasks.json` and let the app create a fresh one |
| `ValueError: invalid literal for int()` | Already handled by `try/except` | The app already catches this — no action needed |
| `KeyError: 'id'` | Task dictionary is missing a field | Check that every task created by `add_task` has `id`, `title`, and `done` |

---

## Glossary

| Term | Definition |
|---|---|
| **CLI** | Command-Line Interface — a text-based way to interact with a program |
| **Function** | A named, reusable block of code that does a specific job |
| **Dictionary** | A Python data structure that stores key-value pairs, e.g. `{"name": "Alice"}` |
| **List** | A Python data structure that stores an ordered sequence of items |
| **JSON** | A file format for storing structured data as readable text |
| **Loop** | Code that repeats — `while True` loops forever until `break` is called |
| **List comprehension** | A compact Python syntax for building a new list from an existing one |
| **`try / except`** | A way to handle errors gracefully so your program doesn't crash |
| **`if __name__ == "__main__"`** | A Python convention that runs code only when the file is executed directly |
| **Boolean** | A value that is either `True` or `False` |

---

*Happy coding! 🐍 You built a real, working application — that's something to be proud of.*