import os
from PIL import Image
from operator import methodcaller
from flask import render_template, url_for,flash,redirect,request
from flaskpage import app, db, bcrypt
from flaskpage.forms import RegistationForm, LoginForm, UpdateAccountForm
from flaskpage.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskpage.xrp import get_xrp_price
import secrets

@app.route("/")
@app.route("/home")
def home():
    xrp_price = get_xrp_price()
    return render_template('home.html', xrp_price=xrp_price)

@app.route("/about")
def about():

     return render_template('about.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are now able to login!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login Successful','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful, Please Check Email and Password",'danger')


    return render_template('login.html', title='Login', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash(f'Update Successful','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        flash("Update unsuccessful, try again later...",'danger')

    return render_template('account.html', title='Account', image_file = image_file, form=form)

