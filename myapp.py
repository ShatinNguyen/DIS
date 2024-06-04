from flask import Flask, render_template, request

import psycopg2


#Columns
#"id" VARCHAR(100)
#"rated" VARCHAR(100)
#"created_at" VARCHAR(100)
#"last_move_at" VARCHAR(100)	
#"turns" INT 	
#"victory_status" VARCHAR(50)
#"winner" VARCHAR(50)	
#"increment_code" VARCHAR(50)
#"white_id" VARCHAR(100) 	
#"white_rating" INT	
#"black_id" VARCHAR(100)
#"black_rating" INT 
#"moves" TEXT	
#"opening_eco" VARCHAR(100)
#"opening_name" VARCHAR(100)
#"opening_ply" INT "



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

@app.route('/search', methods=['GET'])
def search():
    return render_template('results.html')

@app.route('/submit', methods=['POST'])
def submit():
    rating = request.form.get('rating', type=int)
    winner = request.form.get('winner', type=str)
    opening = request.form.get('opening', type=str)

    conn = connection()
    cur = conn.cursor()

    query = "SELECT id, winner, white_id, black_id, white_rating, black_rating, opening_name FROM chess_games WHERE 1=1"
    params = []

    if rating:
        query += " AND (white_rating >= %s OR black_rating >= %s)"  # Assume rating can apply to either player
        params.extend([rating, rating])  # Add rating twice for white and black
    if winner:
        query += " AND winner = %s"
        params.append(winner)
    if opening:
        query += " AND opening_name LIKE %s"  # Use the correct column name
        params.append(f"%{opening}%")  # Allows partial match for flexibility

    cur.execute(query, params)
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
