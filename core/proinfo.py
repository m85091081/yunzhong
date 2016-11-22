from flask import make_response, Response, request, render_template, Blueprint, url_for, redirect, session,jsonify
proinfo = Blueprint('proinfo', __name__ , template_folder='../core_template/templates')
classrom = Blueprint('classrom',__name__ , template_folder='../core_template/templates')
from core_module.dbmongo import User,Product,Pictures
from core_module.form import loginForm , productForm, submitclassinfo
from core_module.pictures import uploadpicture
from flask_paginate import Pagination
from core import app
import ast

@classrom.route('/', methods=['GET', 'POST'])
def porinfo():
    loginform = loginForm()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = Product.countall()
    page = request.args.get('page', type=int, default=1)
    pagepd = Product.countall().limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('proinfo.html',**locals())

@proinfo.route('/bill', methods=['GET', 'POST'])
def porbill():
    if request.method == 'POST':
        loop1 = [1]
        buydict = request.cookies.get('buydict')
        allmoney = 0
        if buydict is None :
            buyinfo = []
        else:
            buydict = ast.literal_eval(str(buydict))
            buyinfo = []
            for x in buydict:
                title = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('name')
                price = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('cost')
                much = buydict.get(x)
                tempinfo = [title,price,much]
                buyinfo.append(tempinfo)
                allmoney = allmoney + (price*much)
            loginform = loginForm()
            pform = productForm()
        return render_template('proinfo-shop03.html',**locals())

@proinfo.route('/checkit', methods=['GET', 'POST'])
def checkit():
    if request.method == 'POST':
        loop1 = [1]
        buydict = request.cookies.get('buydict')
        allmoney = 0
        if buydict is None :
            buyinfo = []
        else:
            buydict = ast.literal_eval(str(buydict))
            buyinfo = []
            for x in buydict:
                title = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('name')
                price = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('cost')
                much = buydict.get(x)
                tempinfo = [title,price,much]
                buyinfo.append(tempinfo)
                allmoney = allmoney + (price*much)
            loginform = loginForm()
            pform = productForm()
        return render_template('proinfo-shop02.html',**locals())

@proinfo.route('/checked', methods=['GET', 'POST'])
def shop1():
    loop1 = [1]
    buydict = request.cookies.get('buydict')
    allmoney = 0
    if buydict is None :
        buyinfo = []
    else:
        buydict = ast.literal_eval(str(buydict))
        buyinfo = []
        for x in buydict:
            title = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('name')
            price = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('cost')
            much = buydict.get(x)
            tempinfo = [title,price,much]
            buyinfo.append(tempinfo)
            allmoney = allmoney + (price*much)
    loginform = loginForm()
    return render_template('proinfo-shop01.html',**locals())

@classrom.route('/show/<url>', methods=['GET', 'POST'])
def showinfo(url):
    loginform = loginForm()
    data = Product.getdata(url)
    if Product.count(str(url)) == 0 :
        return render_template('404.html',**locals())
    return render_template('proinfo-show.html',**locals())

@proinfo.route('/clear', methods=['GET', 'POST'])
def delclr():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('num','',expires=0)
    response.set_cookie('buydict','',expires=0)
    return response

@classrom.route('/submit',methods=['GET','POST'])
def submitpro():
    loginform = loginForm()
    form = submitclassinfo()
    if request.method == 'GET':
        return render_template('lesson.html' , **locals())

@proinfo.route('/submit',methods=['GET','POST'])
def submitprinfoo():
    loginform = loginForm()
    form = submitclassinfo()
    if request.method == 'GET':
        return render_template('event.html' , **locals())

@proinfo.route('/shop', methods=['GET', 'POST'])
def shop():
    loop1 = [1]
    buydict = request.cookies.get('buydict')
    allmoney = 0
    if buydict is None :
        buyinfo = []
    else:
        buydict = ast.literal_eval(str(buydict))
        buyinfo = []
        for x in buydict:
            title = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('name')
            price = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('cost')
            much = buydict.get(x)
            tempinfo = [title,price,much]
            buyinfo.append(tempinfo)
            allmoney = allmoney + (price*much)
    loginform = loginForm()
    return render_template('proinfo-shop.html',**locals())

@proinfo.route('/addcart',methods=['POST'])
def addcart():
    loginform = loginForm()
    num = request.cookies.get('num')
    buydict = request.cookies.get('buydict')
    for x in request.form:
        response = make_response(redirect(url_for('classrom.showinfo',url=str(x).rsplit('-',1)[0])))

    for x in request.form:
        if int(request.form[x]) <= int(Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('much')):
            if num is None :
                num = 0
            if buydict is None:
                buydict = str({})
            buydict = ast.literal_eval(str(buydict))
            num = str(int(num)+int(request.form[x]))
            if buydict.get(x) == None:
                buydict[x]=0
            buydict[x] = int(buydict.get(x)) + int(request.form[x])
            buydict = dict( (x,y) for x,y in buydict.items() if y!=0)

    response.set_cookie('num',num)
    print(buydict)
    response.set_cookie('buydict',str(buydict))
    return response


@app.route('/picture/f/<sha1>',methods=['GET'])
def serve_picture(sha1):
    try:
        f = Pictures.getpicture(sha1)
        if f is None:
            raise IOError()
        if request.headers.get('If-modified-Since') == f['time'].ctime():
            return Response(status=304)
        resp = Response(f['content'], mimetype='image/' + f['mime'])
        resp.headers['Last-Modified'] = f['time'].ctime()
        return resp
    except IOError:
        loginform = loginForm()
        return render_template('404.html',**locals()), 404
@app.route('/mdupload',methods=['POST'])
def mdupload():
    if request.method == 'POST' and 'files[]' in request.files:
        f = request.files['files[]']
        sha1 = uploadpicture(f)
        url = url_for('serve_picture',sha1=str(sha1))
        return jsonify(files=[{"url":url}])
    else:
        return False

