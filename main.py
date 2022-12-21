from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from random import choice
from forms import Search, Add, Update

# App
app = Flask(__name__)
app.config["SECRET_KEY"] = "7YH9jnHj8UH8h98II8GYr64eN8yH55N8B6vr7YUNb66yUJKnb64e76OBV4CVBBVT57"

Bootstrap(app)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

# App Routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/all_cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes= all_cafes)

@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = choice(all_cafes)
    return render_template('cafes.html', cafes=[random_cafe])

@app.route("/search", methods=["GET", "POST"])
def search():
    form = Search()
    if form.validate_on_submit():
        location = form.location.data.title()
        searched_cafes =  db.session.query(Cafe).filter(Cafe.location == location)
        return render_template('search.html', form=form, cafes=searched_cafes )
    return render_template('search.html', form=form)

@app.route('/add', methods=['GET', 'POST'])
def add_new_cafe():
    form = Add()
    if request.method == "POST":
        if form.cancel.data:
            return redirect(url_for('home'))
    if form.validate_on_submit():
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = bool(1 if form.has_sockets.data == '✅' else 0)
        has_toilet = bool(1 if form.has_toilet.data == '✅' else 0)
        has_wifi = bool(1 if form.has_wifi.data == '✅' else 0)
        can_take_calls = bool(1 if form.can_take_calls.data == '✅' else 0)
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/update', methods=["GET","PATCH","POST"])
def update_cafe():
    cafe_id = request.args.get('id')
    selected_cafe = Cafe.query.get(cafe_id)
    form = Update(
        img_url= selected_cafe.img_url,
        seats = selected_cafe.seats,
        coffee_price = selected_cafe.coffee_price
    )
    if request.method == "POST":
        if form.cancel.data:
            return redirect(url_for('cafes'))
    if form.validate_on_submit():
        selected_cafe.img_url = form.img_url.data
        selected_cafe.has_socket = bool(1 if form.has_sockets.data == '✅' else 0)
        selected_cafe.has_toilet = bool(1 if form.has_toilet.data == '✅' else 0)
        selected_cafe.has_wifi = bool(1 if form.has_wifi.data == '✅' else 0)
        selected_cafe.can_take_calls = bool(1 if form.can_take_calls.data == '✅' else 0)
        selected_cafe.seats = form.seats.data
        selected_cafe.coffee_price = form.coffee_price.data
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('update.html', form=form, cafe=selected_cafe)


@app.route('/delete', methods=["GET", "DELETE"])
def delete_cafe():
    cafe_id = request.args.get('id')
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


if __name__ == "__main__":
    app.run(debug=True)