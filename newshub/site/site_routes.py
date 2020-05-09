from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from newshub import pos_db, bcrypt
from newshub.site.models import User
from newshub.site.forms import LoginForm, RegisterForm, UpdateAccountForm
import requests

site_bp = Blueprint('site_bp',__name__)

@site_bp.route('/')
@site_bp.route('/index')
@site_bp.route('/home')
def index():
    # if request.headers.getlist("X-Forwarded-For"):
    #     ip = request.headers.getlist("X-Forwarded-For")[0]
    # else:
    #     ip = request.remote_addr
    # url = 'https://ipinfo.io/'+str(ip)+'/json?token=b579f4931aac3b'
    # loc = requests.get(url)
    page = request.args.get('page',type=int,default=1)
    print(request.remote_addr)
    news_data = requests.get('http://localhost:5000/api/latest_news?page='+str(page))
    return render_template('home.html',news_data=news_data.json())

@site_bp.route('/about')
# @login_required
def about():
    # data = User.query.first()
    return "current_user.username"

@site_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect("login")
    form = LoginForm()
    if form.validate_on_submit():
        # Get user in db by email
        user = User.query.filter_by(email=form.email.data).first()
        # Check users hashed password matches typed password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Check for any next parameter arguments
            next_page = request.args.get("next")
            # Ternary to send user to next page if it exists, otherwise send user to home page
            return redirect(next_page) if next_page else redirect(url_for("site_bp.about"))
        else:
            flash("Login unsuccessful. Check email or password", "danger")

    return render_template("login.html", title="Login", form=form)

@site_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("site_bp.index"))

@site_bp.route('/register',methods=['GET','POST'])
def register():
    print("1")
    if current_user.is_authenticated:
        return redirect("login")
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash password
        print("2")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        # Construct new user
        user = User(
            username=form.name.data,
            email=form.email.data,
            password=hashed_password,
            # dob=form.dob.data,
            address=form.address.data,
        )
        # Save user to db
        db.session.add(user)
        db.session.commit()
        print("3")
        flash("Your account has been created. Please log in", "success")
        return redirect(url_for("site_bp.login"))
    print("4")
    return render_template("register.html", title="Register", form=form)

@site_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    # Check if form data is valid, update user account info in database, redirect to account page
    if form.validate_on_submit():
        # Check for picture data
        # if form.picture.data:
        #     picture_file = save_picture(form.picture.data)
        #     current_user.image_file = picture_file
        current_user.username = form.name.data
        current_user.email = form.email.data
        # current_user.profile_type = form.profile_type.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("site_bp.account"))
    elif request.method == "GET":
        form.name.data = current_user.username
        form.email.data = current_user.email
        # form.profile_type.data = current_user.profile_type
    # Set profile picture image file
    # image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", form=form
    )
