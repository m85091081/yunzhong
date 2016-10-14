# -*- coding: utf-8 -*-
import flask_login
from flask_login import LoginManager , login_required
from core import app
from flask import render_template , session, redirect, url_for, request, Blueprint , flash
import hashlib
from core_module.dbmongo import User as dbUser
from core_module.form import registerForm , loginForm

class User():
    def __init__(self, username):
        self.username = username
    def email(self):
        myname = dbUser.usercheck(self.username)['email']
        return str(myname)
    def name(self):
        myname = dbUser.usercheck(self.username)['name']
        return str(myname)
    def info(self):
        myname = dbUser.usercheck(self.username)
        return myname
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username

lm = LoginManager()
lm.init_app(app)
register = Blueprint('register', __name__, template_folder='../core_template/templates')
auth = Blueprint('auth', __name__ , template_folder='../core_template/templates')
auth = Blueprint('auth', __name__ , template_folder='../core_template/templates')
users = Blueprint('users', __name__ , template_folder='../core_template/templates')
lm.login_view = "main.index"

@users.route('/info',methods=['GET','POST'])
@login_required
def info():
    loginform = loginForm()
    form = registerForm()
    return render_template('member-info.html',**locals())
@lm.user_loader
def user_loader(email):
    if dbUser.usercheck(email) == False:
        return None
    return User(email)

@auth.route('/', methods=['GET', 'POST'])
def login():
    loginform = loginForm()
    if request.method == 'POST' and loginform.validate_on_submit() :
        user = dbUser.usercheck(loginform.email.data)
        if user and dbUser.login(loginform.email.data,loginform.password.data):
            user_obj = User(user['email'])
            flask_login.login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for('main.index'))
        return '帳號或是密碼錯誤'


@register.route('/student',methods=['GET','POST'])
def reg_stu():
    form = registerForm()
    loginform = loginForm()
    if request.method== 'POST' and not form.validate_on_submit():
        for field_name, field_errors in form.errors.items():
            print(field_errors)
            print(field_name)
        return render_template('reg_err.html',**locals())
    
    elif form.validate_on_submit():
        dbUser.add(form.email.data,form.password.data,form.name.data,form.birthday.data,form.country.data,form.phone.data,form.postnum.data,form.address.data,form.education.data,form.grade.data,form.school.data,form.major.data,form.lineid.data,form.fbid.data)
        return render_template('reg_info.html',**locals())
    return render_template('member-student.html',**locals())

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('main.index'))

