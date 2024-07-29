# WATAN
# importing libraries
from flask import Flask, render_template, request, redirect, url_for
from flask import session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyD0eu0W1DQkI_zwWfLs7DK3kcN9An7D_b4",
  "authDomain": "ecopeace-1.firebaseapp.com",
  "projectId": "ecopeace-1",
  "storageBucket": "ecopeace-1.appspot.com",
  "messagingSenderId": "301297032466",
  "appId": "1:301297032466:web:32b7bf3897e0a51bca67cb",
  "databaseURL": "https://ecopeace-1-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# defining
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

# signup route
@app.route('/', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		username= request.form['name']
		try:
			user = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except Exception as e:
			print("error",e)  
			return redirect(url_for('error'))

	else:
		return render_template('signup.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			session['localId'] = user['localId']
			return redirect(url_for('home'))
		except Exception as e:
			print("error",e) 
			return redirect(url_for('error'))
	else:
		return render_template('login.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
	return render_template("home.html")


@app.route("/error")
def error():
	return render_template('error.html')

# running the code
if __name__ == '__main__':
	app.run(debug=True)