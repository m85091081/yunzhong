import datetime
import bson
import conf.setting as setting
from pymongo import MongoClient
import pymongo
client = MongoClient(setting.mongohost)
db = client['Yunzhong']

class Product:
    def __init__(self):
        self.prod = db['Product']
    
    def count(self,val):
        return self.prod.find({'url': str(val)}).count()
    
    def verfiyclass(self):
        return self.prod.find({'$and':[{ 'verfiy': True},{'activity': False}]})
   
    def stayclass(self):
        return self.prod.find({'$and':[{ 'verfiy': False},{'activity': False}]})

    def verfiyacti(self):
        return self.prod.find({'$and':[{'verfiy': True},{'activity': True}]})
   
    def stayacti(self):
        return self.prod.find({'$and':[{'verfiy': False},{'activity': True}]})

    def getdata(self,url):
        return self.prod.find_one({"url": url})
    
    def init(self,verfiy,url,activity,title,pic,timedict,place,link,classify,holderlist,about,prodata,orderdict):
        self.prod.create_index("url", unique=True)
        raw = {
                "verfiy":bool(verfiy), ##布林
                "activity": bool(activity), ##他媽是不是活動
                "url":str(url), 
                "title":str(title),
                "pic":str(pic),
                "timedict":timedict,
                "place":place,
                "link":str(link),
                "classify":classify,
                "holderlist":holderlist,
                "about":str(about),
                "prodata":prodata, ##相關資料
                "orderdict":orderdict
                }
        self.prod.insert_one(raw)
        return True


class User:
    def __init__(self):
        self.user = db['Users']

    def login(self,email,password):
        usern = self.user.find_one({"email": email})
        passwordhash = usern['password'] 
        if password == passwordhash :
            return True
        else:
            return False
    
    def find(self):
        return self.user.find()

    def count(self,val):
        if val is "all" :
            return self.user.count()
        elif val is "student":
            return self.user.find({'school':{'$ne':None}}).count()
        elif val is "company":
            return self.user.find({'companyid':{'$ne':None}}).count()
        elif val is "general":
            return self.user.find({'companyname':{'$ne':None}}).count()
        else:
            return self.user.find({'fbid': val}).count()

    def usercheck(self,email):
        return self.user.find_one({"email": email})

    def fbusercheck(self,fbid):
        return self.user.find_one({"fbid": fbid})
        
    def add(self,email, password, name ,birthday , country , phone , postnum , address , education , grade , school ,major,lineid, fbid):
        self.user.create_index("email", unique=True)
        self.user.create_index("fbid", unique=True, partialFilterExpression={"fbid" : { "$type": "string"}})
        verfiyofemail = True
        raw = {"email": email,
                "verfiyofemail":verfiyofemail,
                "password": password,
                "name": name,
                "birthday": datetime.datetime.combine(birthday, datetime.datetime.min.time()),
                "country" : country,
                "phone" : phone,
                "postnum" : postnum,
                "address" : address,
                "education": education,
                "grade": grade,
                "school":school,
                "major" : major,
                "lineid":lineid,
                "fbid":fbid,
                "date": datetime.datetime.utcnow()}
        self.user.insert_one(raw)
        return True
    
    def addgen(self,email, password, name , birthday, country, phone, postnum, address, industry, companyname, jobtitle, lineid, fbid):
        self.user.create_index("email", unique=True)
        verfiyofemail = True
        self.user.create_index("fbid", unique=True, partialFilterExpression={"fbid" : { "$type": "string"}})
        raw = {"email": email,
                "verfiyofemail":verfiyofemail,
                "password": password,
                "name": name,
                "birthday": datetime.datetime.combine(birthday, datetime.datetime.min.time()),
                "country" : country,
                "phone" : phone,
                "postnum" : postnum,
                "address" : address,
                "industry": industry,
                "companyname": companyname,
                "jobtitle": jobtitle,
                "lineid":lineid,
                "fbid":fbid,
                "date": datetime.datetime.utcnow()}
        self.user.insert_one(raw)
        return True
    

class Pictures:
    def savepicture(content,mime,sha1):
        picture = db['pictures']
        picture.create_index("sha1",unique=True)
        raw = {
                "content": content,
                "mime":mime,
                "time":datetime.datetime.utcnow(),
                "sha1":sha1,
                }
        try:
            print(picture.insert_one(raw).inserted_id)
        except:
            pass
        return sha1

    def getpicture(sha1):
        picture = db['pictures']
        return picture.find_one({'sha1':sha1})


class Visit:
    def count():
        Visit = db['Visit']
        return [Visit.find_one({"day":"all"}),Visit.find().sort("$natural",-1).limit(2)]

    def incount():
        Visit = db['Visit']
        Visit.update({"day":"all"},{"$inc":{"count":1}},upsert=True)
        Visit.update({"day":str(datetime.datetime.today().date())},{"$inc":{"count":1}},upsert=True)
        return True

class info:
    def about(content):
        aboutUs = db['info']
        aboutUs.update({"main":"about"},{"$set":{"content": content}},upsert=True)
        return True

    def general(content):
        benefits = db['info']
        benefits.update({"main":"general"},{"$set":{"content": content}},upsert=True)
        return True

    def company(content):
        benefits = db['info']
        benefits.update({"main":"company"},{"$set":{"content": content}},upsert=True)
        return True

    def student(content):
        benefits = db['info']
        benefits.update({"main":"student"},{"$set":{"content": content}},upsert=True)
        return True

    def getabout():
        aboutUs = db['info']
        return aboutUs.find_one({"main":"about"})

    def getgen():
        benefits = db['info']
        return benefits.find_one({"main":"general"})

    def getcon():
        benefits = db['info']
        return benefits.find_one({"main":"company"})

    def getstu():
        benefits = db['info']
        return benefits.find_one({"main":"student"})
