from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

