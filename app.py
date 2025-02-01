from flask import Flask, request, render_template, jsonify
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__, template_folder='.')

DB_PATH = 'database.db'

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.form.get("query").lower()

    if "employees in the" in user_input:
        department = user_input.split("in the ")[1].split()[0]
        query = "SELECT * FROM Employees WHERE Department = ?"
        result = execute_query(query, (department.capitalize(),))
    elif "manager of the" in user_input:
        department = user_input.split("of the ")[1].split()[0]
        query = "SELECT Manager FROM Departments WHERE Name = ?"
        result = execute_query(query, (department.capitalize(),))
    elif "hired after" in user_input:
        date = user_input.split("after ")[1]
        query = "SELECT * FROM Employees WHERE Hire_Date > ?"
        result = execute_query(query, (date,))
    elif "total salary expense for" in user_input:
        department = user_input.split("for ")[1].split()[0]
        query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
        result = execute_query(query, (department.capitalize(),))
    else:
        result = [("Invalid query or unsupported operation.",)]

    return render_template('index.html', result=result)

@app.route('/visualize')
def visualize():
    query = "SELECT Department, SUM(Salary) FROM Employees GROUP BY Department"
    data = execute_query(query)

    departments, salaries = zip(*data) if data else ([], [])
    plt.bar(departments, salaries, color='skyblue')
    plt.title('Salary Expenses per Department')
    plt.xlabel('Department')
    plt.ylabel('Total Salary')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plot_url = base64.b64encode(image_png).decode('utf8')

    return render_template('index.html', plot_url=plot_url)

if __name__ == "__main__":
    print("Running Flask app.")
    app.run(debug=True)








