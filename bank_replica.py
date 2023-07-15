import re
import mysql.connector
import pwinput

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="86emilin123#",
    database="BANK_REPLICA"
)

myCursor = mydb.cursor()


def validate(f_name, l_name, mob_no, password):

    if re.match(r"^[a-zA-Z]*$", f_name) is None:
        print(f_name, "Only letters allowed for first name")

    if re.match(r"^[a-zA-Z]*$", l_name) is None:
        print("Only letters allowed for last name")

    if re.match(r"^\d{10}$", mob_no) is None:
        print("Please enter your correct mobile number(10 digit)")
    if re.match(r"^\S{8,10}$", password) is None:
        print("Password length should be between 8 and 10. No spaces are allowed ")
    else:
        return 1


class UserRegister:
    def __init__(self, f_name, l_name, mob_no, acct_no, password):
        self.f_name = f_name
        self.l_name = l_name
        self.mob_no = mob_no
        self.acct_no = acct_no
        self.password = password

    def register(self):
        result = myCursor.callproc('insert_user', [f_name, l_name, mob_no, acct_no, password])
        mydb.commit()
        # sql="SELECT id FROM bank_user where account_no='{}'".format(self.acct_no)
        # print(sql)
        myCursor.execute("SELECT id FROM bank_user where account_no='{}'".format(self.acct_no))
        myresult = myCursor.fetchone()
        print(myresult)
        print("Registered Successfully.Your user id is ", myresult)


class Login:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

    def login(self):
        result = myCursor.callproc('check_valid_user', [self.user_id, self.password, 0])
        return result[2]


class Deposit(Login):
    def __init__(self, user_id, password, amount):
        super().__init__(user_id, password)
        self.amount = amount

    def deposit(self):
        result = myCursor.callproc('depositing', [self.user_id, self.amount])
        mydb.commit()
        return result


class Withdraw(Login):
    def __init__(self, user_id, password, amount):
        super().__init__(user_id, password)
        self.amount = amount

    def withdraw(self):
        result = myCursor.callproc('withdrawal', [self.user_id, self.amount])
        mydb.commit()
        return result


try:
    value = input("Please Enter 1 for Register or 2 for LOGIN  :")

    if value == '1':

        '''f_name = input("first_name : ")
        if re.match(r"^[a-zA-Z]*$", f_name) is None:
            raise Exception("Only letters allowed")
        l_name = input("last_name : ")
        if re.match(r"^[a-zA-Z]*$", l_name) is None:
            raise Exception("Only letters allowed")
        mob_no = input("mobile_no : ")
        if re.match(r"^\d{10}$", mob_no) is None:
            raise Exception("Please enter your correct mobile number(10 digit)")
        else:
            mob_no = int(mob_no)
        acct_no = input("account_no : ")
        password = pwinput.pwinput("Whats your password? :")
        if re.match(r"^\S{8,10}$", password) is None:
            raise Exception("Password length should be between 8 and 10. No spaces are allowed ")'''
        flag2 = 1
        while flag2:
            f_name = input("first_name : ")
            l_name = input("last_name : ")
            mob_no = input("mobile_no : ")
            acct_no = input("account_no : ")
            password = pwinput.pwinput("Whats your password? :")
            if validate(f_name, l_name, mob_no, password) == 1:
                flag2 = 0
        user1 = UserRegister(f_name, l_name, mob_no, acct_no, password)
        user1.register()

    elif value == '2':

        user_id = int(input("User_id : "))
        password = pwinput.pwinput("Whats your password? :")

        user1 = Login(user_id, password)
        user1.login()

        if user1.login() == 1:
            print("Successfully logged in")
        else:
            raise Exception("Unsuccessfull login")

        flag = True
        while flag:
            value = input("Please Enter 1 for DEPOSITING or 2 for WITHDRAWAL or 3 for balance_checking or 4 logout  :")
            if value == '1':
                amount = int(input("Enter the depositing amount :"))
                if amount > 0:
                    user1 = Deposit(user_id, password, amount)
                    user1.deposit()
                else:
                    raise Exception("Depositing amount should be greater than zero")
            elif value == '2':
                amount = int(input("Enter the withdrawal amount :"))
                if amount > 0:
                    user1 = Withdraw(user_id, password, amount)
                    user1.withdraw()
                else:
                    raise Exception("Withdraw amount should be greater than zero")
            elif value == '3':
                sql = "SELECT balance FROM bank_user WHERE id = {}".format(user_id)

                myCursor.execute(sql)

                myresult = myCursor.fetchone()
                print("Balance Amount is ", myresult[0])
            elif value == '4':
                flag = False

            else:
                raise Exception("entered option is invalid")
    else:
        raise Exception("Enter 1 or 2")
except Exception as e:
    print(e)
except TypeError as e:
    print(e)
