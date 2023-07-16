from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://matt@localhost/spelling_bee'
db = SQLAlchemy(app)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True)
    correct = db.Column(db.Integer, default=0)
    incorrect = db.Column(db.Integer, default=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form['word']
        result = request.form['result']
        update_word(word, result)
    
    word = select_word()
    return render_template('index.html', word=word.word)

def select_word():
    max_incorrect = db.session.query(db.func.max(Word.incorrect)).scalar()
    min_incorrect = db.session.query(db.func.min(Word.incorrect)).scalar()
    total_incorrect = db.session.query(db.func.sum(Word.incorrect)).scalar()
    
    # Calculate the probability for each word based on incorrect count
    probabilities = [(max_incorrect - word.incorrect + 1) / (total_incorrect - min_incorrect + Word.query.count()) for word in Word.query.all()]
    
    # Select a word using the calculated probabilities
    word = random.choices(Word.query.all(), probabilities)[0]
    
    # Increase the incorrect count to ask incorrect words more often
    word.incorrect += 1
    
    db.session.commit()
    return word

def update_word(word, result):
    word_obj = Word.query.filter_by(word=word).first()
    if word_obj:
        if result == 'correct':
            word_obj.correct += 1
        else:
            word_obj.incorrect += 1
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
