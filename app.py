from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os

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
    
def get_ordered_query(option):
    match option:
        case "H.Hshd_num":
            file_path = os.path.join("queries", "Household_Query_Order_HshdNum.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query
        
        case "T.Basket_num":
            file_path = os.path.join("queries", "Household_Query_Order_BasketNum.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query

        case "T.Purchase_date":
            file_path = os.path.join("queries", "Household_Query_Order_PurchaseDate.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query

        case "T.Product_num":
            file_path = os.path.join("queries", "Household_Query_Order_ProductNum.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query

        case "P.Department":
            file_path = os.path.join("queries", "Household_Query_Order_Department.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query

        case "P.Commodity":
            file_path = os.path.join("queries", "Household_Query_Order_Commodity.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query

        case None:
            file_path = os.path.join("queries", "Data Pull for Household 10.sql")
            with open(file_path, 'r') as file:
                query = file.read()
            return query


# Search the data base for a specific household data and order by the option
def get_household_by_num(house_num, option):
    conn = get_db_connection() # Establish connection to the database
    if conn:
        cursor = conn.cursor()
        query =  get_ordered_query(option)
        cursor.execute(query, house_num)  # Execute the query
        data = cursor.fetchall()  # Fetch all results
        conn.close()  # Close the connection
        return data

# -------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')  # Render the form

# -------------------------------------------------------------------------------------------------

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    return redirect(url_for('menu', username=username, email=email))

# -------------------------------------------------------------------------------------------------

@app.route('/menu')
def menu():
    username = request.args.get('username')
    email = request.args.get('email')

    return render_template('menu.html', username=username, email=email)

# -------------------------------------------------------------------------------------------------

@app.route('/status')
def db_connection_status():
    conn = get_db_connection()
    if conn:
        return "Connection successful!"
    else:
        return "Failed to connect to the database."
    
# -------------------------------------------------------------------------------------------------

@app.route('/sample')
def pull_household_10():
    username = request.args.get('username')
    email = request.args.get('email')

    conn = get_db_connection()  # Establish connection to the database
    if conn:
        cursor = conn.cursor()
        query = get_ordered_query(None)
        cursor.execute(query)  # Execute the query
        households = cursor.fetchall()  # Fetch all results
        conn.close()  # Close the connection

        # Render the results in a template
        return render_template('sample.html', households=households, username=username, email=email)
    else:
        return "Failed to connect to the database."
    
# -------------------------------------------------------------------------------------------------

@app.route('/search', methods=['GET','POST'])
def search_household():
    username = request.args.get('username')
    email = request.args.get('email')

    # Get the search number if it is available
    search_number = ""
    if (request.args.get('search_number') is not None):
        search_number = request.form['search_number']

    # Get the selected sorting options if its available
    selected_option = ""
    if (request.args.get('selected_option') is not None):
        selected_option = request.form['options']

    # Now contact the database and search for the household and order by the selected option
    results = None
    if (search_number is not "" and selected_option is not ""):
        results = get_household_by_num(search_number, selected_option)

    # Render the results in a template
    return render_template('search.html', username=username, email=email, search_number=search_number, selected_option=selected_option, results=results)

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

