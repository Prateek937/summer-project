import subprocess as sb
from time import sleep
import os
import boto3

def configure_cluster(name, nodecount):
	os.system("terraform -chdir=./hadoop init")
	os.system(f"terraform -chdir=./hadoop apply -var name={name} -var nodecount={nodecount} -auto-approve")

def delete_cluster(name, nodecount):
	os.system(f"terraform -chdir=./hadoop destroy -var name={name} -var nodecount={nodecount} -auto-approve")

def hadoop():
	while True:
		os.system('tput setaf 10')
		print("""
			-----------------------------------------------------
				Hadoop:
			-----------------------------------------------------	
				1. Get a Hadoop cluster
				2. Delete Cluster
				3. Show Report
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
			while True:
				try:
					name = input("Enter cluster name: ")
					nodecount = int(input("Enter number of nodes: "))
					break
				except:
					continue
			configure_cluster(name, nodecount)
		elif ch == 2:
			while True:
				try:
					name = input("Enter cluster name: ")
					nodecount = int(input("Enter number of nodes: "))
					break
				except:
					continue
			delete_cluster(name, nodecount)
		elif ch == 3:
			os.system("hadoop dfsadmin -report")
		elif ch == 4:
			os.system("clear")
			break
		else:
			os.system("tput setaf 1")
			print("Invalid Input!")
