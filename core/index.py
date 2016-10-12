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
    return render_template('index.html',**locals())
