import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from to_do_list.forms import CheckForm, AddTaskForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "my_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"data.sqlite")

db = SQLAlchemy(app)

Migrate(app, db)

from to_do_list.models import Task

@app.route('/', methods=['GET', 'POST'])
def index():
    index_page = True
    tasks_id = Task.query.filter_by(my_order=0).order_by(Task.id)
    tasks_today_my_order = Task.query.filter_by(task_type="Today").except_(Task.query.filter_by(my_order=0)).order_by(Task.my_order)
    tasks_week_my_order = Task.query.filter_by(task_type="This week").except_(Task.query.filter_by(my_order=0)).order_by(Task.my_order)
    tasks_later_my_order = Task.query.filter_by(task_type="Later").except_(Task.query.filter_by(my_order=0)).order_by(Task.my_order)
    check_form = CheckForm()
    if check_form.validate_on_submit:
        print(f"check_form.checkbox.data {check_form.checkbox.data}")

    return render_template('index.html',index_page=index_page, tasks_id=tasks_id, tasks_today_my_order=tasks_today_my_order,tasks_week_my_order=tasks_week_my_order, tasks_later_my_order=tasks_later_my_order, check_form=check_form)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = AddTaskForm()

    if form.validate_on_submit():
        new_task = Task(
            text=form.text.data,
            task_type=form.task_type.data
        )
        print(f"form.text.data {form.text.data}")
        print(f"form.task_type.data {form.task_type.data}")
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully")

        return redirect(url_for('index'))

    return render_template('add_task.html', form=form)

@app.route('/save_order', methods=['POST'])
def save_order():
    if request.method == "POST":
        datafromjs = request.form['mydata']
        print(datafromjs)