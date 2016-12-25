from flask import render_template, flash, redirect
from porterw import app, db
from porterw.forms import LoginForm
import pymongo

# _______________________________________

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    collection = 'users'
    col = pymongo.collection.Collection(db, collection, create=False)
    users = [ user['username'] for user in col.find() ]
    user = { 'nickname' : "Bobo", 'usernames' : "%r" % users }
    return render_template('index.html', title='Home', user = user)
# _______________________________________

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for OpenId=%s, remember_me=%s" % ( form.openid.data, str(form.remember_me.data)))
        return redirect("/index")
    return render_template(
            'login.html',
            title='Sign In',
            form=form,
            providers=app.config['OPENID_PROVIDERS']
        )
