from core_module.dbmongo import Product,User,info
from datetime import datetime
import random
info.about("test")
info.general("test")
info.student("test")
info.company("test")
string = '<p>這是一個一生中一定要看的展覽!!</p><br><p>NASA，一個既熟悉又陌生的名詞，多年來，國人僅能從電影或是電視上看到這些人類探索太空的故事，現在，真實的NASA即將降落在台灣，將這個具有重大歷史意義的展覽，完整的呈現在您的面前，帶領我們一起進入一場人類的冒險。<br>這次的展覽有以下八大主題區,超過一千坪的展場,是一般售票特展的三倍大：</p><br><p>◎啟程: 登上火箭發射架<br><br>踏上壯觀的火箭發射架: 讓您化身太空人，一步步前往開啟冒險旅程的火箭</p><br><p><img src="/static/images/test01.jpg"></p><br><p>&nbsp;</p><br><p>◎啟程: 登上火箭發射架<br>踏上壯觀的火箭發射架: 讓您化身太空人，一步步前往開啟冒險旅程的火箭</p><br><p><img src="/static/images/test02.jpg"></p>'

string2 = '<p>購物車系統測試文字</p><br>'

#for x in range(0,100850) :
#    email = random.uniform(1, 10)
#    fbid = random.uniform(1,10)
#    User.add(email, 0, 0 , datetime.strptime('24052010', "%d%m%Y").date() , 0 ,0 , 0 , 0 , 0 , 0 , 0 ,0,0, fbid)

Product.init(True,"nasa-in-taiwan",True,"『NASA-一場人類冒險』特展 台灣站 太空科技‧盡在眼前!","/static/images/pro04.jpg",{"start":datetime(2016,5,28,9,0,0),"end":datetime(2016,11,18,18,0,0),"endbuy":datetime(2016,10,30,19,0,0)},"台北市士林區士商路189號 (國立臺灣科學教育館 七樓特展室)","http://space-event.com.tw/zh-tw/home","科技",["傑迪斯整合行銷股份有限公司","0800-XXXX-YYY","陳慶展 企劃經理"],string,['Nodata'],[{"id":"0","name":"『NASA-一場人類冒險』特展 台灣站","info":"google.com","cost":300,"much":20},{"id":"1","name":"『NASA-一場人類冒險』特展 台灣站","info":"google.com","cost":300,"much":0}])

Product.init(True,"shopping-cart-test",False,"購物車測試文字","/static/images/pro01.jpg",{"start":datetime(2016,5,28,9,0,0),"end":datetime(2016,11,18,18,0,0),"endbuy":datetime(2016,10,30,19,0,0)},"台北市士林區士商路189號 (國立臺灣科學教育館 七樓特展室)","http://space-event.com.tw/zh-tw/home","科技",["傑迪斯整合行銷股份有限公司","0800-XXXX-YYY","陳慶展 企劃經理"],string2,['Nodata'],[{"id":"0","name":"測試票卷-一般票","info":"google.com","cost":300,"much":50},{"id":"1","name":"測試票-學生","info":"google.com","cost":300,"much":10}])
