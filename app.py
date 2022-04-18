from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_word():
    return "Hello World"


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("movies.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

 
@app.route("/movies", methods=['GET','POST'])
def movies():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM movie")
        movies = [
            dict(id = row[0], title = row[1], language = row[2])
            for row in cursor.fetchall()
        ]
        if movies is not None:
            return jsonify(movies)
        
        
    if request.method == 'POST':
        new_title = request.form["title"]
        new_language = request.form["language"]
        sql = """INSERT INTO movie (title, language)
                 VALUES (?,?)"""
        cursor = cursor.execute(sql, (new_title, new_language))
        conn.commit()
        return f"Der Film mit der id: {cursor.lastrowid} wurde erfolgreich erstellt", 201
        

if __name__ == "__main__":
    app.run()