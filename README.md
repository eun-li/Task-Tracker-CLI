# Building a Task Tracker CLI with Python
### A Beginner's Step-by-Step Guide

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Overview](#project-overview)
4. [Setting Up Your Project](#setting-up-your-project)
5. [Core Concepts You Will Learn](#core-concepts-you-will-learn)
6. [Building the App Step by Step](#building-the-app-step-by-step)
   - [Step 1: Imports](#step-1-imports)
   - [Step 2: The Constant](#step-2-the-constant)
   - [Step 3: How Tasks Are Stored](#step-3-how-tasks-are-stored)
   - [Step 4: Loading Tasks from the File](#step-4-loading-tasks-from-the-file)
   - [Step 5: Saving Tasks to the File](#step-5-saving-tasks-to-the-file)
   - [Step 6: Adding a Task](#step-6-adding-a-task)
   - [Step 7: Listing All Tasks](#step-7-listing-all-tasks)
   - [Step 8: Completing a Task](#step-8-completing-a-task)
   - [Step 9: Deleting a Task](#step-9-deleting-a-task)
   - [Step 10: The Menu Display](#step-10-the-menu-display)
   - [Step 11: The Main Loop](#step-11-the-main-loop)
   - [Step 12: The Entry Point](#step-12-the-entry-point)
7. [Full Source Code](#full-source-code)
8. [Running Your App](#running-your-app)
9. [Example Session](#example-session)
10. [Exercises to Go Further](#exercises-to-go-further)
11. [Common Errors and Fixes](#common-errors-and-fixes)
12. [Glossary](#glossary)

---

## Introduction

A **Task Tracker CLI** (Command-Line Interface) is a program you run in your terminal to manage a to-do list. You can add tasks, mark them as done, delete them, and view them, all without leaving the command line.

This project is well suited for beginners because it touches many of the skills you need for real Python work:

- Organizing code into functions
- Reading input from a user
- Using lists and dictionaries to structure data
- Reading from and writing to a file so data is not lost when the program closes

By the end of this guide you will have a working, usable application you built yourself.

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.8 or higher** installed. Check by running one of these commands in your terminal:

  ```bash
  python --version
  ```

  or

  ```bash
  python3 --version
  ```

  You should see output like `Python 3.11.0`.

- A **text editor or IDE**. Recommended options for beginners:
  - [VS Code](https://code.visualstudio.com/) (free, beginner-friendly)
  - [PyCharm Community](https://www.jetbrains.com/pycharm/download/) (free)
  - Even a plain text editor like Notepad works for small projects.

- Basic familiarity with opening a terminal or command prompt.

No prior Python knowledge is required. Every concept is explained when it appears.

---

## Project Overview

Here is what the finished app can do:

| Option | What It Does |
|--------|--------------|
| Add a task | Creates a new task with a title you type in |
| List tasks | Prints all tasks with their status (done or pending) |
| Complete a task | Marks one task as done |
| Delete a task | Removes a task permanently |
| Quit | Exits the program |

Tasks are stored in a file called `tasks.json`. This means your tasks survive even after you close the terminal.

---

## Setting Up Your Project

Create a new folder for your project and navigate into it:

```bash
mkdir task_tracker
cd task_tracker
```

Inside this folder you will work with two files:

```
task_tracker/
├── task_tracker.py   <-- the main Python file you write
└── tasks.json        <-- created automatically when you add your first task
```

No third-party packages need to be installed. This project uses only Python's standard library.

---

## Core Concepts You Will Learn

### Functions

A function is a reusable block of code with a name. You define it once with `def` and call it by name whenever you need it.

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")   # output: Hello, Alice!
greet("Bob")     # output: Hello, Bob!
```

Without functions you would have to copy and paste the same code everywhere it is needed. A function lets you write it once and reuse it freely.

### Lists

A list is an ordered collection of items. You can add items, remove items, and loop over them.

```python
fruits = ["apple", "banana", "cherry"]

fruits.append("date")   # adds to the end
print(fruits[0])        # prints "apple" (index 0 is the first item)
```

### Dictionaries

A dictionary stores values under named keys, like a real dictionary where a word maps to its definition.

```python
task = {
    "id":    1,
    "title": "Buy groceries",
    "done":  False
}

print(task["title"])   # prints "Buy groceries"
```

### JSON Files

JSON (JavaScript Object Notation) is a text format for storing structured data. Python's built-in `json` module converts between Python objects and JSON text.

```python
import json

# Writing data to a file
with open("data.json", "w") as f:
    json.dump({"name": "Alice", "age": 30}, f)

# Reading data back
with open("data.json", "r") as f:
    data = json.load(f)

print(data["name"])   # prints "Alice"
```

### The os Module

The `os` module lets your program interact with the operating system. The most useful thing it gives us here is the ability to check whether a file exists before trying to open it.

```python
import os

if os.path.exists("tasks.json"):
    print("The file is there.")
else:
    print("No file yet.")
```

---

## Building the App Step by Step

### Step 1: Imports

Open a new file called `task_tracker.py` and add these two lines at the very top:

```python
import json
import os
```

`import` makes a module available to your code. These two modules are all we need for this project. They come with Python, so there is nothing extra to install.

---

### Step 2: The Constant

Right below the imports, add:

```python
TASK_FILE = "tasks.json"
```

This is a **constant** -- a variable that is set once and never changed. By convention, Python programmers write constants in ALL_CAPS so anyone reading the code knows not to modify them.

Storing the filename as a constant is good practice. If you ever decide to rename the file, you change it in exactly one place and the entire program updates automatically.

---

### Step 3: How Tasks Are Stored

Before writing any functions, it helps to understand what the data looks like.

Each task is a Python dictionary:

```python
{
    "id":    1,
    "title": "Buy groceries",
    "done":  False
}
```

| Key | Type | Meaning |
|-----|------|---------|
| `"id"` | Integer | A unique number that identifies this task |
| `"title"` | String | The description the user typed |
| `"done"` | Boolean (`True` / `False`) | Whether the task has been completed |

All tasks are kept together in a list:

```python
[
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book",   "done": True}
]
```

This list is what gets saved to -- and loaded from -- `tasks.json`.

---

### Step 4: Loading Tasks from the File

```python
def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    return []
```

**Breaking this down line by line:**

`if os.path.exists(TASK_FILE):`
On the very first run of the program, the file does not exist yet. This check prevents Python from crashing when it tries to open a file that is not there.

`with open(TASK_FILE, "r") as f:`
This opens the file in read mode (`"r"`) and gives us a file handle called `f`. The `with` keyword automatically closes the file when the indented block finishes -- even if something goes wrong inside. This is safer than calling `f.close()` yourself.

`content = f.read().strip()`
`f.read()` returns the entire file contents as one long string. `.strip()` removes any invisible characters (spaces, newlines) from the start and end of the string.

`if not content: return []`
If the file exists but is empty, `content` will be an empty string `""`. Calling `json.loads("")` would crash, so we return an empty list early instead.

`return json.loads(content)`
`json.loads()` (note the "s" for "string") converts JSON text back into a Python object -- in our case a list of dictionaries.

`return []` (at the bottom, outside the `if`)
If the file does not exist at all, this line runs and returns an empty list. The rest of the program will always have a list to work with.

---

### Step 5: Saving Tasks to the File

```python
def save_tasks(tasks):
    """Save the list of tasks to the JSON file."""
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
```

`open(TASK_FILE, "w")`
Opening a file in write mode (`"w"`) does two things: if the file already exists, its contents are erased; if it does not exist, Python creates it. Either way, we get a clean file to write into.

`json.dump(tasks, f, indent=4)`
`json.dump()` converts the Python list into JSON text and writes it directly into the file `f`. The `indent=4` argument formats the output with four spaces of indentation so the file is human-readable when you open it in a text editor.

---

### Step 6: Adding a Task

```python
def add_task(title):
    """Add a new task with the given title."""
    tasks = load_tasks()

    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id":    new_id,
        "title": title,
        "done":  False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: [{new_id}] {title}")
```

**The unique ID line in detail:**

```python
new_id = max((task["id"] for task in tasks), default=0) + 1
```

Reading from the inside out:

- `task["id"] for task in tasks` is a **generator expression**. It is like a compact for-loop that yields one value per task: its ID number.
- `max(...)` finds the largest of those values.
- `default=0` tells `max` what to return if the list is empty (so there are no IDs to compare). With an empty list the max is treated as 0, so the first task gets ID 1.
- `+ 1` makes the new ID one higher than the current maximum.

This approach means IDs are always unique and always increase, even if you delete tasks in the middle.

**f-strings:**

```python
print(f"Task added: [{new_id}] {title}")
```

The `f` before the opening quote makes this an f-string. Anything inside curly braces `{}` is replaced by the value of that variable when the string is printed.

---

### Step 7: Listing All Tasks

```python
def list_tasks():
    """List all tasks."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks added yet.")
        return

    print("\n Your Tasks:")
    print("-" * 35)
    for task in tasks:
        status = ">" if task["done"] else "<"
        print(f"  {status} [{task['id']}] {task['title']}")
    print("-" * 35)
    print()
```

**`if not tasks:`**
In Python, an empty list is "falsy", meaning it is treated as `False` in a boolean check. So `if not tasks:` is a clean way to say "if the list is empty". If it is empty, we print a message and `return` to exit the function early.

**`"-" * 35`**
Python lets you multiply a string by a number to repeat it. This creates a line of 35 dashes as a visual divider.

**The ternary expression:**

```python
status = ">" if task["done"] else "<"
```

This is a compact if/else on one line. Read it as: "set `status` to `>` if the task is done, otherwise set it to `<`." It is exactly equivalent to:

```python
if task["done"]:
    status = ">"
else:
    status = "<"
```

Use whichever form you find easier to read.

---

### Step 8: Completing a Task

```python
def complete_task(task_id):
    """Mark a task done."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task [{task_id}] is already done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"Task [{task_id}] marked as complete.")
            return

    print(f"No task found with id {task_id}.")
```

**Walking through the logic:**

1. Load the current list of tasks.
2. Loop through every task.
3. When we find the task whose `id` matches `task_id`, check whether it is already done.
   - If it is already done, tell the user and stop.
   - If it is not done yet, set `done` to `True`, save the updated list, and confirm to the user.
4. `return` exits the function immediately. Without it the loop would keep running after finding the task, which wastes time and could cause bugs.
5. If the loop finishes without finding a match, we print an error message.

---

### Step 9: Deleting a Task

```python
def delete_task(task_id):
    """Remove a task permanently by id."""
    tasks = load_tasks()

    original_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) == original_count:
        print(f"No task found with id {task_id}.")
    else:
        save_tasks(tasks)
        print(f"Task [{task_id}] deleted.")
```

**The list comprehension:**

```python
tasks = [task for task in tasks if task["id"] != task_id]
```

A **list comprehension** is a shorthand for building a new list. This one creates a list of every task whose ID is *not equal to* `task_id`. The task we want to delete is simply left out.

The long-form version of the same thing:

```python
new_list = []
for task in tasks:
    if task["id"] != task_id:
        new_list.append(task)
tasks = new_list
```

**Detecting whether a task was found:**

We store the list length before the comprehension (`original_count`) and compare it to the length after. If they are equal, nothing was removed -- so the ID the user entered did not match any task. If the length decreased by one, the deletion succeeded.

---

### Step 10: The Menu Display

```python
def show_menu():
    """Display the menu."""
    print("\n=== Task Tracker ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Quit")
    print("====================")
```

This is a simple function with no parameters. Its only job is to print the menu. Putting these print statements in their own function keeps the main loop clean -- instead of repeating all five lines every time, we call `show_menu()` once.

The `\n` at the start of the first string is a newline character. It inserts a blank line before the menu header, which helps the output look less cramped.

---

### Step 11: The Main Loop

```python
def run():
    """Main loop: show the menu and handle user choices."""
    print("Welcome to the main menu.")

    while True:
        show_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("Title cannot be empty.")

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter task id to complete: "))
                complete_task(task_id)
            except ValueError:
                print("Enter a valid number.")

        elif choice == "4":
            list_tasks()
            try:
                task_id = int(input("Enter the task id to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Enter a valid number.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
```

**`while True:`**

This creates an infinite loop. The body of the loop runs, then starts again, then starts again -- forever. The only way to exit is the `break` statement inside the `elif choice == "5":` branch.

**`input(...).strip()`**

`input()` pauses the program and waits for the user to type something and press Enter. The result is always a string. `.strip()` removes any accidental spaces before or after what the user typed. Without it, typing `" 1 "` (with spaces) would not match `"1"` and the program would print "Invalid choice."

**`try / except ValueError:`**

When the user needs to enter a task ID, we call `int()` to convert their string input to a number. If they type `"abc"` instead of a number, `int()` raises a `ValueError`. Without a `try / except`, the program would crash. With it, we catch the error and print a friendly message instead.

**`elif`**

`elif` is short for "else if". Python checks each condition in order and runs only the first one that is True. If none match, the final `else` runs.

---

### Step 12: The Entry Point

```python
if __name__ == "__main__":
    run()
```

When Python runs a file, it sets a special built-in variable called `__name__`. If you run the file directly (for example, `python task_tracker.py`), Python sets `__name__` to the string `"__main__"`. If another Python file imports this one, `__name__` is set to the module's filename instead.

This check means: only start the program if this file was run directly. It is a standard pattern you will see in nearly every Python project.

---

## Full Source Code

Here is the complete `task_tracker.py` file:

```python
import json
import os

TASK_FILE = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    return []


def save_tasks(tasks):
    """Save the list of tasks to the JSON file."""
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(title):
    """Add a new task with the given title."""
    tasks = load_tasks()
    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {
        "id":    new_id,
        "title": title,
        "done":  False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: [{new_id}] {title}")


def list_tasks():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks added yet.")
        return
    print("\n Your Tasks:")
    print("-" * 35)
    for task in tasks:
        status = ">" if task["done"] else "<"
        print(f"  {status} [{task['id']}] {task['title']}")
    print("-" * 35)
    print()


def complete_task(task_id):
    """Mark a task done."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task [{task_id}] is already done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"Task [{task_id}] marked as complete.")
            return
    print(f"No task found with id {task_id}.")


def delete_task(task_id):
    """Remove a task permanently by id."""
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == original_count:
        print(f"No task found with id {task_id}.")
    else:
        save_tasks(tasks)
        print(f"Task [{task_id}] deleted.")


def show_menu():
    """Display the menu."""
    print("\n=== Task Tracker ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Quit")
    print("====================")


def run():
    """Main loop: show the menu and handle user choices."""
    print("Welcome to the main menu.")
    while True:
        show_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("Title cannot be empty.")

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter task id to complete: "))
                complete_task(task_id)
            except ValueError:
                print("Enter a valid number.")

        elif choice == "4":
            list_tasks()
            try:
                task_id = int(input("Enter the task id to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Enter a valid number.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run()
```

---

## Running Your App

Open your terminal, navigate into your project folder, and run:

```bash
python task_tracker.py
```

On some systems (particularly macOS and Linux) you may need:

```bash
python3 task_tracker.py
```

---

## Example Session

The `>` symbol means the task is done. The `<` symbol means it is still pending.

```
Welcome to the main menu.

=== Task Tracker ===
1. Add task
2. List tasks
3. Complete a task
4. Delete a task
5. Quit
====================
Enter choice (1-5): 1
Enter task title: Buy groceries
Task added: [1] Buy groceries

Enter choice (1-5): 1
Enter task title: Write Python docs
Task added: [2] Write Python docs

Enter choice (1-5): 2

 Your Tasks:
-----------------------------------
  < [1] Buy groceries
  < [2] Write Python docs
-----------------------------------

Enter choice (1-5): 3

 Your Tasks:
-----------------------------------
  < [1] Buy groceries
  < [2] Write Python docs
-----------------------------------
Enter task id to complete: 1
Task [1] marked as complete.

Enter choice (1-5): 2

 Your Tasks:
-----------------------------------
  > [1] Buy groceries
  < [2] Write Python docs
-----------------------------------

Enter choice (1-5): 5
Goodbye!
```

---

## Exercises to Go Further

Once your basic app is working, try these challenges to deepen your understanding.

**Beginner**
- Add a "due date" field to each task. Store it as a string in the format `"2025-12-31"`.
- When listing tasks, separate done tasks from pending ones with different headers.

**Intermediate**
- Add a "priority" field (low, medium, high) and sort tasks by priority when listing them.
- Add filtering options: show only pending tasks, or only completed ones.
- Add an "edit" option that lets the user change a task's title.

**Advanced**
- Replace the numbered menu with command-line arguments using Python's `argparse` module. For example: `python task_tracker.py add "Buy milk"`.
- Add timestamps using Python's `datetime` module: record when each task was created and when it was completed.
- Add color to the output using the `colorama` library (`pip install colorama`).

---

## Common Errors and Fixes

| Error message | Likely cause | How to fix it |
|---------------|--------------|---------------|
| `SyntaxError` | Typo in the code | Read the error carefully -- it shows the line number. Look for missing colons, quotes, or parentheses. |
| `FileNotFoundError` | Terminal is in the wrong directory | Make sure your terminal is inside the `task_tracker` folder when you run the script. |
| `json.decoder.JSONDecodeError` | `tasks.json` contains invalid content | Delete `tasks.json` and let the app create a new one on the next run. |
| `ValueError: invalid literal for int()` | User typed letters where a number was expected | This is already handled by the `try / except` blocks in `run()`. No action needed. |
| `KeyError: 'id'` | A task dictionary is missing a field | Check that every task created by `add_task` has `"id"`, `"title"`, and `"done"`. |

---

## Glossary

| Term | Definition |
|------|------------|
| CLI | Command-Line Interface -- a text-based way to interact with a program through a terminal |
| Function | A named, reusable block of code that does a specific job, defined with `def` |
| Parameter | A variable that a function receives as input when it is called |
| Dictionary | A Python data structure that stores key-value pairs, for example `{"name": "Alice"}` |
| List | A Python data structure that stores an ordered sequence of items |
| JSON | A text file format for storing structured data in a human-readable way |
| Constant | A variable whose value never changes; written in ALL_CAPS by convention |
| Loop | Code that repeats; `while True` loops forever until a `break` statement exits it |
| Generator expression | A compact syntax for producing a sequence of values one at a time, without building a full list in memory |
| List comprehension | A compact syntax for building a new list from an existing one, often with a filter condition |
| `try / except` | A way to handle errors gracefully so the program does not crash on bad input |
| Boolean | A value that is either `True` or `False` |
| `if __name__ == "__main__"` | A Python convention that runs code only when the file is executed directly, not when imported |
| f-string | A string prefixed with `f` where `{variable}` placeholders are replaced with their values at runtime |
| `.strip()` | A string method that removes leading and trailing whitespace |