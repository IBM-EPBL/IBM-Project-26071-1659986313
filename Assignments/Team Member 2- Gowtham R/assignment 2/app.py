from flask import Flask, render_template
from flask_cors import CORS





# APP setup

def create_app():
    web_app = Flask(__name__)  # Initialize Flask App
    CORS(web_app)
    web_app.config['SECRET_KEY'] = "afd8a5b29f4c497dbe58216f046ac4b8"
    return web_app


app = create_app()
@app.route('/')
def home():
   return render_template('/home.html')
@app.route('/aboutme')
def about():
   return render_template('/about.html')

@app.route('/signup')
def signup():
   return render_template('/signup.html')

@app.route('/signin')
def signin():
   return render_template('/signin.html')





if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
