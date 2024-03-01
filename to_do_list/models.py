from to_do_list import db

class Task(db.Model):
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