from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todos(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  complete = db.Column(db.Boolean)
  category = db.Column(db.String(50))

class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String())
  password = db.Column(db.String())

@app.route('/')
def index():
  todos = Todos.query.all()
  return render_template(
    'index.html',
    todos=todos
  )

@app.route('/create', methods=['POST'])
def create():
  title = request.form.get('title')
  cat = request.form.get('category')
  new_todo = Todos(
    title=title,
    category=cat,
    complete=False
  )
  db.session.add(new_todo)
  db.session.commit()
  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  todo = Todos.query.filter_by(id=id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
  todo = Todos.query.filter_by(id=id).first()
  todo.complete = True
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
  title = request.form.get('title')

  todo = Todos.query.filter_by(id=id).first()
  todo.title = title
  db.session.commit()
  
  return redirect('/')

# IMPORTANTE V
if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', port=8080)