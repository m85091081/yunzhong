from flask import render_template,request,Blueprint
from core import app
from core_module import dbmongo
from flask_paginate import Pagination
admbp = Blueprint('admbp', __name__ , template_folder='../core_template/templates')

@admbp.route('/')
def admindex():
    return render_template('admin/index.html')

@admbp.route('/user')
def admuser():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allmem = dbmongo.User.find()
    page = request.args.get('page', type=int, default=1)
    pagemem = dbmongo.User.find().limit(30).skip((int(page)-1)*30)
    pagin = Pagination(page=page,per_page=30,bs_version=3,total=allmem.count(),search=search,record_name='allmem')
    return render_template('admin/user.html',**locals())
