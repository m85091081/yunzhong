import hashlib
import bson
from io import BytesIO
from PIL import Image
from core_module.dbmongo import Pictures
allow_formats = set(['jpeg','png','gif'])

def uploadpicture(f):
    content = BytesIO(f.read())
    try:
        mime = Image.open(content).format.lower()
        if mime not in allow_formats:
            raise IOError()
    except IOError:
            return False
    sha1 = hashlib.sha1(content.getvalue()).hexdigest()
    content = bson.binary.Binary(content.getvalue()) 
    return Pictures.savepicture(content,mime,sha1)

def uploadcover(f):
    content = f
    sha1 = hashlib.sha1(content).hexdigest()
    return Pictures.savepicture(content,"jpeg",sha1)
