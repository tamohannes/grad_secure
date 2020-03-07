from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "App number 1, on localhost:9000"
    
if __name__ == "__main__":
    app.run(debug=True)