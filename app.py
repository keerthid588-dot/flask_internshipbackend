from flask import Flask
import psycopg2

app = Flask(__name__)
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Mallikasulu"

def get_db_connection():
    return psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME, 
        user = DB_USER, 
        password = DB_PASS
 )
def create_student_table():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""     
            CREATE TABLE IF NOT EXISTS student_table (
           student_id SERIAL PRIMARY KEY,
           student_name TEXT NOT NULL,
          age INTEGER NOT NULL,
          grade TEXT NOT NULL
           );
    """)
    connection.commit()
    cur.close()
    connection.close()

create_student_table()

if __name__ == "__main__":
    app.run(debug=True)