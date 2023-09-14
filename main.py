#!/usr/bin/python3
"""
Flask RestAPI to fetch persons details
"""
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

conn = psycopg2.connect(database_url)

# create postgress table
CREATE_PERSONS_TABLE = "CREATE TABLE IF NOT EXISTS persons\
        (id SERIAL PRIMARY KEY, name TEXT);"

# connect and execute creation of table
with conn:
    with conn.cursor() as cursor:
        cursor.execute(CREATE_PERSONS_TABLE)

# query to insert new person into table
INSERT_PERSON = "INSERT INTO persons (name) VALUES (%s) RETURNING id;"

@app.route("/api", methods=['POST'])
def create():
    """
    creates and adds new person based on provided details
    """
    data = request.get_json()
    name = data['name']
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(INSERT_PERSON, (name,))
            person_id = cursor.fetchone()[0]
    return jsonify({"id": person_id, "name": name}), 201


@app.route("/api/<int:person_id>", methods=['GET'])
def get(person_id):
    """
    Fetches user based on user id
    """
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM persons WHERE id = %s", (person_id,))
            user = cursor.fetchone()
            if user:
                return jsonify({"id": user[0], "name": user[1]}), 200
            else:
                return jsonify({"error": f"User with ID {person_id} not found"}), 404


@app.route("/api/<int:person_id>", methods=['PUT'])
def update_persons(person_id):
    """
    Updates person based on provided id
    """
    data = request.get_json()
    name = data['name']
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                    "UPDATE persons SET name = %s WHERE id = %s",
                    (name,person_id,)
                    )
        if cursor.rowcount == 0:
            return jsonify({"error": f"User with ID {person_id} not found."}), 404
        return jsonify({
                "id": user_id,
                "name": name, 
                "message": f"User {person_id} updated"
                }), 201


@app.route("/api/<int:person_id>", methods=['DELETE'])
def delete_person(person_id):
    """
    Deletes person based on provided id
    """
    data = request.get_json()
    name = data['name']
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM persons WHERE id = %s", (person_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"{person_id} not found, could not\
                        complete operation"}), 404
    return jsonify({
        "id": user_id,
        "name": name,
        "message": f"User {person_id} deleted"
        }), 201


if __name__ == "__main__":
    app.run(debug=True)
