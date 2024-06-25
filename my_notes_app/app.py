from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/post_note', methods=['GET', 'POST'])
def post_note():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        new_note = Note(name=name, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_note.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
