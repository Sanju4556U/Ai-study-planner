from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# DATABASE
def init_db():

    conn = sqlite3.connect('company.db')

    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            role TEXT,
            salary TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return render_template('index.html')

# ADD EMPLOYEE
@app.route('/add_employee', methods=['POST'])
def add_employee():

    data = request.json

    name = data['name']
    email = data['email']
    role = data['role']
    salary = data['salary']

    conn = sqlite3.connect('company.db')

    c = conn.cursor()

    c.execute('''
        INSERT INTO employees
        (name, email, role, salary)
        VALUES (?, ?, ?, ?)
    ''', (name, email, role, salary))

    conn.commit()
    conn.close()

    return jsonify({"message":"Employee Added"})

# GET EMPLOYEES
@app.route('/get_employees')
def get_employees():

    conn = sqlite3.connect('company.db')

    c = conn.cursor()

    c.execute("SELECT * FROM employees")

    employees = c.fetchall()

    conn.close()

    return jsonify(employees)

# DELETE EMPLOYEE
@app.route('/delete_employee/<int:id>',
methods=['DELETE'])

def delete_employee(id):

    conn = sqlite3.connect('company.db')

    c = conn.cursor()

    c.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Deleted"})

if __name__ == '__main__':
    app.run(debug=True)