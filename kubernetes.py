import os
import subprocess as sp

def kubernetes():
    while True:
        os.system('tput setaf 5')
        print("""
            Main Menu:
            -----------------------------------------------------
                1. Launch Pod
                2. Get Pods
                3. Launch Deployment
                4. Get Deployments
                5. Launch Service
                6. Get Services
                7. Launch ReplicaSet
                8. Get ReplicaSets
                9. Launch Deployment with ReplicaSet
                10. Launch Deployment with ReplicaSet and Service
                11. Main Menu
            -----------------------------------------------------   
            """)
        os.system("tput setaf 2")
        choice  = ""
        while choice == "":
            choice = input("Enter choice : ")

        choice = int(choice)

        if choice == 1:
            sp.call("kubectl run {} --image={}".format(input("Enter Pod Name: "), input("Enter Image Name: ")), shell = True)
        elif choice == 2:
            sp.call("kubectl get pods", shell = True)
        elif choice == 3:
            sp.call("kubectl create deployment {} --image={}".format(input("Enter Deployment Name: "), input("Enter Image Name: ")), shell = True)
        elif choice == 4:
            sp.call("kubectl get deployments", shell = True)
        elif choice == 5:
            sp.call("kubectl expose pod {} --port={}".format(input("Enter Pod Name: "), input("Enter Port Number: ")), shell = True)
        elif choice == 6:
            sp.call("kubectl get services", shell = True)
        elif choice == 7:
            sp.call("kubectl create replicaset --image={}".format(input("Enter Image Name: ")), shell = True)
        elif choice == 8:
            sp.call("kubectl get replicaset", shell = True)
        elif choice == 9:
            sp.call("kubectl create deployment {} --image={} --replicas={}".format(input("Enter Deployment Name: "), input("Enter Image Name: "), input("Enter Number of Replicas: ")), shell = True)
        elif choice == 10:
            sp.call("kubectl create deployment {} --image={} --replicas={} --port={}".format(input("Enter Deployment Name: "), input("Enter Image Name: "), input("Enter Number of Replicas: "), input("Enter Port Number: ")), shell = True)
        elif choice == 11:
            break