from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
import pandas as pd
import os
import base64
from ChatBot_Response import chatbot_response
from keras.utils import load_img, img_to_array
from keras.models import load_model
import warnings
from PIL import Image
warnings.filterwarnings("ignore")
from pymongo import MongoClient
import bcrypt

connection = MongoClient("localhost", 27017)
db = connection["HealthCare"]
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b"82736781_@*@&(796*5&^5)"
# covid_19_model = load_model(r"Trained_Models\covid_model.h5")
# skin_model = load_model(r"Trained_Models\skin_d.h5")
# app.config["SQLALCHEMY_DATABASE_URI"] = "mongodb://localhost:27017"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class App_Data:
    __username = str()
    __login_status = False
    __msg = str()
    __user={}
    def __init__(self):
        print("Current status")
        # print("Login Status: ", self.__login_status)
        print("Current status: ", self.__username)

    def setstatus(self, username=False, login_status=False, msg="",user={}):
        self.__username = username
        self.__login_status = login_status
        self.__msg = msg
        self.__user=user

    def getstatus(self):
        return [self.__username, self.__login_status, self.__msg,self.__user]

    # def start(self,username):
    #     print(self.__model.start())
    #     return [self.__msg,self.__login_status,
    #     self.__model.start(username)]

    # def logout(self):
    #     self.__login_status=False
    #     self.__model.start()
    #     return self.__model


global model
model = App_Data()


class Covid_Disease:
    __covid_19_model = load_model(r"Trained_Models\covid_model.h5")
    def getmodel(self):
        return self.__covid_19_model

    


class Brain_Tumor:
    __mri_model = load_model(r"Trained_Models\BrainTumor.h5")

    # preprocessing for brain Tumor module
    def preprocess_img_mri(self, img_path):
        self.__xtest_image = load_img(img_path, target_size=(150, 150, 3))
        self.__xtest_image = img_to_array(self.__xtest_image)
        self.__xtest_image = np.expand_dims(self.__xtest_image, axis=0)
        self.__predictions = (
            self.__mri_model.predict(self.__xtest_image) > 0.5
        ).astype("int32")
        return self.__predictions

    def get_tumor_result(self):
        if request.method == "POST":
            self.__labels = [
                "Brain Tumor type- Glioma",
                "Brain Tumor type-Meningioma",
                "Don't Worry, you don't have tumor",
                "Brain Tumor type-Pituitary",
            ]
            self.__img = request.files["mri"]
            self.__img.save(
                os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    app.config["UPLOAD_FOLDER"],
                    secure_filename(self.__img.filename),
                )
            )
            self.__file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(self.__img.filename),
            )
            # print(file_path)
            self.__result = self.preprocess_img_mri(self.__file_path)
            self.__raddr, self.__rlink, self.__rcity = get_hospitals("brain")
            return render_template(
                "answer.html",
                res=self.__labels[(np.where(self.__result[0] == 1))[0][0]],
                raddr=self.__raddr,
                rlink=self.__rlink,
                rcity=self.__rcity,
            )


class Bone_Fracture:
    __bone_model = load_model(r"Trained_Models\best_model_bone.h5")

    def getbone(self):
        if request.method == "POST":
            self.__img = request.files["bone"]
            self.__file_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(self.__img.filename),
            )
            self.__img.save(self.__file_path)
            self.__xtest_image = load_img(self.__file_path, target_size=(224, 224))
            self.__xtest_image = img_to_array(self.__xtest_image)
            self.__xtest_image = np.expand_dims(self.__xtest_image, axis=0)
            self.__predictions = self.__bone_model.predict(self.__xtest_image)
            self.__predictions = np.argmax(self.__predictions, axis=1)
            print(self.__predictions[0])
            self.__raddr, self.__rlink, self.__rcity = get_hospitals("bone")
            if self.__predictions[0] == 0:
                _predictions = "Bone Fractured"
            else:
                _predictions = "Bone Not Fractured"
            print(_predictions)
            self.__bone = True
            return render_template(
                "answer.html",
                res=self.__predictions,
                raddr=self.__raddr,
                rlink=self.__rlink,
                rcity=self.__rcity,
                bone=self.__bone,
            )


# -------------------------------------------------------------------------------------------------------------


def insert_image(img,disease_name="Profile"):
    # with open(img, "rb") as image_file:
    encoded_string = base64.b64encode(img)
    # current_user=db.Users.find_one()
    abc = db.Users.update_one({"email":((model.getstatus())[3])["email"]},{"$set":{"Diseases":[ {disease_name:encoded_string}]}},upsert=True)
    print("Success")


def retrieve_image():
    
    data = db.Users.find_one({"email":(model.getstatus()[3])["email"]})
    print("Type:", type(data))
    # print(data)
    print("__________________________________________________________________________________")
    # print(img1)
    print(data["Diseases"])
    with open("test2.jpg", "wb") as im:
        im.write(base64.b64decode(img1))


