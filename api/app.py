# import necessary modules
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialize your app
app = Flask(__name__)
# configure the database URI for SQLite to a relative path named test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initializing the database
db = SQLAlchemy(app)

# create a class with variables that will create columns for id, content, and date created in the database


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def formatted_date(self):
        return self.date_created.strftime('%Y-%m-%d ')

# creating routes


@app.route("/", methods=["POST", "GET"])
def index():
    with app.app_context():  # Use app.app_context() to handle the application context
        db.create_all()  # Create the database tables if not already created
    if request.method == "POST":
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding this task"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_remove = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_remove)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting that task."


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating that task."
    else:
        return render_template("update.html", task=task)


if __name__ == '__main__':
    app.run(debug=True)
