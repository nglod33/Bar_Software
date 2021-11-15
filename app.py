from datetime import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, PrimaryKeyConstraint, Binary
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////test_db"
db = SQLAlchemy(app)

############################################################################
#                                Schemas                                   #
############################################################################

class Swipes(db.Model):
    hash = db.Column(db.String, primary_key=True)

    def __init__(self, hash):
        self.hash = hash
        self.timeStamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

############################################################################
#                              Endpoints                                   #
############################################################################

@app.route('/')
def home_page():
    return 'hello world!'


@app.route('/picture', methods=['POST'])
def post_picture():
    return 'post_picture'


@app.route('/picture', methods=['GET'])
def get_picture():
    return 'get_picture'


############################################################################
#                           Other Functions                                #
############################################################################
def insertHash(IDString):
    # License ID string: "DAQ"
    pass

def checkAge(IDString):
    # Date of birth field: "DBB"
    pass

############################################################################
#                                run app                                   #
############################################################################

if __name__ == "__main__":
    app.run(host='localhost', port='8080')