# # def search():
# #     hosp=Hospital.query.all()
# #     covid_Hospitals_list=[]

# #     for i in hosp:
# #         if i.disease=='covid':
# #             covid_Hospitals_list.append(i)
# #             # return True
# #             print(i.address)
# #     print(covid_Hospitals_list)
class A:
    
    name="Kedar"
    def check_id(self):
        print(id(self.__name))
a=A()
# print(a.__name)
A.__name="!"
a.__name="Swami"
print(A.__name)
print(a.__name)
print(id(A.__name))
a.check_id()



