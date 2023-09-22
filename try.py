import base64
from pymongo import MongoClient
connection = MongoClient("localhost", 27017)
db = connection["Sample"]

def insert_image():
    with open (r"static\bone1.jpg","rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    abc=db.TP.insert_one({"image":encoded_string})
    print("Success")

def retrieve_image():
    data = db.TP.find_one({})
    print("Type:",type(data))
    img1 = data["image"]
    print(img1)
    with open("test2.jpg", "wb") as im:
        im.write(base64.b64decode(img1))
    
    

insert_image()
retrieve_image()