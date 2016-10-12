from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,PasswordField, RadioField , IntegerField , SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length  , EqualTo  
from wtforms.validators import DataRequired as Required
class registerForm(FlaskForm):
    email = StringField('註冊 Email：',validators=[Required()])
    password = PasswordField('密碼：', validators=[Required(),EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('確認密碼：')
    name = StringField('姓名：',validators=[Required()])
    birthday  = DateField('生日：', format='%Y-%m-%d',validators=[Required()])
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

class loginForm(FlaskForm):
    email = StringField('Email：',validators=[Required()],render_kw={"placeholder": "Email"})
    password = PasswordField('密碼：', validators=[Required()],render_kw={"placeholder": "密碼"})


