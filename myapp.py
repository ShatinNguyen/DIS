from flask import Flask, render_template, request, redirect, url_for


import re
import psycopg2
import re
import uuid
import random
import string

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
        dbname="chessproject",
        user="shatinnguyen",
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
    return render_template('results.html', min_white=min_white, min_black=min_black,max_white=max_white,max_black=max_black,openings=openings,enumerate=enumerate)

@app.route('/submit', methods=['POST'])
def submit():
    game_id = request.form.get('GameID', type=str)
    moves = request.form.get('Moves', type=str)
    rating = request.form.get('rating', type=int)
    winner = request.form.get('winner', type=str)
    opening = request.form.get('opening', type=str)
    conn = connection()
    cur = conn.cursor()
    
    query = "SELECT id, winner, white_id, black_id, white_rating, black_rating, opening_name, moves FROM chess_games WHERE 1=1"
    params = []
    filters_applied = False
    
    if game_id:
        query += " AND id ILIKE %s"
        params.append(f"%{game_id}%")
        filters_applied = True
    
    if rating:
        query += " AND (white_rating >= %s OR black_rating >= %s)"
        params.extend([rating, rating])
        filters_applied = True
        
    if winner:
        query += " AND winner = %s"
        params.append(winner)
        filters_applied = True
        
    if opening:
        query += " AND opening_name LIKE %s"
        params.append(f"%{opening}%")
        filters_applied = True
    
    if filters_applied:
        cur.execute(query, params)
        games = cur.fetchall()
        games_filtered = []

        for i in range(len(games)):
            if filterWinner(games[i][1]) & filterGameID(games[i][0]) & filterMoves(games[i][7]):
                games_filtered.append(games[i])
            
        if games_filtered:
            moves = [game[-1] for game in games]
            white_moves, black_moves = sortMoves([(move,) for move in moves])
        
        else:
            white_moves, black_moves = [], []
    else:
        games_filtered, white_moves, black_moves = [], [], []

    cur.close()
    conn.close()

    return render_template('results.html', enumerate=enumerate, 
        games=games_filtered, 
        white_moves=white_moves, 
        black_moves=black_moves,
    )

def filterWinner(winner):
    if re.search("white|black", winner, re.IGNORECASE):
        return True
    else:
        return False
    

def filterGameID(id):
    if re.search("^[a-zA-Z0-9]{8}$", id):
        return True
    else:
        return False
    
def filterMoves(moves):
    if re.match("^(\s*(?:[PNBRQK]?[a-h]?[1-8]?[x-]?[a-h][1-8][+#]?|O-O-O|O-O)\s*)+$", moves):
        return True
    else:
        return False

def sortMoves(moves):
    white_moves = []
    black_moves = []
    for move_set in moves:
        move_list = move_set[0].split()
        white_temp = []
        black_temp = []
        for index, move in enumerate(move_list):
            if index % 2 == 0:
                white_temp.append(move)
            else:
                black_temp.append(move)
        white_moves.append(white_temp)
        black_moves.append(black_temp)
    return white_moves, black_moves


@app.route('/dataset')
def dataset():
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT id, winner, white_id, black_id, white_rating, black_rating, opening_name, moves FROM chess_games")
    games = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('dataset.html', enumerate=enumerate, 
        games=games, 
    )



@app.route('/delete', methods=['GET', 'POST'])
def delete_game():
    if request.method == 'POST':
        game_id = request.form.get('delete_game')
        conn = connection()
        cur = conn.cursor()

        query = "DELETE FROM chess_games WHERE id = %s"
        cur.execute(query, (game_id,))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()

        if affected_rows > 0:
            message = f"Game with ID {game_id} has been successfully deleted."
            success = True
        else:
            message = f"Game with ID {game_id} was not found."
            success = False

        return render_template('delete.html', message=message, success=success)
    else:
        return render_template('delete.html')



@app.route('/update', methods=['GET', 'POST'])
def update_game():
    if request.method == 'POST':
        game_id = request.form.get('update_game')
        new_winner = request.form.get('new_winner')
        conn = connection()
        cur = conn.cursor()

        query = "UPDATE chess_games SET winner = %s WHERE id = %s"
        cur.execute(query, (new_winner, game_id))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()

        if affected_rows > 0:
            message = f"Game with ID {game_id} has been successfully updated."
            success = True
        else:
            message = f"Game with ID {game_id} was not found."
            success = False

        return render_template('update.html', message=message, success=success)
    else:
        return render_template('update.html')

@app.route('/import', methods=['GET'])
def import_page():
    return render_template('import.html')


def generate_custom_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def is_unique_id(game_id):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM chess_games WHERE id = %s)", (game_id,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return not exists

def get_unique_id():
    while True:
        game_id = generate_custom_id()
        if is_unique_id(game_id):
            return game_id


@app.route('/submit_game', methods=['POST'])
def submit_game():
    game_id = get_unique_id()
    game_data = {
        "id": game_id,
        'rated': request.form['rated'],
        'created_at': request.form['created_at'],
        'last_move_at': request.form.get('last_move', None),
        'turns': int(request.form.get('turns', 0)),
        'victory_status': request.form.get('victory_status', None),
        'winner': request.form['winner'],
        'increment_code': request.form.get('increment_code', None),
        'white_id': request.form['white'],
        'white_rating': int(request.form['white_rating']),
        'black_id': request.form['black'],
        'black_rating': int(request.form['black_rating']),
        'moves': request.form['moves'],
        'opening_eco': request.form['opening_eco'],
        'opening_name': request.form['opening_name'],
        'opening_ply': request.form.get('opening_ply', None)
    }
    conn = connection()
    cur = conn.cursor()
    query = """
    INSERT INTO chess_games (id, rated, created_at, last_move_at, turns, victory_status, winner, increment_code, white_id, white_rating, black_id, black_rating, moves, opening_eco, opening_name, opening_ply) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        game_data['id'], game_data['rated'], game_data['created_at'], game_data['last_move_at'],
        game_data['turns'], game_data['victory_status'], game_data['winner'], game_data['increment_code'],
        game_data['white_id'], game_data['white_rating'], game_data['black_id'], game_data['black_rating'],
        game_data['moves'], game_data['opening_eco'], game_data['opening_name'], game_data['opening_ply']
    ))

    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('import_page'))
@app.route('/about')
def about():
    return '<h1>About Page</h1>'

if __name__ == "__main__":
    app.run(debug=True)