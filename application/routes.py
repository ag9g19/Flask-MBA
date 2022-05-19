import os
from flask import abort, current_app as app
from flask import redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from werkzeug.utils import secure_filename


class MyForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Submit")


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")


"""
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('/dashapp2/'))
"""

"""
@app.route("/about")
def about():
    return render_template("about.html")


# route to html page - "table"
@app.route("/table")
def table():

    # converting csv to html
    data = pd.read_csv("Bakery.csv")
    data = process_bakery(data)
    data_20 = data.head(20)

    df = px.data.medals_wide()
    fig1 = px.bar(
        df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input"
    )
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "table.html", tables=[data_20.to_html()], titles=[""], graph1JSON=graph1JSON
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# @app.route("/admin")
# def admin():
#   return redirect(url_for("user", name="Admin"))


def process_bakery(data):
    data.drop(["Daypart", "DayType"], axis=1, inplace=True)
    data.dropna()
    data.rename(
        {"TransactionNo": "id", "Items": "item", "DateTime": "date"},
        axis=1,
        inplace=True,
    )

    return data
"""
