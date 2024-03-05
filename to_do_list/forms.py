"""
This module defines the Flask-WTF forms for the application.
Each class represents a form that can be used in a template.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField


class AddTaskForm(FlaskForm):
    """
    Represents a form for adding a new task.

    Attributes:
    text (StringField): A field for the text of the task.
    task_type (RadioField): A field for the type of the task. 
    The choices are "Today", "This week", and "Later".
    submit (SubmitField): A field to submit the form.

    This form is used in the 'add_task' route to get the user's input for a new task.
    """
    text = StringField("Task: ")
    task_type = RadioField("When you want to complete?", choices=["Today", "This week", "Later"])
    submit = SubmitField("Save")
