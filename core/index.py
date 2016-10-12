# -*- coding: utf-8 -*-
# muMDAU_app main / first page 
from core import app, socketio
from threading import Thread
from flask import request, render_template, Blueprint, url_for, redirect, session
from core_module.dbmongo import User
from core_module.form import loginForm
main = Blueprint('main', __name__ , template_folder='../core_template/templates')
# index page main route page 


@main.route('/', methods=['GET', 'POST'])
def index():
    loginform = loginForm()
    allmem = User.count('all')
    company = User.count('company')
    return render_template('index.html',**locals())

@main.route('/about', methods=['GET', 'POST'])
def about():
    loginform = loginForm()
    return render_template('about.html',**locals())

@app.errorhandler(404)
def page_not_found(e):
    loginform = loginForm()
    return render_template('404.html',**locals()), 404