def get_hospitals(disease):
    __rows = pd.read_csv(
        r"C:\Users\asus\OneDrive\Ked data\VS Code\Python\Health-Care\static\Covid.csv"
    )
    __hosdetail = __rows[__rows["Diseases"] == disease]
    # create list for Address, hospital name,link
    __raddr, __rlink, __rcity = (
        list(__hosdetail["Address"]),
        list(__hosdetail["Google Map Link"]),
        list(__hosdetail["City"]),
    )
    return (__raddr, __rlink, __rcity)


# model = pickle.load(open("Trained_Models/heart.pkl", "rb"))
# model_diabetes = pickle.load(open("Trained_Models/DiabetesModel96.pkl", "rb"))

# class hospital(db.Model):
#     userName = db.Column(db.String, primary_key=True, nullable=False)
#     address = db.Column(db.String, primary_key=False, nullable=False)
#     link = db.Column(db.String, primary_key=False, nullable=False)
#     city = db.Column(db.String, primary_key=False, nullable=False)
#     disease = db.Column(db.String, primary_key=False, nullable=False)


@app.route("/predict", methods=["POST"])
def predict():
    __text = request.get_json().get("message")
    __res = chatbot_response(__text)
    __message = {"answer": __res}
    return jsonify(__message)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email_list = db.Users.find_one({"email": request.form["mail"]})
        print(email_list)
        if email_list:
            # print(type(__pass))
            # print(__pass)
            try:
                if bcrypt.checkpw(
                    (request.form["password"]).encode("utf-8"),
                    email_list["encrypted_password"],
                ):
                    print(email_list["name"])
                    model.setstatus(email_list["name"], True,user=email_list)
                    return redirect("/")
                else:
                    # print("Here wroo")
                    model.setstatus(msg="Wrong Password")
                    return render_template("login.html", viewBag=model)
            except:
                model.setstatus(msg="Try Again")
                return redirect("/login")

        else:
            model.setstatus(msg="User doesn't exist! Please register yourself")
            return render_template("login.html", viewBag=model)
    model.setstatus()
    return render_template("login.html", viewBag=model)


@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    model.setstatus()
    return redirect("/")


@app.route("/")
def refresh():
    return render_template("homepage.html", viewBag=model)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        fn = request.form["fname"]
        ln = request.form["lname"]
        email = request.form["email"]
        gender = request.form["inlineRadioOptions"]
        age = int(request.form["age"])
        password = request.form["password"]
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        enc_password = bcrypt.hashpw(bytes, salt)
        name = fn + " " + ln
        # print(name, email, password, email, gender)
        new_doc = {
            "name": name,
            "email": email,
            "gender": gender,
            "age": age,
            "encrypted_password": enc_password,
        }
        try :
            db.Users.insert_one(new_doc)
        except:
            model.setstatus(msg="User already exist! Please login to continue ")
            return redirect("/registration")
        print("Committed")
        return redirect("/login")
    model.setstatus()
    return render_template("registration.html",viewBag=model)


@app.route("/Covid_19",methods=["GET","POST"])
def Covid_19():
    if request.method == "POST":
        cobj=Covid_Disease()
        covid_19_model=cobj.getmodel()
        img = request.files["covid"].read()
        img=base64.b64encode(img)
        print(img,"______________",type(img))
        # img=Image.open(img)
        # img=base64.b64encode(img)
        # file_path = os.path.join(
        #     os.path.abspath(os.path.dirname(__file__)),
        #     app.config["UPLOAD_FOLDER"],
        #     secure_filename(img.filename),
        # )
        # img.save(file_path)
        insert_image(img,"Covid-19")
        img=retrieve_image()
        xtest_image = load_img(img, target_size=(100, 100, 3))
        xtest_image = img_to_array(xtest_image)
        xtest_image = np.expand_dims(xtest_image, axis=0)
        predictions = (covid_19_model.predict(xtest_image)).astype(
            "int32"
        )
        predictions = predictions[0][0]
        raddr, rlink, rcity = get_hospitals("covid")
        if predictions == 0:
            predictions = "Covid 19 Negative"
        elif predictions == 1:
            predictions = "Covid 19 Positive"
        return render_template(
            "answer.html",
            res=predictions,
            raddr=raddr,
            rlink=rlink,
            rcity=rcity,
        )
    return render_template("Covid_19.html", viewBag=model)


# @app.route("/Heart_Disease_Prediction")
# def Heart_Disease_Prediction():
#     if app.config["LOGIN_STATUS"]:
#         return render_template(
#             "Heart_Disease.html",
#             status=app.config["LOGIN_STATUS"],
#             username=app.config["USERNAME"],
#         )
#     return redirect("/login")


# @app.route("/diabetes", methods=["GET", "POST"])
# def diabetes():
#     if request.method == "POST":
#         # diver code for testing the model
#         para = [
#             float(request.form["hlbp"]),
#             float(request.form["chol"]),
#             float(request.form["chol2"]),
#             float(request.form["bmi"]),
#             float(request.form["smoker"]),
#             float(request.form["stroke"]),
#             float(request.form["cdmi"]),
#             float(request.form["phyacti"]),
#             float(request.form["veg"]),
#             float(request.form["drink"]),
#             float(request.form["genhealth"]),
#             float(request.form["mh"]),
#             float(request.form["ph"]),
#             float(request.form["walk"]),
#             float(request.form["age"]),
#             float(request.form["education"]),
#             float(request.form["income"]),
#         ]
#         tip = [para]
#         res = model_diabetes.predict(np.array(tip))
#         if res[0] == 0:
#             answer = "Non-Diabetic"
#         else:
#             answer = "Diabetic"
#         return render_template("answer.html", res=answer)
#     if app.config["LOGIN_STATUS"]:
#         return render_template(
#             "diabetes.html",
#             status=app.config["LOGIN_STATUS"],
#             username=app.config["USERNAME"],
#         )
#     return redirect("/login")


