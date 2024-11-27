from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyodbc
import os
import ntpath
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the database connection details
server = 'finalproject-group39-sql-server.database.windows.net'
database = 'finalproject-group39-sql-db'
username = 'finalprojectadmin'
password = 'group39SECRET'
driver = '{ODBC Driver 17 for SQL Server}'

# -----------------------------------------------  
# Function to test database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# -----------------------------------------------  
# Function to test storage account connection
def get_sa_connection():
    try:
        # Define the account name and basic credential for the storage account
        account_url = "https://finalprojectgroup39sa.blob.core.windows.net/"
        credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=credential)

        # Create the container client for our storage account
        return blob_service_client.get_container_client(container="8451-data")
    except:
        return None
    
# -----------------------------------------------  
def get_query(sqlfile):
    try:
        file_path = os.path.join("queries", sqlfile)
        with open(file_path, 'r') as file:
            query = file.read()
        return query
    except:
        return None

# -----------------------------------------------  
def get_ordered_query(option):
    match option:
        case "H.Hshd_num":
            return get_query("Household_Query_Order_HshdNum.sql")
        
        case "T.Basket_num":
            return get_query("Household_Query_Order_BasketNum.sql")

        case "T.Purchase_date":
            return get_query("Household_Query_Order_PurchaseDate.sql")

        case "T.Product_num":
            return get_query("Household_Query_Order_ProductNum.sql")

        case "P.Department":
            return get_query("Household_Query_Order_Department.sql")

        case "P.Commodity":
            return get_query("Household_Query_Order_Commodity.sql")

        case _:
            return get_query("Data Pull for Household 10.sql")


# -----------------------------------------------
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

# -----------------------------------------------
# Setup the blob storage connection so we can send a file to our storage account.
# Uploading files will replace the existing files of the same name in the blob
# storage account, this way the data pipeline will pick up the new data.
def upload_household_blob_file(filepath):
    try:
        if (ntpath.basename(filepath) != "400_households.csv"):
            raise Exception("File name was not the expected file name!")
        container_client = get_sa_connection()
        with open(file=filepath, mode="rb") as data:
            container_client.upload_blob(name="400_households.csv", data=data, overwrite=True)
        return "The file was successfully uploaded to the server!"
    except Exception as e:
        return f"The file failed being uploaded to the server: {e}"

# -----------------------------------------------
def upload_product_blob_file(filepath):
    try:
        if (ntpath.basename(filepath) != "400_products.csv"):
            raise Exception("File name was not the expected file name!")
        container_client = get_sa_connection()
        with open(file=filepath, mode="rb") as data:
            container_client.upload_blob(name="400_products.csv", data=data, overwrite=True)
        return "The file was successfully uploaded to the server!"
    except Exception as e:
        return f"The file failed being uploaded to the server: {e}"

# -----------------------------------------------
def upload_transaction_blob_file(filepath):
    try:
        if (ntpath.basename(filepath) != "400_transactions.csv"):
            raise Exception("File name was not the expected file name!")
        container_client = get_sa_connection()
        with open(file=filepath, mode="rb") as data:
            container_client.upload_blob(name="400_transactions.csv", data=data, overwrite=True)
        return "The file was successfully uploaded to the server!"
    except Exception as e:
        return f"The file failed being uploaded to the server: {e}"

# -----------------------------------------------  
def process_blob_file(filepath, datatype):
    if datatype == 'household':
        return upload_household_blob_file(filepath)
    elif datatype == 'product':
        return upload_product_blob_file(filepath)
    elif datatype == 'transaction':
        return upload_transaction_blob_file(filepath)

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
    if (search_number != "" and selected_option != ""):
        results = get_household_by_num(search_number, selected_option)

    # Render the results in a template
    return render_template('search.html', username=username, email=email, search_number=search_number, selected_option=selected_option, results=results)

# -------------------------------------------------------------------------------------------------

@app.route("/upload", methods=['GET'])
def upload():
    username = request.args.get('username')
    email = request.args.get('email')

    return render_template('upload.html', username=username, email=email)

# -------------------------------------------------------------------------------------------------

