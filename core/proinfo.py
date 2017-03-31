from flask import make_response, Response, request, render_template, Blueprint, url_for, redirect, session,jsonify
from flask_login import current_user , login_required
from core_module.dbmongo import Product as product,Pictures
from core_module.form import loginForm , productForm, submitclassinfo
from core_module.pictures import uploadpicture,uploadcover
from flask_paginate import Pagination
from core import app
from xpinyin import Pinyin
import ast , datetime, base64, re

p = Pinyin()
proinfo = Blueprint('proinfo', __name__ , template_folder='../core_template/templates')
tickets = Blueprint('tickets', __name__ , template_folder='../core_template/templates')
act = Blueprint('act', __name__ , template_folder='../core_template/templates')
classrom = Blueprint('classrom',__name__ , template_folder='../core_template/templates')

Product = product()
### classrom 課程區域
@tickets.route('/member/<url>', methods=['GET'])
def tickemem(url):
    loginform = loginForm()
    if current_user.email() == Product.geturlcreator(url) :
        title  = Product.geturlname(url)
        ticitem = Product.getticmem(url)
        return render_template('tmem.html',**locals())

@tickets.route('/dashboard', methods=['GET'])
def tickerdash():
    loginform = loginForm()
    buyertic = Product.getbuyer(current_user.email())
    creatortic_raw = Product.getcreator(current_user.email())
    creatortic = []
    for x in creatortic_raw:
        title = x.get('title')
        url = x.get('url')
        temp_ticket_count = 0
        for xx in x.get('orderdict'):
            temp_ticket_count = int(xx.get('much')) + int(temp_ticket_count)
        crawdict = {"url":url,"title":title,"much":temp_ticket_count}
        creatortic.append(crawdict)
    return render_template('tdash.html',**locals())


@classrom.route('/', methods=['GET', 'POST'])
def porinfo():
    loginform = loginForm()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = Product.verfiyclass()
    page = request.args.get('page', type=int, default=1)
    pagepd = Product.verfiyclass().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('proinfo-class.html',**locals())

@classrom.route('/show/<url>', methods=['GET', 'POST'])
def showinfo(url):
    loginform = loginForm()
    data = Product.getdata(url)
    if Product.count(str(url)) == 0 or data.get('activity') == True or data.get('verfiy') == False:
        return render_template('404.html',**locals())
    return render_template('proinfo-show.html',**locals())

@classrom.route('/verify', methods=['GET', 'POST'])
def showverinfo():
    loginform = loginForm()
    return render_template('wait.html',**locals())

@classrom.route('/submit',methods=['GET','POST'])
def submitpro():
    loginform = loginForm()
    form = submitclassinfo()
    if request.method == 'GET':
        return render_template('lesson.html' , **locals())
    elif request.method == 'POST' and form.validate_on_submit() and len(list(filter(None,request.form.getlist('ticket[]')))) >= 3 :
        address = form.address.data
        link = form.link.data
        flavor = form.organize.data
        organize = current_user.name()
        daterange = form.daterange.data
        labout = form.labout.data
        cover = url_for('serve_picture',sha1=uploadcover(base64.b64decode(form.cover.data[23:])))
        name = form.name.data
        name_pinyin = p.get_pinyin(str(name)).replace('-','').replace(' ','')[0:14]
        url =  str(datetime.datetime.now().strftime('%y%m%d%H%M'))+'-'+name_pinyin
        content = form.content.data
        ticket = request.form.getlist('ticket[]')
        count = 0
        dticket = []
        for x,y,z in zip(ticket[0::3], ticket[1::3],ticket[2::3]):
            dtickettemp = {"id": count,"name":x,"cost":y,"much":z}
            count = count + 1
            dticket.append(dtickettemp)
        Product.init(False,current_user.email(),url,False,name,labout,cover,daterange,address,link,flavor,organize,content,"noproddata",dticket)
        return redirect(url_for('classrom.showverinfo'))
    
    else:
        """偷懶debug區"""
        """不要送任何可以測資讓認證可過即可直接測試"""
        return render_template('reg_err.html',**locals())


### 活動模組


@act.route('/', methods=['GET', 'POST'])
def actporinfo():
    loginform = loginForm()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = Product.verfiyacti()
    page = request.args.get('page', type=int, default=1)
    pagepd = Product.verfiyacti().sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('proinfo-acti.html',**locals())

