# -*- coding: utf-8 -*-
# muMDAU_app main / first page
from core import app
from flask import request, render_template, Blueprint, g
from core_module.dbmongo import User , Visit, info , Product
from core_module.form import loginForm
main = Blueprint('main', __name__ , template_folder='../core_template/templates')

user = User()
product = Product()

@app.context_processor
def allmdbr():
    infopp = info.prophoto()['url']
    loginform = loginForm()
    return dict(infopp = infopp , loginform = loginform)

@main.route('/', methods=['GET', 'POST'])
def index():
    fbreg = request.cookies.get('fbreg') 
    allmem = user.count('all')
    Visit.incount()
    company = user.count('company')
    vcc = product.verfiyclasscount()
    vac = product.verfiyacticount()
    return render_template('index.html',**locals())

@main.route('/about', methods=['GET', 'POST'])
def about():
    content = info.getabout()['content']
    return render_template('about.html',**locals())

@main.route('/member-benefits-general', methods=['GET'])
def benefit_general():
    content = info.getgen()['content']
    return render_template('member-benefits-general.html',**locals())

@main.route('/member-benefits-student', methods=['GET'])
def benefit_student():
    content = info.getstu()['content']
    return render_template('member-benefits-student.html',**locals())

@main.route('/member-benefits-company', methods=['GET'])
def benefit_company():
    content = info.getcon()['content']
    return render_template('member-benefits-company.html',**locals())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',**locals()), 404
