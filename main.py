import os
import random
import pandas as pd
from cryptography.fernet import Fernet
import base64


path = "C:\\Users\\SANJAY RATHOD\\Downloads\\PROJECT\\GPTCHALLENGE\\database.xlsx"
edf = pd.read_excel(path,engine="openpyxl")

IScore = 0


c = "R"
while c == "R":
    status = str(input("Hello mister or miss could you please tell me if you have an account (yes or no) ?:"))
    if status == "no" or status == "NO":
        print("Ow dont worry lets get you setup.")
        SUsername = input("Please Tell me the Username you want: ")
        lenusername = len(SUsername)
        if lenusername > 3:
            print("good")
            S1Password = input("Please Enter your password it must be long: ")
            lenS1Password = len(S1Password)
            if lenS1Password > 8:
                S2Password = input("Please enter your paswword again: ")
                if S1Password == S2Password:
                    key = Fernet.generate_key()
                    F = Fernet(key)
                    BPassword = S2Password.encode()
                    EPassword = F.encrypt(BPassword)
                    SEPass = base64.urlsafe_b64encode(EPassword).decode()
                    key_str = base64.urlsafe_b64encode(key).decode()
                    df = pd.DataFrame({"Username":SUsername,"Password":SEPass,"Key":key_str,"Score":IScore},index = [1])
                    edf = pd.read_excel(path,engine="openpyxl")
                    cdf = pd.concat([edf,df],ignore_index=True)
                    cdf.to_excel(path ,index = False , engine = "openpyxl")
                    c = "exit"
                else:
                    print("your password does not match.")
            else:
                print("the password must be longer than 8 characters.")
        else:
            print("the username must be longer than 3 characters.")
    if status == "yes" or status == "YES":
        print("Gotchya lets get you logged in now.")
        LUsername = input("now tell me your username that you signed up with: ")
        if LUsername in edf['Username'].values:
            user_row = edf[edf['Username'] == LUsername]
            LDPassword = user_row['Password'].values[0]  
            DKey = user_row["Key"].values[0]
            BDKey = base64.urlsafe_b64decode(DKey)
            F = Fernet(BDKey)
            BLDPassword = base64.urlsafe_b64decode(LDPassword)
            DDPassword = F.decrypt(BLDPassword)
            SDDPassword = DDPassword.decode()
            LPassword = input("Now enter your password: ")
            if SDDPassword == LPassword:
                DIScore = user_row["Score"].values[0]
                print("Boi you are successfully logged in")
                print("your current score is",DIScore)
                ask = str(input("Do you want to play the game?: "))
                if ask == "yes" or ask == "Yes":
                        X = "ACTIVE"
                        ranger = str(input("do you want EASY,Medium,Hard or DAMN mode?: "))
                        if ranger == "EASY":
                            ran = 10
                            scorer = 2
                        if ranger == "Medium":
                            ran = 200
                            scorer = 5
                        if ranger == "Hard":
                            ran = 500
                            scorer = 10
                        if ranger == "DAMN":
                            ran = 1000
                            scorer = 50
                        number = random.randrange(0,ran)
                        Unumber = int(input("Enter your guese or if you give up type '112345': "))
                        if Unumber != "i give up":
                            if number > Unumber:
                                print("your close but try guessing a bit higher number.")
                                Unumber = int(input("Enter your guese or if you give up type 'i give up': "))
                            if number < Unumber:
                                print("you are close but try thinking a bit lower number.")
                                Unumber = int(input("Enter your guese or if you give up type 'i give up': "))
                            if number == Unumber:
                                X = "DEACTIVATED"
                                UDIScore = user_row["Score"].values[0]
                                FScore = UDIScore + scorer
                                print("DAMN boi you guessed it right here is your",scorer,"points added to your account making a total of",FScore,"points.")
                                edf.loc[edf['Username'] == LUsername, 'Score'] = FScore
                                edf.to_excel(path ,index = False , engine = "openpyxl")
            else:
                print("your password does not match.")
        else:
            print("your username does not exists in the database.")
    c = input("type R to continue or type exit: ")