@app.route("/Bone_Fracture_Detection")
def Bone_Fracture_Detection():
    if (model.getstatus())[1]:
        return render_template("Bone_Fracture.html", viewBag=model)
    return redirect("/login")


@app.route("/Skin_Cancer")
def Skin_Cancer():
    if (model.getstatus())[1]:
        return render_template("Skin_Cancer.html", viewBag=model)
    return redirect("/login")


@app.route("/Brain_Tumor_Detection")
def Brain_Tumor_Detection():
    if (model.getstatus())[1]:
        return render_template("Brain_Tumor.html", viewBag=model)
    return redirect("/login")


@app.route("/getmri", methods=["POST"])
# prediction code for brain tumor detection
def getmri():
    b = Brain_Tumor()
    return b.get_tumor_result()


# def searchHos():


# def searchHos():
#     db_file = r"C:\Users\asus\OneDrive\Ked data\VS Code\Python\Health-Care\instance\database.db"
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#     except sqlite3.Error as e:
#         print(e)
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Sheet1 WHERE diseases='covid'")
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)





# @app.route("/getskin", methods=["POST"])
# def getskin():
#     if request.method == "POST":
#         img = request.files["skin"]
#         file_path = os.path.join(
#             os.path.abspath(os.path.dirname(__file__)),
#             app.config["UPLOAD_FOLDER"],
#             secure_filename(img.filename),
#         )
#         img.save(file_path)
#         img = load_img(file_path, target_size=(224, 224))
#         img = img_to_array(img)
#         test_image = np.expand_dims(img, axis=0)
#         a = np.argmax(skin_model.predict(test_image), axis=1)
#         print(a[0])
#         disease_list = [
#             "Eczema 1677",
#             "Melanoma",
#             "Atopic Dermantitis",
#             "Basal Cell Carcinoma (BCC)",
#             "Mealanocytic Nevi (NV)",
#             "Benign Keratosis-like Lessions (BKL)",
#             "Psoriasis pictures lichen Planus and related diseases",
#             "Seaborrheic Keratoses and other Benign Tumors",
#             "Tinea Ringworm Candidiasis and other fungal infections",
#             "Warts Molluscum and other Viral Infections",
#         ]
#         disease = disease_list[int(a[0] + 1)]
#         print(disease)
#         raddr, rlink, rcity = get_hospitals("skin")
#     return render_template(
#         "answer.html", res=disease, raddr=raddr, rlink=rlink, rcity=rcity
#     )


@app.route("/getbone", methods=["POST"])
def getbone():
    b = Bone_Fracture()
    b.getbone()


# @app.route("/getValue", methods=["POST"])
# def getValue():
#     if request.method == "POST":
#         oldpeak = float(request.form["oldpeak"])
#         slope = int(request.form["slope"])
#         ca = int(request.form["ca"])
#         thal = int(request.form["thal"])
#         sex = int(request.form["sex"])
#         age = int(request.form["age"])
#         cp = int(request.form["chaistpain"])
#         restecg = int(request.form["wave"])
#         thalach = int(request.form["hrate"])
#         fbs = int(request.form["bloodsugar"])
#         trestbps = int(request.form["bloodpressure"])
#         chol = int(request.form["serum"])
#         exang = int(request.form["anigna"])
#         input_data = [
#             age,
#             sex,
#             cp,
#             trestbps,
#             chol,
#             fbs,
#             restecg,
#             thalach,
#             exang,
#             oldpeak,
#             slope,
#             ca,
#             thal,
#         ]
#         print(input_data)
#         answer = input_data
#         input_data = np.array(input_data)
#         input_data = input_data.reshape(1, -1)
#         print("Input_Data: ", input_data)
#         answer = model.predict(input_data)
#         print(answer)
#         raddr, rlink, rcity = get_hospitals("heart")
#         if answer:
#             answer = "Don't Worry You Don't Have a serious Heart Condition"
#         else:
#             answer = "Sorry to say that you might have a serious heart Condition. Please refer to a Doctor and Get treated!"
#         return render_template(
#             "answer.html", res=answer, raddr=raddr, rlink=rlink, rcity=rcity
#         )


if __name__ == "__main__":
    app.run(debug=True, port=2000)
    # searchHos()
    # hosp=Hospital.query.all()
    # covid_Hospitals_list=[]

    # for i in hosp:
    #     if i.disease=='covid':
    #         covid_Hospitals_list.append(i)
    #         # return True
    #         print(i.address)
    # print(covid_Hospitals_list)


###############   Veerkrushna Dalvi
