"""
This module defines the SQLAlchemy models for the application.
Each class represents a table in the database.
"""
from to_do_list import db

class Task(db.Model):
    """
    Represents a task in the to-do list.

    Attributes:
    id (int): The primary key of the task.
    checked (bool): A boolean indicating whether the task is checked off.
    text (str): The text of the task.
    my_order (int): The order of the task in the to-do list.
    task_type (str): The type of the task.

    Methods:
    __init__(self, text, task_type): Initializes a new instance of the Task class.
    __repr__(self): Returns a string representation of the Task instance.
    """
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    checked = db.Column(db.Boolean)
    text = db.Column(db.Text)
    my_order = db.Column(db.Integer)
    task_type = db.Column(db.String)

    def __init__(self, text, task_type) -> None:
        self.checked = False
        self.text = text
        self.my_order = 0
        self.task_type = task_type

    def __repr__(self) -> str:
        return f" Task id: {self.id}. Task text: {self.text}"
