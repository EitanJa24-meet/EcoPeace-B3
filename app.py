# importing libraries
from flask import Flask, render_template, request, redirect, url_for
from flask import session
import pyrebase
import os
import google.generativeai as genai
import markdown

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# firebase auth and db
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

# global variable for the chatbot response
finetune = ""

# signup route
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['name']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except Exception as e:
            print("error", e)
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
            print("error", e)
            return redirect(url_for('error'))
    else:
        return render_template('login.html')

# home route
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# /chatbot route
@app.route("/chatbot", methods=['GET', 'POST'])
def bot():
    global finetune
    if request.method == 'POST':
        user_input = request.form['message']
        # Start a new chat session or continue the existing one
        chat_session = model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    "Welcome! I'm the EcoPeace chatbot, here to help you explore our initiatives in environmental peacebuilding across Israel, Palestine, and Jordan. Whether you're interested in our cross-border water conservation projects, renewable energy collaborations, or educational programs for youth about the environment, I can provide you with detailed information. Visit our website: https://ecopeaceme.org. What would you like to learn more about today?"
                ]
            }
        ])
        # Get the response from the chatbot
        response = chat_session.send_message(user_input).text
        
        finetune = markdown.markdown(response)

    return render_template("chatbot.html", response=finetune)

@app.route("/join", methods=['GET', 'POST'])
def join():
    return render_template('join.html')

# library route
@app.route('/library', methods=['GET', 'POST'])
def library():
    return render_template("library.html")

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
	return render_template('teacher.html')

@app.route('/student', methods=['GET', 'POST'])
def student():
	return render_template('student.html')


# error route
@app.route("/error")
def error():
    return render_template('error.html')

# running the code
if __name__ == '__main__':
    app.run(debug=True)
