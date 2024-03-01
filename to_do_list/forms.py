from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SubmitField

class CheckForm(FlaskForm):

    checkbox = BooleanField()

class AddTaskForm(FlaskForm):
    text = StringField("Task: ")
    task_type = RadioField("When you want to complete?", choices=["Today", "This week", "Later"])
    submit = SubmitField("Save")

