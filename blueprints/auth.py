from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired
from urllib.parse import urlparse

from setup_utils.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    print("🟢 /login route hit")
    print("Form submitted?", form.is_submitted())
    
    if form.validate_on_submit():
        print("Form validated successfully")
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("User found:", user.username)
        else:
            print("User not found")
        
        if user and user.check_password(form.password.data):
            print("✅ Password correct, logging in")
            login_user(user)
            flash("Logged in", "success")

            next_page = request.args.get("next")
            print("Next page:", next_page)
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("index.home")
            
            print("Redirecting to:", next_page)
            return redirect(next_page)
        
        print("❌ Invalid username or password")
        flash("Invalid username or password", "danger")
    else:
        if request.method == "POST":
            print("❌ Form validation failed")
            print(form.errors)
    
    return render_template("login.html", form=form)


# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             print("✅ User logged in")
#             flash("Logged in", "success")
            
#             next_page = request.args.get("next")
#             if not next_page or urlparse(next_page).netloc != "":
#                 next_page = url_for("index.home")
            
#             return redirect(next_page)
        
#         print("❌ Invalid username or password")
#         flash("Invalid username or password", "danger")
#     return render_template("login.html", form=form)
    

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("index.home"))