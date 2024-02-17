from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import secrets

import analysis.weaver_analysis


# Flask requires this line
app = Flask(__name__)
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
foo = secrets.token_urlsafe(16)
app.secret_key = foo
csrf = CSRFProtect(app)


class WordForm4(FlaskForm):
    w1 = StringField("Word 1: ", validators=[DataRequired(), Length(4, 4)])
    w2 = StringField("Word 2: ", validators=[DataRequired(), Length(4, 4)])
    submit = SubmitField("Find Optimal Paths")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/jail")
def jail():
    return render_template("jail.html")


@app.route("/solve4", methods=["GET", "POST"])
def solve4():
    w1 = None
    w2 = None

    form = WordForm4()
    if form.validate_on_submit():
        w1 = form.w1.data
        w2 = form.w2.data
        # return redirect( url_for('actor', id=id) )rm()

    solution = ""
    if w1 is not None and w2 is not None:
        print(w1, w2)
        solution = analysis.weaver_analysis.gui_paths_4(w1.lower(), w2.lower())
        # print(solution)

    return render_template("solve4.html", form=form, solution=solution)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
