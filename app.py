import os
from urllib import request
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3307/uok_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id" , db.Integer , primary_key = True, autoincrement=True)
    predictedGender = db.Column(db.String(100))
    predictedAge = db.Column(db.String(100))
    actualAge = db.Column(db.String(100))
    actualGender = db.Column(db.String(100))
    image = db.Column(db.LargeBinary(length=(2**25)-1))
   

    def __init__(self,predictedGender,predictedAge,actualAge,actualGender,image):
            self.predictedGender = predictedGender
            self.predictedAge = predictedAge
            self.actualAge = actualAge
            self.actualGender = actualGender
            self.image = image

@app.route("/add-student" ,methods=["POST" , "GET"])
def addStudent():
    predictedGender = None
    predictedAge = None
    actualAge = None
    actualGender = None

    if request.method == "POST":
        predictedGender = request.form["predictedGender"]
        predictedAge = request.form["predictedAge"]
        actualAge = request.form["actualAge"]
        actualGender = request.form["actualGender"]
        image = request.files["image"]
        basepath = ""
        file_path = os.path.join(
        basepath, image.filename)
        image.save(file_path)
        img = convertToBinaryData(file_path)

        new_user = users(predictedGender,predictedAge,actualAge,actualGender,image) ; 
        db.session.add(new_user)
        db.session.commit()
        print("Success")


    return "Success "

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)