@app.route("/upload-file", methods=['POST'])
def upload_file():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        data_type = request.form.get('dataType')
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Create directory for specific data type if it doesn't exist
        data_type_folder = os.path.join(UPLOAD_FOLDER, data_type)
        if not os.path.exists(data_type_folder):
            os.makedirs(data_type_folder)

        # Save the file
        filepath = os.path.join(data_type_folder, file.filename)
        file.save(filepath)

        # Process the file based on data type
        status = process_blob_file(filepath, data_type)

        return jsonify({
            'message': status,
            'filename': file.filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -------------------------------------------------------------------------------------------------

@app.route("/dashboard", methods=['GET'])
def dashboard():
    username = request.args.get('username')
    email = request.args.get('email')

    return render_template('dashboard.html', username=username, email=email)

# -------------------------------------------------------------------------------------------------
# Chart 1 - Bar chart where x-axis is the age ranges and y-axis is the total spend per basket
# Chart 2 - Bar chart where the x-axis is whether they are a homeowner and the y-axis is the number of units per basket
# Chart 3 - Bar chart where the x-axis is the store-region and the y-axis is number of homeowners in that region
# Chart 4 - Pie chart where each section of the pie are the different income ranges and size of the slice is determined by number of people in that income range
# Chart 5 - Bar chart where the x-axis is the income range and the y-axis is the average spend per basket
# Chart 6 - Bar chart where the x-axis is the number of children and the y-axis is both the average spend per basket and the average number of units per basket

@app.route("/dashboard-agespendgraph", methods=['GET'])
def dashboard_agespendgraph():
    conn = get_db_connection()
    rawData = []
    if conn:
        cursor = conn.cursor()
        query =  get_query("chart1.sql")
        cursor.execute(query)
        rawData = cursor.fetchall()
        conn.close()

    labels = [row[0] for row in rawData if row[0] != "Age_range"]
    data = [row[1] for row in rawData if row[1] != "total_spend"]
    
    return jsonify({
        'type': 'bar',
        'data': {
            'labels': labels,
            'datasets': [{
                'label': 'Total Spend',
                'data': data,
                'backgroundColor': 'blue',
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

@app.route("/dashboard-homeownerunitschart", methods=['GET'])
def dashboard_homeownerunitschart():
    conn = get_db_connection()
    rawData = []
    if conn:
        cursor = conn.cursor()
        query =  get_query("chart2.sql")
        cursor.execute(query)
        rawData = cursor.fetchall()
        conn.close()

    labels = [row[0] for row in rawData if row[0] != "Homeowner"]
    data = [row[1] for row in rawData if row[1] != "total_units"]

    return jsonify({
        'type': 'line',
        'data': {
            'labels': labels,
            'datasets': [{
                'label': 'Total Units',
                'data': data,
                'backgroundColor': 'blue',
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

@app.route("/dashboard-regionhomeownerchart", methods=['GET'])
def dashboard_regionhomeownerchart():
    conn = get_db_connection()
    rawData = []
    if conn:
        cursor = conn.cursor()
        query =  get_query("chart3.sql")
        cursor.execute(query)
        rawData = cursor.fetchall()
        conn.close()

    labels = [row[0] for row in rawData if row[0] != "Store_r"]
    data = [row[1] for row in rawData if row[1] != "num_homeowners"]

    return jsonify({
        'type': 'bar',
        'data': {
            'labels': labels,
            'datasets': [{
                'label': 'Num Homeowners',
                'data': data,
                'backgroundColor': 'blue',
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

@app.route("/dashboard-incomechart", methods=['GET'])
def dashboard_incomechart():
    return jsonify({
        'type': 'line',
        'data': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'datasets': [{
                'label': 'Monthly Sales',
                'data': [12000, 15000, 18000, 16500, 20000, 22000],
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

@app.route("/dashboard-incomespendchart", methods=['GET'])
def dashboard_incomespendchart():
    return jsonify({
        'type': 'line',
        'data': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'datasets': [{
                'label': 'Monthly Sales',
                'data': [12000, 15000, 18000, 16500, 20000, 22000],
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

@app.route("/dashboard-childrenspendunitschart", methods=['GET'])
def dashboard_childrenspendunitschart():
    return jsonify({
        'type': 'line',
        'data': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'datasets': [{
                'label': 'Monthly Sales',
                'data': [12000, 15000, 18000, 16500, 20000, 22000],
                'borderColor': 'blue',
                'fill': False
            }]
        }
    })

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

