## Task Management API with CLI Interface

This project involves building a RESTful Task Management system that includes both an API backend and a command-line interface (CLI) for user interaction.

## Software Requirements
- Python 3.8 or higher
- SQLite (or any database of your choice)

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/divyesh3489/Task_manangement.git
   cd Task_manangement
   ```
2. Create a virtual environment:
   ```
    python -m venv venv
    use ".\venv\Scripts\activate" on Windows or "source ./venv/bin/activate" on macOS/Linux
    ```
3. Install dependencies:
   ```
    pip install -r requirements.txt
    ```
4. Apply database migrations (if applicable):
   ```
    cd Task
    alembic upgrade head
    ```
5. Insert Dummy Data (optional):
   ```
    python dummy_data.py
    ```
6. Run the API server:
   ```
    python main.py
    ```
7. Access the API documentation at
    ```
    http://localhost:8000/docs
    ```

## API Endpoint Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints
- `GET /tasks/` : List all tasks with optional filtering and searching 
    - `Query Parameters`:
        - `skip`: Number of tasks to skip for pagination (default: 0)
        - `limit`: Maximum number of tasks to return (default: 10)
        - `status`: Filter by task status (panding, in-progress, completed,canceled, Hold)
        - `priority`: Filter by priority level (low, medium, high, urgent)
        - `search`: Search tasks by title or description

- `GET /tasks/{task_id}` : Retrieve a task by ID
    - `Path Parameters`:
        - `task_id`: ID of the task to retrieve 
- `POST /tasks/` : Create a new task
    - `Request Body`:
        - `title`: Title of the task (string, required)
        - `description`: Description of the task (string, optional)
        - `due_date`: Due date of the task (datetime, optional)
        - `priority`: Priority level of the task (string: low, medium, high, urgent; default: medium)
- `PUT /tasks/{task_id}` : Update a task by ID
    - `Path Parameters`:
        - `task_id`: ID of the task to update
    - `Request Body`:
        - `title`: Updated title of the task (string, optional)
        - `description`: Updated description of the task (string, optional)
        - `due_date`: Updated due date of the task (datetime, optional)
        - `priority`: Updated priority level of the task (string: low, medium, high, urgent; optional)
- `PATCH /tasks/{task_id}/status` : Mark task as complete/incomplete
    - `Path Parameters`:
        - `task_id`: ID of the task to update
    - `Request Body`:
        - `status`: New status of the task (string: pending, in-progress, completed, canceled, Hold)
- `PATCH /tasks/{task_id}/priority` : Update task priority
    - `Path Parameters`:
        - `task_id`: ID of the task to update
    - `Request Body`:
        - `priority`: New priority level of the task (string: low, medium, high, urgent)
- `DELETE /tasks/{task_id}` : Delete a task by ID
    - `Path Parameters`:
        - `task_id`: ID of the task to delete
    

## CLI Usage Examples

### Starting the CLI
```
python cli/cli.py
```

### 1. Create a New Task
```
Task Management CLI
1. Create Task
2. View All Tasks
3. View Task by ID
4. Update Task
5. Update Task Priority
6. Update Task Status
7. Delete Task
8. Exit
Enter your choice: 1

Enter task title: Finish the quarterly report
Enter task description: Complete the annual report and submit by end of the week
Enter task priority (1: low, 2: medium, 3: high, 4: urgent): 3
Enter task status (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled): 2
Enter due date (YYYY-MM-DDTHH:MM:SS): 2026-01-31T17:00:00

Task created successfully!
Task Details: {
  "id": 1,
  "title": "Finish the quarterly report",
  "description": "Complete the annual report and submit by end of the week",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2026-01-31T17:00:00",
  "is_completed": false,
  "created_at": "2026-01-28T10:30:00",
  "updated_at": "2026-01-28T10:30:00"
}
```

### 2. View All Tasks
```
Enter your choice: 2

Enter search term (leave blank for no search): 
Enter number of tasks to retrieve (default 10): 10
Enter number of tasks to skip (default 0): 0
Enter task status to filter (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled) or leave blank for no filter: 
Enter task priority to filter (1: low, 2: medium, 3: high, 4: urgent) or leave blank for no filter: 

ID: 1
Title: Finish the quarterly report
Description: Complete the annual report and submit by end of the week
Status: in_progress
Priority: high
Due Date: 2026-01-31T17:00:00
Created At: 2026-01-28T10:30:00
Updated At: 2026-01-28T10:30:00
--------------------
ID: 2
Title: Review code changes
Description: Review pull requests and provide feedback
Status: pending
Priority: medium
Due Date: 2026-02-05T12:00:00
Created At: 2026-01-28T10:35:00
Updated At: 2026-01-28T10:35:00
--------------------
```

### 3. View Task by ID
```
Enter your choice: 3

Enter task ID: 1

ID: 1
Title: Finish the quarterly report
Description: Complete the annual report and submit by end of the week
Status: in_progress
Priority: high
Due Date: 2026-01-31T17:00:00
Created At: 2026-01-28T10:30:00
Updated At: 2026-01-28T10:30:00
--------------------
```

### 4. Filter Tasks by Status
```
Enter your choice: 2

Enter search term (leave blank for no search): 
Enter number of tasks to retrieve (default 10): 10
Enter number of tasks to skip (default 0): 0
Enter task status to filter (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled) or leave blank for no filter: 3
Enter task priority to filter (1: low, 2: medium, 3: high, 4: urgent) or leave blank for no filter: 

ID: 5
Title: Deploy to production
Description: Deploy latest version to production servers
Status: completed
Priority: urgent
Due Date: 2026-01-29T09:00:00
Created At: 2026-01-27T14:20:00
Updated At: 2026-01-28T08:15:00
--------------------
```

### 5. Search Tasks
```
Enter your choice: 2

Enter search term (leave blank for no search): report
Enter number of tasks to retrieve (default 10): 10
Enter number of tasks to skip (default 0): 0
Enter task status to filter (1: pending, 2: in_progress, 3: completed, 4: hold, 5: cancelled) or leave blank for no filter: 
Enter task priority to filter (1: low, 2: medium, 3: high, 4: urgent) or leave blank for no filter: 

ID: 1
Title: Finish the quarterly report
Description: Complete the annual report and submit by end of the week
Status: in_progress
Priority: high
Due Date: 2026-01-31T17:00:00
Created At: 2026-01-28T10:30:00
Updated At: 2026-01-28T10:30:00
--------------------
```




## Assumptions Made
- The API uses SQLite for data persistence, but it can be configured to use other databases.
- Basic validation is implemented for task data, including required fields and valid status/priority values.
- The CLI interface is designed to perform CRUD operations and display tasks in a readable format.
- Error handling is implemented to manage edge cases, such as attempting to retrieve or update non-existent tasks.
- The API follows RESTful principles and uses appropriate HTTP status codes for responses.
- All timestamps are stored in UTC format and response given in UTC.

## Requirements.txt File
```
fastapi
uvicorn
sqlalchemy
pydantic
alembic
pydantic-settings
requests
```