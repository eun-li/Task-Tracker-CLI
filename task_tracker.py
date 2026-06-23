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