from flask import Flask, render_template, request, redirect, url_for

import psycopg2
import re
import uuid

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
def homie():
    return home()

@app.route('/home')
def home():
    return render_template('interface.html')


#search and submits
@app.route('/search', methods=['GET'])
def search():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT MIN(white_rating) AS min_white_rating, MIN(black_rating) AS min_black_rating FROM chess_games;")
    results_min = cur.fetchone()
    min_white, min_black = results_min
    cur.execute("SELECT MAX(white_rating) AS max_white_rating, MAX(black_rating) AS max_black_rating FROM chess_games;")
    results_max = cur.fetchone()
    max_white, max_black = results_max
    cur.execute("SELECT DISTINCT opening_name FROM chess_games ORDER BY opening_name;")
    openings = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('results.html', min_white=min_white, min_black=min_black,max_white=max_white,max_black=max_black,openings=openings)

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
####


#IMPORT AND IMPORTING


def parser(data):
    pattern = re.compile(r"\[([A-Za-z0-9]+)\s+\"(.+?)\"\]")
    metadata = dict(pattern.findall(data))
    stripped_moves = re.sub(r'(\{[^}]*\})|(\([^)]*\))', '', data.split('\n\n', 1)[1]).strip()
    moves = re.sub(r'\d+\.', '', stripped_moves).replace("  ", " ").strip()

    return metadata, moves



#def prep_moves(moves):
#    moves = moves.split()
#    result = []
#    for i in range(len(moves)):
#        curr = []
#        for j in range(i,len(moves)):
#            if moves[i] = int 
#    return result
    

def whowon(fields, moves):
    result = ""
    winner = ""
    if '#' in moves:
        result = "checkmate"
    elif "draw" in moves:
        result = "draw"
    else:
        result= "no winner?"
    data = fields.get("Result", "")
    if '1-0' in data:
        winner = "white"
    elif '0-1' in data:
        winner = "black"
    else:
        winner = "draw"
    return result, winner



def prepare_for_db(fields, moves):
    victory_stats, winner = whowon(fields,moves)
    

    game_data = {
        "id": str(uuid.uuid4()),
        "rated": "True", ##skal fixes
        "created_at": fields.get("Date"),
        "last_move_at": "something",
        "turns": len(moves.split()), 
        "victory_status": whowon(moves),
        "winner": winner,
        "increment_code": "unknown",
        "white_id": fields.get("White", "unknown"),
        "black_id": fields.get("Black", "unknown"),
        "white_rating": fields.get("WhiteElo","unknown"),
        "black_rating": fields.get("BlackElo","unknown"),
        "moves": moves,
        "opening_eco": fields.get("ECO", "unknown"), 
        "opening_name": fields.get("Opening", "unknown"),
        "opening_ply": "unknown"
    }
    return game_data

def insert_game(game_data):
    conn = connection()
    cur = conn.cursor()

    columns = ', '.join(game_data.keys())
    placeholders = ', '.join(['%s'] * len(game_data))
    sql = f"INSERT INTO chess_games ({columns}) VALUES ({placeholders})"
    
    cur.execute(sql, list(game_data.values()))
    conn.commit()
    cur.close()
    conn.close()
    
    
    
@app.route('/import', methods=['GET'])
def import_page():
    return render_template('import.html')


@app.route('/importing', methods=['POST'])
def importing():
    file = request.files.get('pgn_file')
    if file and file.filename != '':
        content = file.read().decode('utf-8')
    else:
        content = request.form.get('pgn_text', '')  

    fields, moves = parser(content)
    game_data = prepare_for_db(fields, moves)
    insert_game(game_data)

    print("Success")
    return redirect(url_for('import_page'))

##

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

if __name__ == "__main__":
    app.run(debug=True)
