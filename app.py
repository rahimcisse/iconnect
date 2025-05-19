from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('Job-Browse-Page.html')

@app.route('/login')
def login():
    return render_template('login.html')
 
if __name__ == "__main__":
    app.run(debug=True)

