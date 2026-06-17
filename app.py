from flask import Flask, jsonify, request
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
          roll_number INTEGER NOT NULL,
           email TEXT NOT NULL
           );
    """)
    connection.commit()
    cur.close()
    connection.close()

create_student_table()

@app.route("/send_data",methods = ["POST"])
def send_data():
    student_name = request.json['student_name']
    roll_number = request.json['roll_number']
    email = request.json['email']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
        INSERT INTO student_table (student_name, roll_number, email)
        VALUES (%s, %s, %s);
    """, (student_name, roll_number, email))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message": "Data inserted successfully!"}), 201


@app.route("/get_data", methods=["GET"])
def get_data():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("""
                select * from student_table;
    """)
    Data = cur.fetchone()
    cur.close()
    connection.close()
    return jsonify({
              "student_id":Data[0],
              "student_name":Data[1],
              "roll_number":Data[2],
                "email":Data[3],

    }),200

@app.route("/put_data",methods=["PUT"])
def put_data():
    student_id = request.json['student_id']
    student_name = request.json['student_name']
    roll_number = request.json['roll_number']
    email = request.json['email']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("UPDATE student_table SET student_name = %s, roll_number = %s, email = %s WHERE student_id = %s",(student_name, roll_number, email, student_id))
    
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message": "Data updated successfully!"}), 200

@app.route("/delete_data",methods=["DELETE"])
def delete_data():
    student_id = request.json['student_id']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM student_table WHERE student_id = %s",(student_id,))
    connection.commit()
    cur.close()
    connection.close()
    return jsonify({"message": "Data deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
