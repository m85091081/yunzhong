from flask import render_template,Blueprint
from core import app
admbp = Blueprint('admbp', __name__ , template_folder='../core_template/templates')

@admbp.route('/')
def admindex():
    return render_template('admin/index.html')
