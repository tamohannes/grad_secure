from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "App number 1, on localhost:9000"


@app.route("/path1")
def path1():
    return "App number 1, on localhost:9000, path1"
    

@app.route("/path2")
def path2():
    return "App number 1, on localhost:9000, path2"
    

@app.route("/path3/path3prime")
def path3():
    return "App number 1, on localhost:9000, path3/path3prime"
        

if __name__ == "__main__":
    app.run(debug=True)