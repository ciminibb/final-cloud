from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://finalprojectadmin:group39SECRET@finalproject-group39-sql-server.database.windows.net:1433/finalproject-group39-sql-db?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)

# DEFINE DB MODELS
# -------------------------------------------------------------------------------------------------

# Define class for Households table
class Household(db.Model):
    Hshd_num = db.Column(db.Integer, primary_key=True)
    Loyalty = db.Column(db.String(100))
    Age_range = db.Column(db.String(100))
    Marital = db.Column(db.String(100))
    Income_range = db.Column(db.String(100))
    Homeowner = db.Column(db.String(100))
    Hshd_composition = db.Column(db.String(100))
    HH_size = db.Column(db.String(100))
    Children = db.Column(db.String(100))

# Define class for Products table
class Product(db.Model):
    Product_num = db.Column(db.Integer, primary_key=True)
    Department = db.Column(db.String(100))
    Commodity = db.Column(db.String(100))
    Brand_ty = db.Column(db.String(100))
    Natural_organic_flag = db.Column(db.String(100))

# Define class for Transactions table
class Transaction(db.Model):
    __tablename__ = 'transaction'  # Explicit table name (optional but recommended)

    # Composite Primary Key: Hshd_num, Product_num, Basket_num
    Hshd_num = db.Column(db.Integer, db.ForeignKey('household.Hshd_num'), primary_key=True)
    Product_num = db.Column(db.Integer, db.ForeignKey('product.Product_num'), primary_key=True)
    Basket_num = db.Column(db.String(100), primary_key=True)

    # Other Columns
    Purchase_date = db.Column(db.Date)
    Spend = db.Column(db.Float)
    Units = db.Column(db.Integer)
    Store_r = db.Column(db.String(100))
    Week_num = db.Column(db.Integer)
    Year = db.Column(db.Integer)

# -------------------------------------------------------------------------------------------------

# This function renders the homepage (sign-in form) at / endpoint.
@app.route('/')
def index():
    return render_template('index.html')  # Render the form

# This function handles the submission of the sign-in form on homepage.
@app.route('/submit', methods=['POST'])
def submit():
    # Get the data from the form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Redirect to /menu and pass the credentials as query parameters
    return redirect(url_for('menu', username=username, email=email))

# This function renders the menu at /menu endpoint, among other things.
@app.route('/menu')
def menu():
    # Retrieve credentials from query parameters
    username = request.args.get('username')
    email = request.args.get('email')

    # Render the menu page with the credentials
    return render_template('menu.html', username=username, email=email)

# This function renders the data for Household #10 and related transactions.
@app.route('/household/<int:hshd_num>')
def show_household_data(hshd_num):
    # Query to fetch data matching the SQL query exactly
    data = db.session.query(
        Household.Hshd_num.label('Hshd_num'),
        Transaction.Basket_num.label('Basket_num'),
        Transaction.Purchase_date.label('Purchase_date'),
        Transaction.Product_num.label('Product_num'),
        Product.Department.label('Department'),
        Product.Commodity.label('Commodity'),
        Product.Brand_ty.label('Brand_ty'),
        Product.Natural_organic_flag.label('Natural_organic_flag'),
        Transaction.Spend.label('Spend'),
        Transaction.Units.label('Units'),
        Transaction.Store_r.label('Store_r'),
        Transaction.Week_num.label('Week_num'),
        Transaction.Year.label('Year'),
        Household.Loyalty.label('Loyalty'),
        Household.Age_range.label('Age_range'),
        Household.Marital.label('Marital'),
        Household.Income_range.label('Income_range'),
        Household.Homeowner.label('Homeowner'),
        Household.Hshd_composition.label('Hshd_composition'),
        Household.HH_size.label('HH_size'),
        Household.Children.label('Children')
    ).join(Transaction, Household.Hshd_num == Transaction.Hshd_num) \
     .join(Product, Transaction.Product_num == Product.Product_num) \
     .filter(Household.Hshd_num == hshd_num) \
     .order_by(
         Household.Hshd_num,
         Transaction.Basket_num,
         Transaction.Purchase_date,
         Transaction.Product_num,
         Product.Department,
         Product.Commodity
     ).all()

    # Render the results in a template
    return render_template('household_data.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

