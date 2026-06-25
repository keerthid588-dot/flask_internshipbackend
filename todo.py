from flask import Flask, request,jsonify
import psycopg2
from flask_bcrypt import Bcrypt

app =Flask(__name__)

bcrypt = Bcrypt(app)

#database config
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Mallikasulu"

def get_db_connection():
    return psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user =DB_USER,
        password =DB_PASSWORD
    )

#CREATE STUDENT_TABLE
def create_student_table():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
             CREATE TABLE IF NOT EXISTS users_table(
                 user_id SERIAL PRIMARY KEY,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 email TEXT NOT  NULL UNIQUE
                );
""")
    connection.commit()
    cur.close()
    connection.close()

create_student_table()

@app.route('/signup', methods = ['POST'])
def signup():

    username =request.json["username"]
    email =request.json["email"]
    password =request.json["password"]
    
    hashed_passsword = bcrypt.generate_password_hash(password).decode("utf-8")
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
         INSERT INTO users_table(username,email,password) VALUES(%s,%s,%s)
""",(username,email,hashed_passsword))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message":"signup successful"})


@app.route('/login', methods = ['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]
    if not email or not password:
        return jsonify({"error":"All fields are required"}),400
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
        SELECT * FROM users_table WHERE email = %s
    """,(email,))

    user = cur.fetchone()
    cur.close()
    connection.close()
    if not user:
       return jsonify({"error":"Invalid email or password"}),401
    return jsonify({
        "message":"Login successful",
        "user":{
            "user_id":user[0],
            "username":user[1],
            "email":user[3]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)