from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, MetaData, Table, Column, String, inspect
import datetime
from datetime import datetime
import hashlib
import os
import imageReader
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'test_db.db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
ALLOWED_TOKENS = ['sampleToken']
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not inspect(engine).has_table("Swipes"):
    metadata = MetaData(engine)
    table = Table('Swipes', metadata,
        Column('hash_string', String),
        Column('ts', String, primary_key=True)
    )
    metadata.create_all()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

############################################################################
#                                Schemas                                   #
############################################################################


class Swipes(db.Model):
    hash_string = db.Column('hash_string', db.String(128))
    ts = db.Column('ts', db.String, primary_key=True)

    def __init__(self, hash_string):
        ts = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash_string = hash_string
        self.ts = ts

    def __repr__(self):
        return '<Swipe %r>' % self.hash_string

############################################################################
#                              Endpoints                                   #
############################################################################


@app.route('/')
def home_page():
    return 'hello world!'


@app.route('/picture', methods=['POST'])
def post_picture():
    if 'file' not in request.files:
        return {"isOfAge": False, "license_id": "Missing file"}
    if request.form.get("token") not in ALLOWED_TOKENS:
        return {"isOfAge": False, "license_id": "Missing/Invalid token"}
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        results_dict = imageReader.readLicense(filename)
        if results_dict['isOfAge']:
            insertHash(results_dict['license_id'], request.form.get("token"))
        result_json = json.dumps(results_dict)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return result_json


@app.route('/picture', methods=['GET'])
def get_picture():
    if 'file' not in request.files:
        return {"isOfAge": False, "license_id": "Missing file"}
    if request.form.get("token") not in ALLOWED_TOKENS:
        return {"isOfAge": False, "license_id": "Missing/Invalid token"}
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        results_dict = imageReader.readLicense(filename)
        license_id = checkHash(results_dict['license_id'])
        timestamps = checkHash(license_id, request.form.get("token"))
        return json.dumps(timestamps)


############################################################################
#                           Other Functions                                #
############################################################################
def insertHash(IDString, token):
    encoded_string = (IDString + token).encode()
    hash_obj = hashlib.sha512(encoded_string)
    db_string = hash_obj.digest()
    new_swipe = Swipes(db_string)
    db.session.add(new_swipe)
    db.session.commit()


def checkHash(IDString, token):
    encoded_string = (IDString + token).encode()
    hash_obj = hashlib.sha512(encoded_string)
    db_string = hash_obj.digest()
    results = Swipes.query.filter(Swipes.hash_string == db_string)
    return results


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


############################################################################
#                                run app                                   #
############################################################################

if __name__ == "__main__":
    app.run(host='localhost', port='8080')