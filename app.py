import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "p-a-s-s-w-o-r-d"

# ===================== DATABASE CONFIG =====================
database_url = os.getenv("MYSQL_URL")

if database_url and database_url.startswith("mysql://"):
    database_url = database_url.replace(
        "mysql://", "mysql+pymysql://", 1
    )

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===================== UPLOAD CONFIG =====================
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===================== MODEL =====================
class Fruit(db.Model):
    __tablename__ = "fruits"

    Fruit_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Color = db.Column(db.String(30))
    Taste = db.Column(db.String(30))
    Country_Origin = db.Column(db.String(50))
    Price_Per_Kg = db.Column(db.Numeric(5, 2))
    Image = db.Column(db.String(100))

# ===================== CREATE TABLES =====================
with app.app_context():
    db.create_all()

# ===================== HELPERS =====================
def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ===================== ROUTES =====================

# Show form
@app.route("/")
def index():
    return render_template("register.html")

# Handle form submission
@app.route("/register", methods=["POST"])
def register():
    image_file = request.files.get("image")
    filename = None

    if image_file and image_file.filename and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_file.save(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )

    new_fruit = Fruit(
        Name=request.form.get("name"),
        Color=request.form.get("color"),
        Taste=request.form.get("taste"),
        Country_Origin=request.form.get("country"),
        Price_Per_Kg=request.form.get("price"),
        Image=filename
    )

    db.session.add(new_fruit)
    db.session.commit()

    return redirect(url_for("view_fruits"))

# View fruits (like /users)
@app.route("/entries")
def view_fruits():
    fruits = Fruit.query.all()

    total_fruits = len(fruits)

    return render_template(
        "entries.html",
        fruits=fruits,
        total_fruits=total_fruits
    )

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
