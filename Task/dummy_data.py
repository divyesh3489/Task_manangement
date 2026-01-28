import json
from datetime import datetime
from db.session import SessionLocal
from models.task import Task, StatusEnum, PriorityEnum

def create_dummy_tasks():
    """
    Create and add dummy tasks to the database for testing purposes.
    """

    with open("dummy_data.json") as f:
        tasks_data = json.load(f)

    for data in tasks_data["tasks"]:
        task = Task(
            title=data["title"],
            description=data.get("description"),
            status=StatusEnum(data.get("status", "pending")),
            priority=PriorityEnum(data.get("priority", "medium")),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
        )
        db = SessionLocal()
        db.add(task)
        db.commit()
        db.refresh(task)
        db.close()
    print("Dummy data added to the database.")

if __name__ == "__main__":
    create_dummy_tasks()

