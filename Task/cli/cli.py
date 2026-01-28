import requests

skip = 0
limit = 10
search = ""
filter_status = ""
filter_priority = ""
task_id = None
get_all_tasks_url = f"http://localhost:8000/api/v1/tasks/?skip={skip}&limit={limit}"
get_one_task_url = f"http://localhost:8000/api/v1/tasks/{task_id}"
update_task_url = f"http://localhost:8000/api/v1/tasks/{task_id}"
update_priority_url = f"http://localhost:8000/api/v1/tasks/{task_id}/priority"
update_status_url = f"http://localhost:8000/api/v1/tasks/{task_id}/status"
delete_task_url = f"http://localhost:8000/api/v1/tasks/{task_id}"
create_task_url = "http://localhost:8000/api/v1/tasks/"

headers = {
    "Content-Type": "application/json"
}

status_enum_map = {
    1: "pending",
    2: "in_progress",
    3: "completed",
    4: "hold",
    5: "cancelled"
}
pripority_enum_map = {  
    1: "low",
    2: "medium",
    3: "high",
    4: "urgent"
}

def display_menu():
    """
    Display the main menu options.
    """
    print("\nTask Management CLI")
    print("1. Create Task")
    print("2. View All Tasks")
    print("3. View Task by ID")
    print("4. Update Task")
    print("5. Update Task Priority")
    print("6. Update Task Status")
    print("7. Delete Task")
    print("8. Exit")

def dispaly_task(task):
    print(f"ID: {task['id']}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Status: {task['status']}")
    print(f"Priority: {task['priority']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Created At: {task['created_at']}")
    print(f"Updated At: {task['updated_at']}")
    print("-" * 20)

def create_task():
    """
    Create a new task with user input.
    """
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    try:
        while True:
            priority = int(input("Enter task priority (1: low, 2: medium, 3: high, 4: urgent): "))
            if priority in pripority_enum_map:
                priority = pripority_enum_map[priority]
                break
            else:
                print("Invalid priority. Please enter a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        return
    try:
        while True:
            status = int(input("Enter task status (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled): "))
            if status in status_enum_map:
                status = status_enum_map[status]
                break
            else:
                print("Invalid status. Please enter a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return
    due_date = input("Enter due date (YYYY-MM-DDTHH:MM:SS) : ") or None
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "status": status,
        "due_date": due_date
    }

    response = requests.post(create_task_url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Task created successfully!")
        print("Task Details:", response.json())
    else:
        print("Failed to create task. Status Code:", response.status_code)
        print("Response:", response.text)



def getall_tasks():
    """
    Retrieve all tasks with optional search and filtering.
    """
    input_search = input("Enter search term (leave blank for no search): ")
    try:
        while True:
            limit = int(input("Enter number of tasks to retrieve (default 10): ") or "10")
            skip = int(input("Enter number of tasks to skip (default 0): ") or "0")
            if limit < 0 or skip < 0:
                print("Skip and limit must be non-negative integers.")
            else:
                break
    except ValueError:
        print("Invalid input. Please enter valid numbers for skip and limit.")
        return
    try: 
        filter_status = input("Enter task status to filter (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled) or leave blank for no filter: ") 
        if filter_status:
            filter_status = int(filter_status)
            if filter_status in status_enum_map:
                filter_status = status_enum_map[filter_status]
            else:
                print("Invalid status filter. Please enter a number between 1 and 5.")
                return
        else:
            filter_status = ""
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return
    try:
        filter_priority = input("Enter task priority to filter (1: low, 2: medium, 3: high, 4: urgent) or leave blank for no filter: ") 
        if filter_priority:
            filter_priority = int(filter_priority)
            if filter_priority in pripority_enum_map:
                filter_priority = pripority_enum_map[filter_priority]
            else:
                print("Invalid priority filter. Please enter a number between 1 and 4.")
                return
        else:
            filter_priority = ""
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        return
    url = f"http://localhost:8000/api/v1/tasks/?skip={skip}&limit={limit}"
    if input_search:
        url += f"&search={input_search}"
    if filter_status:
        url += f"&filter_status={filter_status}"
    if filter_priority:
        url += f"&filter_priority={filter_priority}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        if tasks:
            for task in tasks:
                dispaly_task(task)
        else:
            print("No tasks found.")
    else:
        print("Failed to retrieve tasks. Status Code:", response.status_code)
        print("Response:", response.text)
        
def get_task_by_id():
    """
    Retrieve task details by ID.
    """
    try:
        task_id = int(input("Enter task ID: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        task = response.json()
        dispaly_task(task)
    elif response.status_code == 404:
        print("Task not found.")
    else:
        print("Failed to retrieve task. Status Code:", response.status_code)
        print("Response:", response.text)
def update_task():
    """
    Update task details by ID.
    """
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return
    title = input("Enter new task title (leave blank to keep unchanged): ")
    description = input("Enter new task description (leave blank to keep unchanged): ")
    due_date = input("Enter new due date (YYYY-MM-DDTHH:MM:SS) (leave blank to keep unchanged): ")
    payload = {}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if due_date:
        payload["due_date"] = due_date
    if not payload:
        print("No updates provided.")
        return
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Task updated successfully!")
        print("Updated Task Details:", response.json())
    elif response.status_code == 404:
        print("Task not found.")
    else:
        print("Failed to update task. Status Code:", response.status_code)
        print("Response:", response.text)
    
def update_task_priority():
    """
    Update task priority by ID.
    """
    try:
        task_id = int(input("Enter task ID to update priority: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return
    try:
        while True:
            priority = int(input("Enter new task priority (1: low, 2: medium, 3: high, 4: urgent): "))
            if priority in pripority_enum_map:
                priority = pripority_enum_map[priority]
                break
            else:
                print("Invalid priority. Please enter a number between 1 and 4.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        return
    payload = {
        "priority": priority
    }
    url = f"http://localhost:8000/api/v1/tasks/{task_id}/priority"
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Task priority updated successfully!")
        print("Updated Task Details:", response.json())
    elif response.status_code == 404:
        print("Task not found.")
    else:
        print("Failed to update task priority. Status Code:", response.status_code)
        print("Response:", response.text)

def update_task_status():
    """
    Update task status by ID.
    """
    try:
        task_id = int(input("Enter task ID to update status: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return
    try:
        while True:
            status = int(input("Enter new task status (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled): "))
            if status in status_enum_map:
                status = status_enum_map[status]
                break
            else:
                print("Invalid status. Please enter a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return
    payload = {
        "status": status
    }
    url = f"http://localhost:8000/api/v1/tasks/{task_id}/status"
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Task status updated successfully!")
        print("Updated Task Details:", response.json())
    elif response.status_code == 404:
        print("Task not found.")
    else:
        print("Failed to update task status. Status Code:", response.status_code)
        print("Response:", response.text)

def delete_task():
    """
    Delete a task by ID.
    """
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return
    url = f"http://localhost:8000/api/v1/tasks/{task_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Task deleted successfully!")
    elif response.status_code == 404:
        print("Task not found.")
    else:
        print("Failed to delete task. Status Code:", response.status_code)
        print("Response:", response.text)
 
def main():
    while True:
        display_menu()
        try:
            choice =int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue
        if choice == 1:
            create_task()
        elif choice == 2:
            getall_tasks()
        elif choice == 3:
            get_task_by_id()
        elif choice == 4:
            update_task()
        elif choice == 5:
            update_task_priority()
        elif choice == 6:
            update_task_status()
        elif choice == 7:
            delete_task()
        elif choice == 8:
            print("Exiting Task Management CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
if __name__ == "__main__":
    main()