import subprocess as sb
from time import sleep
import os

import boto3

def launch_ec2_instances(count, role):
	global NAMENODE_IP
	ec2_client = boto3.client('ec2')

	response = ec2_client.run_instances(
	    ImageId="ami-06ca3ca175f37dd66",
	    InstanceType="t3.micro",
	    MinCount=count,
	    MaxCount=count,
	    SecurityGroups=['default']  # Assuming the default security group is used
	)

	instance_ids = [instance['InstanceId'] for instance in response['Instances']]

	# Update the security group inbound rule to allow all traffic
	ec2_resource = boto3.resource('ec2')
	security_group = ec2_resource.SecurityGroup(response['Instances'][0]['SecurityGroups'][0]['GroupId'])
	try:
		security_group.authorize_ingress(
    	    IpPermissions=[
    	        {
    	            'IpProtocol': '-1',
    	            'FromPort': -1,
    	            'ToPort': -1,
    	            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    	        }
    	    ]
    	)
	except:
		pass    
	print(response)
	response[0].wait_until_running()
	if role == 'namenode':
		NAMENODE_IP = response[0].public_ip_address
	

# for Configuring files
def file_handeling(file_path, ip, namenode):
	file = open("{}".format(file_path), 'r')
	string_list = file.readlines()
	file.close()

	index_initial = string_list.index('<configuration>\n')
	index_final = string_list.index('</configuration>\n')

	del string_list[index_initial+1:index_final]
	if file_path == '/etc/hadoop/hdfs-site.xml':
		string_list.insert(index_initial + 1, "<property>\n")
		if namenode == True:
			string_list.insert(index_initial + 2, "<name>dfs.name.dir</name>\n")
		else:
			string_list.insert(index_initial + 2, "<name>dfs.data.dir</name>\n")
		string_list.insert(index_initial + 3, "<value>/nn</value>\n")
		string_list.insert(index_initial + 4, "</property>\n")
	elif file_path == '/etc/hadoop/core-site.xml':
		string_list.insert(index_initial + 1, "<property>\n")
		string_list.insert(index_initial + 2, "<name>fs.default.name</name>\n")
		string_list.insert(index_initial + 3, "<value>hdfs://{}:9001</value>\n".format(ip))
		string_list.insert(index_initial + 4, "</property>\n")
	else: sb.call('echo "configuration file not found"', shell=True)

	file = open("{}".format(file_path), "w")
	new_file_content = "".join(string_list)
	file.write(new_file_content)
	file.close()
	
def configure_namenode_hadoop():
	# if Type == 1:
	# 	ip = '192.168.43.194'
	#else:
	launch_ec2_instances(1, 'namenode')
	ip = '0.0.0.0'
	sleep(1)
	os.system('tput setaf 3')
	sb.call("echo '[Namenode]'", shell=True)
	sb.call("echo 'Configuring hdfs-site.xml file...'", shell=True)

	file_handeling('/etc/hadoop/hdfs-site.xml', '0.0.0.0', True)
	sleep(1)
	sb.call("echo 'ConfiguredConfigured hdfs-site.xml file...'", shell=True)
	sleep(1)
	sb.call("echo 'Configuring core-site.xml file...'", shell=True)

	file_handeling('/etc/hadoop/core-site.xml', ip, True)
	sleep(1)
	sb.call("echo 'Configured core-site.xml file...'", shell=True)
	sleep(1)
	sb.call("echo 'Formatting Namenode...'", shell=True)
	sb.call("echo 'Y' | hadoop namenode -format",shell = True)
	# if out[0] == 0:
		
	# 	sb.call("echo 'Namenode successfully fomatted !'", shell=True)
	# else:
	# 	os.system('tput setaf 1') 
	# 	print('Something went Wrong while formatting !')
	# 	print('Trying again..')
	# 	sb.getstatusoutput("echo 'Y' | hadoop namenode -format")
	sb.call("echo 'Namenode successfully fomatted !'", shell=True)
	sleep(1)
	os.system('tput setaf 3')
	sb.call("echo 'Starting Namenode...'", shell=True)
	sb.call("echo 3 > /proc/sys/vm/drop_caches", shell=True)
	out = sb.getstatusoutput("hadoop-daemon.sh start namenode")
	
	if 'running' in out[1]:
		sb.getstatusoutput("hadoop-daemon.sh stop namenode")
		out = sb.getstatusoutput("hadoop-daemon.sh start namenode")
	if out[0] == 0:
		os.system('tput setaf 2')
		sb.call("echo 'Namenode started successfully !'", shell=True)
	else:
		os.system('tput setaf 1')
		print('Something went Wrong !')
		print(out[1])
		os.system('tput setaf 7')

def configure_datanodes_hadoop(datanode_count):
	launch_ec2_instances(int(datanode_count), 'datanode')
	sleep(1)
	os.system('tput setaf 3')
	sb.call("echo '[Datanode]'", shell=True)
	sb.call("echo 'Configuring hdfs-site.xml file...'", shell=True)

	file_handeling('/etc/hadoop/hdfs-site.xml', NAMENODE_IP, False)
	sleep(1)
	sb.call("echo 'ConfiguredConfigured hdfs-site.xml file...'", shell=True)
	sleep(1)
	sb.call("echo 'Configuring core-site.xml file...'", shell=True)

	file_handeling('/etc/hadoop/core-site.xml', NAMENODE_IP, True)
	sleep(1)
	sb.call("echo 'Configured core-site.xml file...'", shell=True)
	sleep(1)
	# if out[0] == 0:
		
	# 	sb.call("echo 'Namenode successfully fomatted !'", shell=True)
	# else:
	# 	os.system('tput setaf 1') 
	# 	print('Something went Wrong while formatting !')
	# 	print('Trying again..')
	# 	sb.getstatusoutput("echo 'Y' | hadoop namenode -format")
	os.system('tput setaf 3')
	sb.call("echo 'Starting Datanode...'", shell=True)
	sb.call("echo 3 > /proc/sys/vm/drop_caches", shell=True)
	out = sb.getstatusoutput("hadoop-daemon.sh start datanode")
	
	if 'running' in out[1]:
		sb.getstatusoutput("hadoop-daemon.sh stop datanode")
		out = sb.getstatusoutput("hadoop-daemon.sh start datanode")
	if out[0] == 0:
		os.system('tput setaf 2')
		sb.call("echo 'Datanode started successfully !'", shell=True)
	else:
		os.system('tput setaf 1')
		print('Something went Wrong !')
		print(out[1])
		os.system('tput setaf 7')

def configure_cluster():
	configure_namenode_hadoop()
	configure_datanodes_hadoop(input('Enter Datanode Count: '))
	sb.call("hadoop dfsadmin -report", shell=True)

def hadoop():
	while True:
		os.system('tput setaf 10')
		print("""
			-----------------------------------------------------
				Hadoop:
			-----------------------------------------------------	
				1. Configure Hadoop Namenode
				2. Configure Hadoop Datanode
				3. Configure the Whole Cluster
				4. Show Report
				5. Main Menu
			-----------------------------------------------------
			""")
		os.system("tput setaf 2")
		ch  = ""
		while ch == "":
			ch = input("Enter choice : ")
		ch = int(ch)
		
		os.system('tput setaf 7')
		if ch == 1:
			configure_namenode_hadoop()
		elif ch == 2:
			configure_datanodes_hadoop(input('Enter Datanode Count: '))
		elif ch == 3:
			configure_cluster()
		elif ch == 4:
			os.system("hadoop dfsadmin -report")
		elif ch == 5:
			os.system("clear")
			break
		else:
			os.system("tput setaf 1")
			print("Invalid Input!")
