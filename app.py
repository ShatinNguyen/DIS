from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Oliver:potato@localhost/Chessproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: reduces overhead

db = SQLAlchemy(app)


class ChessGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rated = db.Column(db.Integer)
    created_at = db.Column(db.String(100))
    last_move_at = db.Column(db.String(100))
    turns = db.Column(db.Integer)
    victory_status = db.Column(db.String(100))
    winner = db.Column(db.String(100))
    increment_code = db.Column(db.String(100))
    white_id = db.Column(db.String(100))
    white_rating = db.Column(db.Integer)
    black_id = db.Column(db.String(100))
    black_rating = db.Column(db.Integer)
    moves = db.Column(db.Text)
    opening_eco = db.Column(db.String(10))
    opening_name = db.Column(db.Text)
    opening_ply = db.Column(db.Integer)

    def __repr__(self):
        return '<ChessGame %r>' % self.title

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['inputData']  # This retrieves the data from the form field
    print(data)
    # Example query using the data
    # Suppose we are searching for chess games based on a player's ID
    games = ChessGame.query.filter_by(white_id).all()  # Adjust the filter according to your needs
    print(games)
    # You could then pass these games to a template to display them
    return render_template('results.html', games=games)



@app.route('/white-wins')
def white_wins():
    games = ChessGame.query.filter_by(winner='white').all()
    return render_template('white_wins.html', games=games)

@app.route('/')
def home():
    return render_template('interface.html')


@app.route('/about')
def about():
    return '<h1>About Page</h1>'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
