import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "p-a-s-s-w-o-r-d"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/nature_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

class Fruit(db.Model):
    __tablename__ = 'fruit'

    Fruit_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Color = db.Column(db.String(30))
    Taste = db.Column(db.String(30))
    Country_Origin = db.Column(db.String(50))
    Price_Per_Kg = db.Column(db.Numeric(5,2))
    Image = db.Column(db.String(100))

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        taste = request.form["taste"]
        country = request.form["country"]
        price = request.form["price"]
        image_file = request.files.get("image")

        filename = None
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)

        new_fruit = Fruit(
            Name=name,
            Color=color,
            Taste=taste,
            Country_Origin=country,
            Price_Per_Kg=price,
            Image=filename
        )
        db.session.add(new_fruit)
        db.session.commit()

        flash("Fruit registered successfully!", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/entries")
def entries():
    fruits = Fruit.query.all()
    return render_template("entries.html", fruits=fruits)

if __name__ == "__main__":
    app.run(debug=True)
