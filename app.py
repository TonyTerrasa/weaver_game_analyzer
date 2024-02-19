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


# @app.route("/solve4", methods=["GET", "POST"])
# def solve4():
#     w1 = None
#     w2 = None

#     form = WordForm4()
#     if form.validate_on_submit():
#         w1 = form.w1.data
#         w2 = form.w2.data
#         # return redirect( url_for('actor', id=id) )rm()

#     solution = ""
#     if w1 is not None and w2 is not None:
#         print(w1, w2)
#         solution = analysis.weaver_analysis.gui_paths_4(w1.lower(), w2.lower())
#         # print(solution)

#     return render_template("solve4.html", form=form, solution=solution)

def generate_solution_html(w1, w2):
    
    paths = analysis.weaver_analysis.correctness_paths_4(w1, w2)
    path_box = ""
    for p_num, p in enumerate(paths):
        option_string = ""
        option_string += f'<div class="path-option" id="option{p_num+1}Content">\n'
        option_string += f'<h2 class="option-name">Option {p_num+1}</h2>\n'
        for step in p:
            option_string += '<div class="wordle-grid">\n'
            for letter, correctness in step:
                if correctness == "C":
                    option_string += f'<div class="box correct-box">{letter}</div>\n'
                else:
                    option_string += f'<div class="box normal-box">{letter}</div>\n'
            option_string += '</div>\n'
        option_string += '</div>\n'
        path_box += option_string


    selector = ""
    for p_num in range(len(paths)):
        selector += f'<option value="option{p_num+1}">Option {p_num+1}</option>\n'
    selector += f'<option value="all" selected>All</option>\n'

    return selector, path_box


@app.route("/solve4", methods=["GET", "POST"])
def solve4():
    w1 = None
    w2 = None
    selector = ""
    path_box = ""

    form = WordForm4()
    if form.validate_on_submit():
        w1 = form.w1.data
        w2 = form.w2.data
        # return redirect( url_for('actor', id=id) )rm()

    solution = ""
    if w1 is not None and w2 is not None:
        print(w1, w2)
        selector, path_box = generate_solution_html(w1, w2)
        print(selector)
        print(path_box)

    return render_template("solve4.html", 
        form=form, 
        selector=selector, 
        path_box=path_box,
        w1=w1,
        w2=w2)


if __name__ == "__main__":
    # solve("stay", "stow")
    app.run(host='0.0.0.0', debug=True)

