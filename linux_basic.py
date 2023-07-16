import time
import os


def linux(T, ip):
    ch = 0
    while ch != 4:
        os.system('tput setaf 10')
        print("""
            -----------------------------------------------------
                Linux:
            -----------------------------------------------------   
                1. date
                2. calender
                3. Show IP
                4. Main Menu
            -----------------------------------------------------
            """)
        os.system("tput setaf 2")
        ch  = ""
        while ch == "":
            ch = input("Enter choice : ")
        ch = int(ch)
            
        os.system('tput setaf 7')

        if ch == 1:
            os.system("tput setaf 3")
            if T == 'local':
                    os.system("date")
            else:
                    os.system("ssh  {} date".format(ip))
            input()
        elif ch == 2:
            os.system("tput setaf 3")
            if T == 'local':
                os.system("cal")
            else:
                os.system("ssh {} cal".format(ip))
            input()

        elif ch == 3:
            os.system("tput setaf 3")
            if  T == 'local':
                os.system("ifconfig")
            else:
                os.system("ssh {} ifconfig enp0s3".format(ip))
            input()

        elif ch == 4:
            os.system("clear")
            break

        else:
            os.system("tput setaf 1")
            print("Invalid Input!")
            


