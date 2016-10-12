import datetime
import conf.setting as setting 
from pymongo import MongoClient
client = MongoClient(setting.mongohost)
db = client['Yunzhong']
class InitDB:
    user = db['Users']

class User:
    def login(email,password):
        user = db['Users']
        usern = user.find_one({"email": email})
        passwordhash = usern['password'] 
        if password == passwordhash :
            return True
        else:
            return False

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


