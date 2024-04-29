from flask import Flask, render_template, request

import psycopg2

#Columns
#     id 
#     rated 
#     created_at 
#     last_move_at 
#     turns 
#     victory_status 
#     winner 
#     increment_code 
#     white_id 
#     white_rating 
#     black_id 
#     black_rating
#     moves
#     opening_eco
#     opening_name
#     opening_ply

app = Flask(__name__)

def connection():
    curr_con = psycopg2.connect(
        dbname="Chessproject",
        user="Oliver",
        password="Potato",
        host="localhost",
        port="5432")
    return curr_con


@app.route('/')
def home():
    return render_template('interface.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['inputData']
    conn = connection()
    cur = conn.cursor()
    print(data)
    cur.execute("SELECT id, winner FROM chess_games WHERE white_rating = %s", (data,))
    games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('results.html', games=games)


@app.route('/white-wins')
def white_wins():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chess_games WHERE winner = 'white'")
    games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('white_wins.html', games=games)



@app.route('/about')
def about():
    return '<h1>About Page</h1>'

if __name__ == "__main__":
    app.run(debug=True)
