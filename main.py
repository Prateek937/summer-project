import os
import linux_basic as linux
import linux
import docker
import hadoop
import apache_web
import cv
import aws 
import chatbot
import texttospeech
import kubernetes
import train_your_model
os.system("tput setaf 6")
os.system("clear")
operating_sys = input("Where u want to run prog ? (local/Remote) : ")
if operating_sys == 'remote':
    ip = input("Enter remote IP : ")
else:
    ip = 0
print("{}:{}".format(operating_sys, ip))


while True:
    os.system('tput setaf 5')
    print("""
        Main Menu:
        -----------------------------------------------------
            1. Linux
            2. Docker
            3. Hadoop
            4. AWS Cloud
            5. Apache httpd Server
            6. Polly
            7. Computer Vision
            8. Kubernetes
            9. Train Your Model
            10. Seek help
            11.Exit 
        -----------------------------------------------------   
        """)
    os.system("tput setaf 2")
    choice  = ""
    while choice == "":
        choice = input("Enter choice : ")
    
    choice = int(choice)

    if operating_sys == "remote" or operating_sys == "local":
        if choice == 1:
            os.system("clear")
            linux.linux()

        elif choice == 2:
            os.system("clear")
            docker.docker(operating_sys, ip)

        elif choice == 3:
            os.system("clear")
            hadoop.hadoop()

        elif choice == 4:
            os.system("clear")
            aws.aws()

        elif choice == 5:
            os.system("clear")
            apache_web.webserver()

        elif choice == 6:
            texttospeech.process_file(input("File Path: "))
        
        elif choice == 7:
            cv.cv()
        elif choice == 8:
            kubernetes.kubernetes()
        elif choice == 10:
            chatbot.bot()
        elif choice == 9:
            train_your_model.train_your_model()
        elif choice == 11:
            exit()
        else:
            os.system("tput setaf 1")
            print("Invalid Input! ")




