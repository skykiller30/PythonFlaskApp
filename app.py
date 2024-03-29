from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#newnow = s
#now = datetime.utcnow.strftime("%Y%m%d-%H%M%S")
#now2 = now.strftime('%a %d %b %Y, %I:%M%p')
cst_timezone = pytz.timezone('America/Chicago')


class Todo(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.Text, nullable=False)
    

def __repr__(self):
    return '<Task %r>' % self.id


@app.route('/',methods=['POST', 'GET'])
def index():


    if request.method == 'POST':
        now = datetime.now(cst_timezone).strftime('%A %B %d, %Y @ %I:%M%p')
        
        task_content = request.form['content']

        new_task = Todo(content=task_content, date_created=now)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting your task'
        
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your tasks'
        
    else:
        return render_template('update.html', task=task)
 

if __name__ == "__main__":
    app.run(debug=True)