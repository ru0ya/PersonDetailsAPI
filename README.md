# PersonDetails API
-------------------
- This is a simple REST API built using Flask framework for managing  
persons details. It is based off of CRUD methods that is (Create, Read,  
Update, Delete) performed on a persons details.  

---------------------------
## Table of Contents
- [Prerequisites](https://github.com/ru0ya/PersonDetailsAPI/tree/main#prerequisites)  
- [Installation](https://github.com/ru0ya/PersonDetailsAPI/tree/main#installation)  
- [Routes](https://github.com/ru0ya/PersonDetailsAPI/tree/main#routes)  
- [Documentation](https://github.com/ru0ya/PersonDetailsAPI#documentation)  
- Deployment  
- UML-DIAGRAM

------------------  
## Prerequisites  
Ensure that you have the following readily installed in your system:  
- The latest version of Python  
- An IDE such as Vscode or Pycharm   

-----------------------------------
## Installation  
Follow the following steps to set up and run:  
1. Clone the repository to your local machine:  
```
git clone https://github.com/ru0ya/PersonDetailsAPI.git
```  


2. Navigate to project directory:  
```
cd PersonDetailsAPI
```  

3. Run the following command to set up virtual environment:  
```
python -m venv env
```  
```
source env/bin/activate
```  

4. Run the following command to install dependencies:  
```
pip install -r requirements.txt
```  

------------------
## Routes  
- First we need to connect to a postgresdB and create tables to enable queries:  

```import psycopg2


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
```

> **CREATE(POST)**  
```
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
```

> **READ(GET)**
```
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
```

> **UPDATE(PUT)**
```
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
```

> **DELETE(DELETE)**
```
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
```

- To start the server run the following command:  
`gunicorn main:app'  

Flask server should now run at http://127.0.0.1:8000

----------------------------------  
## Documentation
- These are tests done with Postman to verify API's functionality  
```
undefined/workspace/personapitests/collection/29746601-66697261-e703-4f34-9119-aec29e22a9eb?action=share&creator=29746601
```
