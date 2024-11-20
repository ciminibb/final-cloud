from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Define the database connection details
server = 'finalproject-group39-sql-server.database.windows.net'
database = 'finalproject-group39-sql-db'
username = 'finalprojectadmin'
password = 'group39SECRET'
driver = '{ODBC Driver 17 for SQL Server}'

# Function to test database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# -------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')  # Render the form

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    return redirect(url_for('menu', username=username, email=email))

@app.route('/menu')
def menu():
    username = request.args.get('username')
    email = request.args.get('email')

    return render_template('menu.html', username=username, email=email)

@app.route('/status')
def db_connection_status():
    conn = get_db_connection()
    if conn:
        return "Connection successful!"
    else:
        return "Failed to connect to the database."

@app.route('/sample')
def show_households():
    conn = get_db_connection()  # Establish connection to the database
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Households")  # Query to fetch all households
        households = cursor.fetchall()  # Fetch all results
        conn.close()  # Close the connection

        # Render the results in a template
        return render_template('sample.html', households=households)
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

