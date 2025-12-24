from flask import Flask, render_template
from routes.upload_routes import upload_bp

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

app.register_blueprint(upload_bp)

if __name__ == "__main__":
    app.run(debug=True)
