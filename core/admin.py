from flask import render_template,request,Blueprint,redirect,url_for,current_app
from flask_login import current_user , login_required
from core import app
from core_module import dbmongo
from core_module.form import aboutform,submitclassinfo,loginForm
from core_module.pictures import uploadpicture,uploadcover
from flask_paginate import Pagination
import ast , datetime, base64, re
admbp = Blueprint('admbp', __name__ , template_folder='../core_template/templates')
dbUser = dbmongo.User()
dbprod = dbmongo.Product()
dbadm = dbmongo.Admin()
@admbp.before_request
def bfreq():
    try:
        cmail =  current_user.email()
    except Exception as e:
        return '無管理權限'
        
    if not dbadm.usercheck(cmail) :
        return '無管理權限'


@login_required
@admbp.route('/')
def admindex():
    allmemcount = dbUser.count("all")
    allstdcount = dbUser.count("student")
    allgencount = dbUser.count("general")
    allcocount  = dbUser.count("company")
    allvfyclass = dbprod.verfiyclass().count()
    allvfyacti  = dbprod.verfiyacti().count()
    allstayclass= dbprod.noverfiyclass().count()
    allstayacti = dbprod.noverfiyacti().count()
    visit = dbmongo.Visit.count()
    allvisit = visit[0]["count"]
    todayvisit = visit[1][0]["count"]
    yesterdayvisit = visit[1][1]["count"]
    percent = round(todayvisit/yesterdayvisit*100,1)
    return render_template('admin/index.html',**locals())

@login_required
@admbp.route('/user')
def admuser():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allmemcount = dbUser.find().count()
    page = request.args.get('page', type=int, default=1)
    pagemem = dbUser.find().limit(30).skip((int(page)-1)*30)
    pagin = Pagination(page=page,per_page=30,bs_version=3,total=allmemcount,search=search,record_name='allmem')
    return render_template('admin/user.html',**locals())

@login_required
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

@login_required
@admbp.route('/student', methods=['POST','GET'])
def admstudent():
    form = aboutform()
    content = dbmongo.info.getstu()['content']
    if request.method == 'GET':
        return render_template('admin/admin-member-benefits-student.html',**locals())

    elif request.method == 'POST' and form.validate_on_submit():
        content = form.content.data
        dbmongo.info.student(content)
        return render_template('admin/admin-member-benefits-student.html',**locals())

@login_required
@admbp.route('/general', methods=['POST','GET'])
def admgeneral():
    form = aboutform()
    content = dbmongo.info.getgen()['content']
    if request.method == 'GET':
        return render_template('admin/admin-member-benefits-general.html',**locals())

    elif request.method == 'POST' and form.validate_on_submit():
        content = form.content.data
        dbmongo.info.general(content)
        return render_template('admin/admin-member-benefits-general.html',**locals())

@login_required
@admbp.route('/company', methods=['POST','GET'])
def admcompany():
    form = aboutform()
    content = dbmongo.info.getcon()['content']
    if request.method == 'GET':
        return render_template('admin/admin-member-benefits-company.html',**locals())

    elif request.method == 'POST' and form.validate_on_submit():
        content = form.content.data
        dbmongo.info.company(content)
        return render_template('admin/admin-member-benefits-company.html',**locals())

@login_required
@admbp.route('/class/submit', methods=['POST','GET'])
def admprosubmit():
    if request.method == "POST":
       dbprod.proshelve(request.form.getlist('urls[]'))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = dbprod.verfiyclass()
    page = request.args.get('page', type=int, default=1)
    pagepd = dbprod.verfiyclass().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('admin/admin-product-management.html',**locals())

@login_required
@admbp.route('/preview/<url>', methods=['GET'])
def admpreview(url):
    loginform = loginForm()
    data = dbprod.getdata(url)
    if dbprod.count(str(url)) == 0:
        return render_template('404.html',**locals())
    return render_template('proinfo-show.html',**locals())


@login_required
@admbp.route('/proedit/<url>', methods=['POST','GET'])
def admproedit(url):
    data = dbprod.getdata(url)
    form = submitclassinfo()
    if request.method == 'GET':
        return render_template('admin/proedit.html' , **locals())
    elif request.method == 'POST' and form.validate_on_submit() and len(list(filter(None,request.form.getlist('ticket[]')))) >= 3 :
        address = form.address.data
        link = form.link.data
        organize = form.organize.data
        daterange = form.daterange.data
        cover = form.cover.data
        labout = form.labout.data
        print(cover[0:4])
        if cover[0:4] == '/pic':
            pass
        else:
            cover = url_for('serve_picture',sha1=uploadcover(base64.b64decode(cover[23:])))
        name = form.name.data
        content = form.content.data
        ticket = request.form.getlist('ticket[]')
        count = 0
        dticket = []
        for x,y,z in zip(ticket[0::3], ticket[1::3],ticket[2::3]):
            dtickettemp = {"id": count,"name":x,"cost":y,"much":z}
            dticket.append(dtickettemp)
        dbprod.proupdate(url,name,labout,cover,daterange,address,link,"no-classify",organize,content,"noproddata",dticket)
        return redirect(url_for('classrom.showinfo',url=url))
    
    else:
        """偷懶debug區"""
        """不要送任何可以測資讓認證可過即可直接測試"""
        return render_template('reg_err.html',**locals())

@login_required
@admbp.route('/siteedit', methods=['POST','GET'])
def admsiteedit():
    if request.method == 'GET':
        return render_template('admin/admin-edit.html',**locals())


@login_required
@admbp.route('/acti/submit', methods=['POST','GET'])
def admstusubmit():
    if request.method == "POST":
       dbprod.proshelve(request.form.getlist('urls[]'))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = dbprod.verifyacti()
    page = request.args.get('page', type=int, default=1)
    pagepd = dbprod.verfiyacti().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('admin/admin-product-management-acti.html',**locals())


@login_required
@admbp.route('/acti/unsubmit', methods=['POST','GET'])
def admentsubmit():
    if request.method == "POST":
       dbprod.proconfirm(request.form.getlist('urls[]'))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = dbprod.noverfiyacti()
    page = request.args.get('page', type=int, default=1)
    pagepd = dbprod.noverfiyacti().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('admin/admin-product-unverify-acti.html',**locals())

@login_required
@admbp.route('/class/unsubmit', methods=['POST','GET'])
def admunclasssubmit():
    if request.method == "POST":
       dbprod.proconfirm(request.form.getlist('urls[]'))
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = dbprod.noverfiyclass()
    page = request.args.get('page', type=int, default=1)
    pagepd = dbprod.noverfiyclass().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('admin/admin-product-unverify.html',**locals())