@act.route('/show/<url>', methods=['GET', 'POST'])
def actshowinfo(url):
    loginform = loginForm()
    data = Product.getdata(url)
    if Product.count(str(url)) == 0 or data.get('activity') == False or data.get('verfiy') == False:
        return render_template('404.html',**locals())
    return render_template('proinfo-show.html',**locals())

@act.route('/verify', methods=['GET', 'POST'])
def shotactverifyinfo():
    loginform = loginForm()
    return render_template('wait.html',**locals())

@act.route('/submit',methods=['GET','POST'])
def submitprinfoo():
    loginform = loginForm()
    form = submitclassinfo()
    if request.method == 'GET':
        return render_template('activity.html' , **locals())
    elif request.method == 'POST' and form.validate_on_submit() and len(list(filter(None,request.form.getlist('ticket[]')))) >= 3 :
        address = form.address.data
        link = form.link.data
        flavor = form.organize.data
        organize = current_user.name()
        daterange = form.daterange.data
        cover = url_for('serve_picture',sha1=uploadcover(base64.b64decode(form.cover.data[23:])))
        name = form.name.data
        name_pinyin = p.get_pinyin(str(name)).replace('-','').replace(' ','')[0:14]
        url =  str(datetime.datetime.now().strftime('%y%m%d%H%M'))+'-'+name_pinyin
        content = form.content.data
        labout = form.labout.data
        ticket = request.form.getlist('ticket[]')
        count = 0
        dticket = []
        for x,y,z in zip(ticket[0::3], ticket[1::3],ticket[2::3]):
            dtickettemp = {"id": count,"name":x,"cost":y,"much":z}
            count = count + 1
            dticket.append(dtickettemp)
        Product.init(False,current_user.email(),url,True,name,labout,cover,daterange,address,link,flavor,organize,content,"noproddata",dticket)
        return redirect(url_for('act.shotactverifyinfo',url=url))
    else:
        """偷懶debug區"""
        """不要送任何可以測資讓認證可過即可直接測試"""
        return render_template('reg_err.html',**locals())


### 搜尋模組

@app.route('/search/', methods=['GET'])
def porinfosearch():
    loginform = loginForm()
#    category = request.args.get('category')
    title = request.args.get('title')
    if title==None:
        pass
    else:
        title = title.rsplit(' ')
        for index, item in enumerate(title):
            title[index] = re.compile(''+item+'')
 #   if 'search' not in dir(Product):
  #      return render_template('404.html',**locals()),404
    search = False
    q = request.args.get('q')
    if q:
        search = True
    allpd = Product.searchmozz(title)
    page = request.args.get('page', type=int, default=1)
    pagepd = allpd.sort('$natural',-1).limit(9).skip((int(page)-1)*9)
    pagin = Pagination(page=page,per_page=9,bs_version=3,total=allpd.count(),search=search,record_name='allpd')
    return render_template('proinfo.html',**locals())


### 購物車模組

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
                url = Product.getdata(str(x).rsplit('-',1)[0]).get('url')
                tid = Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('id')
                much = int(buydict.get(x))
                price = int(price)
                tempinfo = [title,price,much]
                buyinfo.append(tempinfo)
                allmoney = allmoney + (price*much)
                if Product.ticupdate(url,tid,much)== 'NoTic':
                    return render_template('err_tic.html',**locals())

                Product.ticadd(tid,url,title,current_user.name(),current_user.info().get('phone'),current_user.email(),much,int(price*much))
            loginform = loginForm()
            pform = productForm()
        response = make_response(render_template('proinfo-shop03.html',**locals()))
        response.set_cookie('num','',expires=0)
        response.set_cookie('buydict','',expires=0)
        return response

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
                much = int(buydict.get(x))
                price = int(price)
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
            much = int(buydict.get(x))
            price = int(price)
            tempinfo = [title,price,much]
            buyinfo.append(tempinfo)
            allmoney = allmoney + (price*much)
    loginform = loginForm()
    return render_template('proinfo-shop01.html',**locals())


@proinfo.route('/clear', methods=['GET', 'POST'])
def delclr():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('num','',expires=0)
    response.set_cookie('buydict','',expires=0)
    return response



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
            price = int(Product.getdata(str(x).rsplit('-',1)[0]).get('orderdict')[int(str(x).rsplit('-',1)[1])].get('cost'))
            much = int(buydict.get(x))
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
    refer = request.headers.get('Referer')
    response = make_response(redirect(refer))

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
        else:
            return render_template('err_tic.html',**locals())

    response.set_cookie('num',num)
    print(buydict)
    response.set_cookie('buydict',str(buydict))
    return response

### editor 用模組

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

