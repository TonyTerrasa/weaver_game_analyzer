from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, StopValidation

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
    w1 = StringField("Word 1", validators=[DataRequired(), Length(min=4, max=5, message="words must be length 4 or 5")])
    w2 = StringField("Word 2", validators=[DataRequired(), Length(min=4, max=5, message="words must be length 4 or 5")])
    submit = SubmitField("Find Optimal Paths")

    def validate(self, extra_validators=None):
        if len(self.w1.data) != len(self.w2.data):
            msg = "words must be the same length"
            self.w1.errors += (msg, )
            return False
        
        return True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/jail")
def jail():
    return render_template("jail.html")


@app.route("/solve", methods=["GET", "POST"])
def solve():
    word1, word2 = None, None
    word_length = 4
    solutions = []
    num_solutions = 0
    len_path = 0
    errors_present = False
    gui_summary = ""
    

    print("Hello I'm in the solve")

    form = WordForm4()
    if form.validate_on_submit():
        word1 = form.w1.data
        word2 = form.w2.data

    if word1 is not None and word2 is not None:
        solutions, errors = analysis.weaver_analysis.correctness_paths(word1, word2)
        num_solutions = len(solutions)

        if len(errors):
            form.w1.errors += errors
        else:
            word_length = len(word1)
            len_path = len(solutions[0]) - 1

            if word_length == 4:
                gui_summary = analysis.weaver_analysis.gui_paths_4(word1, word2)
            else:
                gui_summary = analysis.weaver_analysis.gui_paths_5(word1, word2)

            # 3 is where the first path starts (before that there is intro)
            # the last one of gui_summary 
            gui_summary = gui_summary[3:-1]

        # print(num_solutions)
        # print(solutions)

    errors_present = len(form.w1.errors) > 0

    return render_template("solve.html", 
        form=form, 
        solutions=solutions,
        num_solutions=num_solutions, 
        len_path=len_path,
        gui_summary=gui_summary,
        w1=word1,
        w2=word2,
        word_length=word_length,
        errors_present=errors_present,
        )


if __name__ == "__main__":
    # solve("stay", "stow")
    app.run(host='0.0.0.0', debug=True)

