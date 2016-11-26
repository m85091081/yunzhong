from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField, RadioField , IntegerField , SelectField,FieldList
from wtforms.fields.html5 import DateField
from wtforms.validators import Length  , EqualTo  
from wtforms.validators import DataRequired as Required
import wtforms
class submitclassinfo(FlaskForm):
    cover = StringField('',validators=[Required()])
    name = StringField('',validators=[Required()],render_kw={"placeholder": "請輸入課程名稱"})
    daterange = StringField('',validators=[Required()],render_kw={"placeholder": "請輸入日期"})
    address = StringField('',validators=[Required()],render_kw={"placeholder": "請輸入活動地址"})
    link = StringField('',validators=[Required()],render_kw={"placeholder": "請輸入相關鏈接"})
    organize = StringField('',validators=[Required()],render_kw={"placeholder": "請輸入主辦單位"})
    content = StringField('', widget=wtforms.widgets.TextArea())

    
class registerForm(FlaskForm):
    email = StringField('註冊 Email：',validators=[Required()])
    password = PasswordField('密碼：', validators=[Required(),EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('確認密碼：')
    name = StringField('姓名：',validators=[Required()])
    birthday  = DateField('生日：', format='%Y-%m-%d',validators=[Required()],render_kw={"placeholder": "格式: 2016-01-20"})
    country = RadioField('',choices=[('taiwan','本國'),('china','陸生'),('japan','日本'),('korea','韓國')],validators=[Required()])
    phone = IntegerField('',validators=[Required()])
    postnum = IntegerField('',validators=[Required()],render_kw={"placeholder": "郵遞區號"})
    address = StringField('',validators=[Required()],render_kw={"placeholder": "地址欄"})
    education = SelectField('' , choices=[('junior', '國中'), ('high', '高中'), ('university', '大學'),('yinjoso', '研究所'),('other', '其他')],validators=[Required()])
    grade = StringField('',validators=[Required()],render_kw={"placeholder": "年級"})
    school = StringField('',validators=[Required()],render_kw={"placeholder": "畢業 / 就讀學校"})
    major = StringField('',[Required()],render_kw={"placeholder": "畢業 / 就讀科系"})
    lineid = StringField('')
    fbid = StringField('')
    accept_tos = BooleanField('我已詳閱', validators=[Required()])

class registerFormgen(FlaskForm):
    email = StringField('註冊 Email：',validators=[Required()])
    password = PasswordField('密碼：', validators=[Required(),EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('確認密碼：')
    name = StringField('姓名：',validators=[Required()])
    birthday  = DateField('生日：', format='%Y-%m-%d',validators=[Required()],render_kw={"placeholder": "格式: 2016/01/20"})
    country = RadioField('',choices=[('taiwan','本國'),('china','陸生'),('japan','日本'),('korea','韓國')],validators=[Required()])
    phone = IntegerField('',validators=[Required()])
    postnum = IntegerField('',validators=[Required()],render_kw={"placeholder": "郵遞區號"})
    address = StringField('',validators=[Required()],render_kw={"placeholder": "地址欄"})
    lineid = StringField('')
    fbid = StringField('')
    industry = SelectField('', choices=[('construction','營建工程業'),('Wholesale','批發及零售業'),('transport','運輸及倉儲業'),('manufacturing','製造業'),('mining','礦業及土石採取業')])
    companyname = StringField('',validators=[Required()])
    jobtitle = StringField('',validators=[Required()])
    accept_tos = BooleanField('我已詳閱', validators=[Required()])

class loginForm(FlaskForm):
    email = StringField('Email：',validators=[Required()],render_kw={"placeholder": "Email"})
    password = PasswordField('密碼：', validators=[Required()],render_kw={"placeholder": "密碼"})

class productForm(FlaskForm):
    email = StringField('Email：',validators=[Required()],render_kw={"placeholder": "Email"})
    name = StringField('Name：',validators=[Required()],render_kw={"placeholder": "姓名"})
    phone = StringField('Email：',validators=[Required()],render_kw={"placeholder": "電話"})


