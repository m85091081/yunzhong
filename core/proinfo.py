from flask import request, render_template, Blueprint, url_for, redirect, session
proinfo = Blueprint('proinfo', __name__ , template_folder='../core_template/templates')
from core_module.dbmongo import User,Product
from core_module.form import loginForm

@proinfo.route('/show/<url>', methods=['GET', 'POST'])
def showinfo(url):
    loginform = loginForm()
    data = Product.getdata(url)
    if Product.count(str(url)) == 0 :
        return render_template('404.html',**locals())
    return render_template('proinfo-show.html',**locals())

