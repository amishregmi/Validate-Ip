import os
import re
import netmiko
from netmiko import ConnectHandler

#EDIT the host IP username and password 
host="####"
user="##########"
pw = "#############"

execute_commaand = "show ip arp | inc "
platform = "cisco_ios"

unavailableips = False #Will print out those ips from text file that are unavailable 
errorips = False #For ips in file that don't have 3 "."s
#scl enable rh-python36 bash
#python3 ipcheck.py

#show ip arp | inc <iptocheck> The command to send.

checkip = input("Please enter m for manual enter, or f to read from file: ")

while(checkip!="m" and checkip!="f"):
	print("Invalid IP Entered")
	checkip = input("Please enter m for manual enter, or f to read from file: ")

#This function takes the command to send to the switch and checks the output of the command. Returns a string indicating whether IP is available or not.
#Only make connection once
def one_time_connect():
	try:
		device = ConnectHandler(device_type=platform, ip=host, username=user, password=pw)
		print("CONNECTED TO SWITCH")
		return device
	except Exception as e:
		print(e)
	


def connection(req_command):
		
	print("EXECUTING COMMAND")
	try:
		
		output = device.send_command(req_command)
		
		#print("THE LENGTH OF OUTPUT IS: ",len(output))
		
		if (len(output)==0):
			return "Available"
		else:
			return "Unavailable"

	except Exception as e:
		print(e)

#Manual Enter of IP.

if (checkip=="m"):

	inputip = input("Please enter ip to check: ")
	numberofdots = inputip.count('.') #To check if it's a valid IP.
	while(numberofdots!=3):
		inputip= input("Not a valid IP. Please enter a valid IP: ")
		numberofdots = inputip.count('.')
	device= one_time_connect()
	oneipcheckcommand = execute_commaand+str(inputip)
	print("SENDING THE COMMAND: ", oneipcheckcommand)
	checker = connection(oneipcheckcommand)
	print()
	if (checker=="Available"):
		print("THE IP ",inputip, " is available")
	else:
		print("THE IP ", inputip, " is unavailable")

#Import IPS FROM a file.

elif (checkip=="f"):
	#results = []
	available_ips=[]
	unavailable_ips=[]
	error_ips = []
	filename = input("Please enter the name of the file: ")
	if (os.path.exists(filename)):
		#resforeveryfile = {}
		with open(filename,'r') as f:
			device = one_time_connect()
			try:
				
				allips=f.readlines()
				listofipsinfile = [x.strip() for x in allips]
				#print("THE IP ADDRESSES ARE: ", listofipsinfile) #Saved all ips to a list.
				
				#check if the IP in every element of the list  is available.

				for one in listofipsinfile: 
					#if one not in resforeveryfile.keys():
					#	resforeveryfile[one] = 0;
					numberofdots = one.count('.')
					if (numberofdots!=3):
						error_ips.append(one)
						continue
					oneipcheckcommand = execute_commaand+str(one)
					print("SENDING THE COMMAND: ",oneipcheckcommand)
					checker = connection(oneipcheckcommand)
					if (checker=="Available"):
						available_ips.append(one)
						
					else:
						unavailable_ips.append(one)


			except Exception as e:
				print(e)
		print()
		print("THE FOLLOWING IPS ARE AVAILABLE: ")
		for one in available_ips:
			print(one)
			
		if(unavailableips==True):
			print("THE FOLLOWING IPS ARE UNAVAILABLE: ")
			for one in unavailable_ips:
				print(one)
		if (errorips==True):
			print("THE FOLLOWING IPS IN THE FILE HAVE ERRORS")
			for one in error_ips:
				print(one)
		
	else:
		print("The file ", filename, "was not found")

