from flask import render_template,request,Blueprint
from core import app
from core_module import dbmongo
from core_module.form import aboutform
from flask_paginate import Pagination
admbp = Blueprint('admbp', __name__ , template_folder='../core_template/templates')
allmem = dbmongo.User()

@admbp.route('/')
def admindex():
    allmemcount = allmem.count("all")
    allstdcount = allmem.count("student")
    allgencount = allmem.count("general")
    allcocount  = allmem.count("company")
    allprod = dbmongo.Product()
    allvfyclass = allprod.verfiyclass().count()
    allvfyacti  = allprod.verfiyacti().count()
    allstayclass= allprod.stayclass().count()
    allstayacti = allprod.stayacti().count()
    visit = dbmongo.Visit.count()
    allvisit = visit[0]["count"]
    todayvisit = visit[1][0]["count"]
    yesterdayvisit = visit[1][1]["count"]
    percent = round(todayvisit/yesterdayvisit*100,1)
    return render_template('admin/index.html',**locals())

@admbp.route('/user')
def admuser():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allmemcount = allmem.find().count()
    page = request.args.get('page', type=int, default=1)
    pagemem = allmem.find().limit(30).skip((int(page)-1)*30)
    pagin = Pagination(page=page,per_page=30,bs_version=3,total=allmemcount,search=search,record_name='allmem')
    return render_template('admin/user.html',**locals())

@admbp.route('/about', methods=['POST','GET'])
def admabout():
    form = aboutform()
    content = dbmongo.info.getabout()['content']
    if request.method == 'GET':
        return render_template('admin/about.html',**locals())

    elif request.method == 'POST' and form.validate_on_submit():
        content = form.content.data
        dbmongo.info.about(content)
        return render_template('admin/about.html',**locals())
