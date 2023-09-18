

class Current_User:
    __login_status = False
    __username = str()

    def __init__(self):
        print("Current status")
        print("Login Status: ", self.__login_status)
        print("Current status: ", self.__username)
    

def new_user():
    new_user = Current_User()
    return new_user
