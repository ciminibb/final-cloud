import pyodbc

# Replace with your actual connection details
server = 'finalproject-group39-sql-server.database.windows.net'
database = 'finalproject-group39-sql-db'
username = 'finalprojectadmin'
password = 'group39SECRET'
driver= '{ODBC Driver 17 for SQL Server}'

try:
    # Establishing the connection
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    print("Connection successful!")

    # Create a cursor from the connection
    cursor = conn.cursor()

    # Example SQL query
    cursor.execute("SELECT TOP 5 * FROM Households")

    # Fetch results
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")

