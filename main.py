from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid warning

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
