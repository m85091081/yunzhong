import datetime
import conf.setting as setting 
from pymongo import MongoClient
client = MongoClient(setting.mongohost)
db = client['Yunzhong']
class InitDB:
    user = db['Users']
class Product:
    def count(val):
        prod = db['Product']
        return prod.find({'url': str(val)}).count()

    def getdata(url):
        prod = db['Product']
        produ = prod.find_one({"url": url})
        return produ
    
    def init(url,title,pic,timedict,place,link,classify,holderlist,about,prodata,payment,orderdict):
        prod = db['Product']
        prod.create_index("url", unique=True)
        raw = { "url":str(url),
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
    def count(val):
        if val is "all" :
            user = db['Users']
            return user.count()
        elif val is "company":
            user = db['Users']
            return user.find({'companyid': {'$ne': None}}).count()


            
    def usercheck(email):
        user = db['Users']
        usern = user.find_one({"email": email})
        return usern

    def add(email, password, name ,birthday , country , phone , postnum , address , education , grade , school ,major,lineid, fbid):
        user = db['Users']
        user.create_index("email", unique=True)
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


