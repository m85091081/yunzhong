# -*- coding: utf-8 -*-
import flask_login
from flask_login import LoginManager , login_required
from core import app
from flask import make_response,render_template , session, redirect, url_for, request, Blueprint , flash
import hashlib
import time
from core_module import facebook
from core_module.dbmongo import User as dbuser
from core_module.dbmongo import Admin 
from core_module.form import registerForm , loginForm ,registerFormgen

dbadm = Admin()
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
    def is_admin(self):
        try: 
            cmail = current_user.email()
        except Exception as e:
            return False
        if not dbadm.usercheck(cmail):
            return False
        return True

dbUser = dbuser()
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
            return redirect(request.args.get("next") or url_for('main.index'))
        return render_template('login_err.html',loginform = loginform)
    else:
        return render_template('login_err.html',loginform = loginform)

@register.route('/student',methods=['GET','POST'])
def reg_stu():
    form = registerForm()
    loginform = loginForm()
    fbtoken = request.cookies.get('fbToken')
    if fbtoken:
        fbname = facebook.getData(fbtoken)

    if request.method== 'POST' and not form.validate_on_submit():
        return render_template('reg_err.html',**locals())
    elif form.validate_on_submit():
        if form.fbid.data =="":
            fbuuid = None
        else:
            fbuuid = form.fbid.data
        dbUser.add(form.email.data,form.password.data,form.name.data,form.birthday.data,form.country.data,form.phone.data,form.postnum.data,form.address.data,form.education.data,form.grade.data,form.school.data,form.major.data,form.lineid.data,fbuuid)
        return render_template('reg_info.html',**locals())
    return render_template('member-student.html',**locals())

@register.route('/general',methods=['GET','POST'])
def reg_gen():
    form = registerFormgen()
    loginform = loginForm()
    if request.method== 'POST' and not form.validate_on_submit():
        return render_template('reg_err.html',**locals())
    elif form.validate_on_submit():
        if form.fbid.data =="":
            fbuuid = None
        else:
            fbuuid = form.fbid.data
        dbUser.addgen(form.email.data,form.password.data,form.name.data,form.birthday.data,form.country.data,form.phone.data,form.postnum.data,form.address.data,form.industry.data,form.companyname.data,form.jobtitle.data,form.lineid.data,fbuuid)
        return render_template('reg_info.html',**locals())
    return render_template('member-general.html',**locals())

@app.route('/fb')
def fblogin():
    code = request.args.get('code',False)
    if code:
        Res=facebook.getToken(request.base_url,code)
        if Res[0]:
            fbuid = facebook.getUID(Res[1])
            if dbUser.count(fbuid) is not 0 :
                user = dbUser.fbusercheck(fbuid)
                user_obj = User(user['email'])
                flask_login.login_user(user_obj)
                return redirect(request.args.get("next") or url_for('main.index'))
            else:
                resp = make_response(redirect(url_for('main.index')))
                resp.set_cookie(key='fbreg', value='1', expires=time.time()+2)
                resp.set_cookie(key='fbToken',value=Res[1],max_age=int(Res[2]),secure=False)
                return resp
    else:
        fburl = facebook.genGetCodeURL(request.base_url)
        return redirect(fburl, code=301)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('main.index'))

