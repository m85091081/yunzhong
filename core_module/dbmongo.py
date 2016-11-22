import datetime
import conf.setting as setting
from pymongo import MongoClient
import pymongo
client = MongoClient(setting.mongohost)
db = client['Yunzhong']
class InitDB:
    user = db['Users']
class Product:
    def count(val):
        prod = db['Product']
        return prod.find({'url': str(val)}).count()
    def countall():
        prod = db['Product']
        return prod.find()
    def getdata(url):
        prod = db['Product']
        produ = prod.find_one({"url": url})
        return produ
    
    def init(url,activity,title,pic,timedict,place,link,classify,holderlist,about,prodata,payment,orderdict):
        prod = db['Product']
        prod.create_index("url", unique=True)
        raw = { "activity": bool(activity),
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
                "payment":payment, ##布林
                "orderdict":orderdict
                }
        print(prod.insert_one(raw).inserted_id)
        return True


class User:
    def login(email,password):
        user = db['Users']
        usern = user.find_one({"email": email})
        passwordhash = usern['password'] 
        if password == passwordhash :
            return True
        else:
            return False
    def find():
        user = db['Users']
        return user.find()
    def count(val):
        if val is "all" :
            user = db['Users']
            return user.count()
        elif val is "company":
            user = db['Users']
            return user.find({'companyid': {'$ne': None}}).count()
        else:
            user = db['Users']
            return user.find({'fbid': val}).count()
            

    def usercheck(email):
        user = db['Users']
        usern = user.find_one({"email": email})
        return usern

    def fbusercheck(fbid):
        user = db['Users']
        usern = user.find_one({"fbid": fbid})
        return usern
        
    def add(email, password, name ,birthday , country , phone , postnum , address , education , grade , school ,major,lineid, fbid):
        user = db['Users']
        user.create_index("email", unique=True)
        user.create_index("fbid", unique=True)
        raw = {"email": email,
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
        print(user.insert_one(raw).inserted_id)
        return True
    
    def addgen(email, password, name , birthday, country, phone, postnum, address, industry, companyname, jobtitle, lineid, fbid):
        user = db['Users']
        user.create_index("email", unique=True)
        user.create_index("fbid", unique=True)
        raw = {"email": email,
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
        print(user.insert_one(raw).inserted_id)
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


