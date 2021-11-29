from flask import render_template, url_for,flash,redirect
from flaskpage import app
from flaskpage.forms import RegistationForm, LoginForm
from flaskpage.models import User, Post


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
     return render_template('about.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegistationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':

            flash(f'You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful",'danger')
    return render_template('login.html', title='Login', form=form)