"""
This module initializes the Flask application and its extensions.
It also defines several routes and utility functions for the application.

It includes the following:

- Configuration of the Flask application and SQLAlchemy.
- Definition of the `get_tasks` utility function.
- Definition of the `index`, `add_task`, `save_order`, and `update_task` routes.

This module is the entry point for the application.
"""

import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from to_do_list.forms import AddTaskForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)

db = SQLAlchemy(app)

Migrate(app, db)

from to_do_list.models import Task


def get_tasks(task_type, checked=False):
    """
    Returns a query for tasks based on the task type and checked status.

    Parameters:
    task_type (str): The type of the task. Can be "id", "Today", "This week", or "Later".
    checked (bool): The checked status of the task. Default is False.

    Returns:
    SQLAlchemy Query: A query for tasks that match the specified type and checked status.
    """
    if task_type == "id" and not checked:
        return Task.query.filter_by(my_order=0, checked=checked).order_by(Task.id)
    elif task_type == "id" and checked:
        return Task.query.filter_by(checked=checked).order_by(Task.id)
    else:
        return (
            Task.query.filter_by(task_type=task_type, checked=checked)
            .except_(Task.query.filter_by(my_order=0))
            .order_by(Task.my_order)
        )


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The index route that renders the index page.

    Returns:
    str: The rendered template for the index page.
    """
    index_page = True
    tasks_id = get_tasks("id")
    tasks_today_my_order = get_tasks("Today")
    tasks_week_my_order = get_tasks("This week")
    tasks_later_my_order = get_tasks("Later")
    tasks_completed = get_tasks("id", True)

    return render_template(
        "index.html",
        index_page=index_page,
        tasks_id=tasks_id,
        tasks_today_my_order=tasks_today_my_order,
        tasks_week_my_order=tasks_week_my_order,
        tasks_later_my_order=tasks_later_my_order,
        tasks_completed=tasks_completed,
    )


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    """
    Route for adding a new task. If the form is valid on submission,
    a new task is created and added to the database.

    Returns:
    str: The rendered template for the 'add_task' page if the form is not valid or if the request method is 'GET'.
         If the form is valid and the request method is 'POST', a redirect response to the 'index' page is returned.
    """
    form = AddTaskForm()

    if form.validate_on_submit():
        new_task = Task(text=form.text.data, task_type=form.task_type.data)
        print(f"form.text.data {form.text.data}")
        print(f"form.task_type.data {form.task_type.data}")
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully")

        return redirect(url_for("index"))

    return render_template("add_task.html", form=form)


@app.route("/save_order", methods=["POST"])
def save_order():
    """
    Route for saving the order of tasks.
    The order and group of tasks are received as JSON in the request.
    The order and group of each task are updated in the database.

    Returns:
    str, int: An empty response with a 204 status code, indicating that the request has succeeded
    but there's no additional content to send in the response body.
    """
    group_to_task_type = {
        "box-today": "Today",
        "box-week": "This week",
        "box-later": "Later",
    }
    task_order = request.get_json()
    for group, tasks in task_order.items():
        for task_index, task_id in enumerate(tasks, 1):
            task = Task.query.get(task_id)
            task.my_order = task_index
            task.task_type = group_to_task_type[group]
    db.session.commit()
    return "", 204


@app.route("/update_task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Route for updating the checked status of a task.
    The task to be updated is identified by the task_id in the URL.

    Parameters:
    task_id (int): The ID of the task to be updated.

    Returns:
    str, int: An empty response with a 204 status code, indicating that the request has succeeded
    but there's no additional content to send in the response body.
    """
    task = Task.query.get(task_id)
    task.checked = not task.checked
    db.session.commit()
    return "", 204
