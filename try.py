# # # # def search():
# # # #     hosp=Hospital.query.all()
# # # #     covid_Hospitals_list=[]
import bcrypt

# example password
password = 'passwordabc'
  
# converting password to array of bytes
bytes = password.encode('utf-8')
  
# generating the salt
salt = bcrypt.gensalt()
  
# Hashing the password
hash = bcrypt.hashpw(bytes, salt)
print(type(hash))
# Taking user entered password 
userPassword =  'passwordabc'
  
# encoding user password
userBytes = userPassword.encode('utf-8')
  
# checking password
result = bcrypt.checkpw(userBytes, hash)
print(result)
# # # #     for i in hosp:
# # # #         if i.disease=='covid':
# # # #             covid_Hospitals_list.append(i)
# # # #             # return True
# # # #             print(i.address)
# # # #     print(covid_Hospitals_list)
# # class A:
# #     __name="Kedar"
# #     def check_id(self):
# #         print(f"my name is {self.__name}")
# # a=A()
# # # print(a.__name)
# # # A.__name="!"
# # a.__name="Swami"
# # # print(A.__name)
# # # print(a.__name)
# # # print(id(A.__name))
# # a.check_id()
# # class A:
# #     __dic={}
# #     __dic["name"]="Kedar"
# #     __dic["name"]="swami"
# # a=A()
# print(a.__dic["name"])

# from pymongo import MongoClient
# connection = MongoClient("localhost", 27017)

# database = connection['HealthCare']

# database.Users.insert_one({"name":"kedarSwami","gender":"male"})
# print("File inserted Succesfully")
