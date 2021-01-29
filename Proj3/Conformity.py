
import json
import getpass
import os
import pathlib
import subprocess
import platform
import requests# pip install requests
import pandas as pd  # pip install pandas


def welcome():
  print("___________________welcome " + getpass.getuser() + "___________________")
def installPackages():
  print("installing required packages")
  os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
  os.system("python get-pip.py")
  os.system("pip install requests")
  os.system("pip install pandas")
  os.system("pip install xlsxwriter")
  os.system("pip install xlrd")
def populateLists():
  print("opening file 'Equipment_ID_Or_Name_list.txt'")
  print("please wait...")




  fe = open("Equipment_ID_Or_Name_list.txt", "r")
  Lines = fe.readlines()
  for line in Lines:    
    equipmentIDOrName = str(line.strip())
    reqQuery = s.get("https://intranet.linkbynet.com/v7/api/1.1/Equipment.json/Search?Query=" + equipmentIDOrName)
    # "Id"
    # "Name"
    # "OutSourcingLevelName"
    # "Type"
    # "Company_Name"
    # "Ips"
    # "Projects"
    # "ProjectList"
    # "HostType"
    # "IsVirtualized"
    # "IsDisabled"
    # "CIType"
    # "OSType"
    # "OSVersion"
    # "Room"
    # "Bay"
    # "DNSBackup1"
    # "DNSBackup2"
    # "VCenterName"
    # "Company_Id"    
    equipmentID = ''
    Name = ''
    TeamInCharge = ''
    HostType = ''
    SerialNumber=''
    if reqQuery.ok:
      jsonQueryAPI = json.loads(json.dumps(reqQuery.json()[0]))
      equipmentID = jsonQueryAPI['Id']
      Name = jsonQueryAPI['Name']
      HostType = jsonQueryAPI['HostType']  
      reqTechnical = s.get("https://intranet.linkbynet.com/v7/api/1.1/Equipment.json/" + str(equipmentID) + "/General/Technical")
      # "Type"
      # "relationType"
      # "CIClass"
      # "CINumber"
      # "Parent_Name"
      # "ParentEquipments"
      # "HostedEquipments"
      # "VCenterName"
      # "Cluster_Name"
      # "VIPServer"
      # "WebClient_Url"
      # "Parent_Id"
      # "Environment"
      # "EnvironmentFunction"
      # "BackupFunction"
      # "MonitoringFunction"
      # "PrimaireOrSecondaire"
      # "PrimaryServer_Name"
      # "PrimaryServer_Id"
      # "comment"
      # "TeamInCharge"
      # "Firmware_Name"
      # "id_cloud"
      if reqTechnical.ok:      
        jsonTechAPI = reqTechnical.json() 
        TeamInCharge = jsonTechAPI['TeamInCharge']             
      else:
        TeamInCharge = "fail to get data"
      reqSupport = s.get("https://intranet.linkbynet.com/v7/api/1.1/Equipment.json/" + str(equipmentID) + "/General/Support")
      # "ManufacturerName"
      # "ProductName"
      # "Model"
      # "Id"
      # "Mid"
      # "SerialNumber"
      # "ProductNumber"
      # "SupportContractNumber"
      # "CustomerServicePhone"
      # "UserFullName"
      # "IsInStock"
      # "StorageDate"
      # "MessageStorageSuppression"
      # "IsDisabled"
      # "IsBlacklisted"
      # "ArchiveDate"
      # "MessageSuppression"
      if reqSupport.ok:      
        jsonSupportAPI = reqSupport.json() 
        SerialNumber = jsonSupportAPI['SerialNumber']             
      else:
        SerialNumber = "fail to get data"
    else:
      equipmentID = "fail to get ID"
      Name = "fail to get ID"
      HostType = "fail to get ID"
    IDList.append(equipmentID)
    NameList.append(Name)
    HostTypeList.append(HostType)
    TeamInChargeList.append(TeamInCharge)
    SerialNumberList.append(SerialNumber)
  fe.close()
def readFile(filepath):
  if (pathlib.Path(filepath).exists()) and (os.stat(filepath).st_size > 0):
    populateLists()
  else:    
    open(filepath, "w")
    print("insert equipment ids or names in the opened text file")
    openFile(filepath)
    input('press enter when finished inserting and saving')
    readFile(filepath)
def openFile(filepath):
  print("opening file")
  if platform.system() == 'Darwin':       # macOS
    subprocess.call(('open', filepath))
  elif platform.system() == 'Windows':    # Windows
    os.startfile(filepath)
  else:                                   # linux variants
    subprocess.call(('xdg-open', filepath))
def writeToExcel(ticketNumber,IDList, NameList, HostTypeList, TeamInChargeList,SerialNumberList):
  print("Writing data to excel")
  df = pd.DataFrame({
    "IDs of Machines": IDList,
    "Names of Machines": NameList,
    "Host Type": HostTypeList,
    "Team In Charge": TeamInChargeList,
    "Serial Number": SerialNumberList,
  })
  writer = pd.ExcelWriter('conformity_followup_' + ticketNumber + '.xlsx', engine='xlsxwriter')# pylint: disable=abstract-class-instantiated
  df.to_excel(writer, sheet_name='conformity_followup_' + ticketNumber, index=False)
  writer.save()
  openFile(str('conformity_followup_' + ticketNumber + '.xlsx'))

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 


##########################################
# for lis in jsn_list:
#     for key,val in lis.items():
#         print(key, val)
s =requests.Session()
IDList = []
NameList = []
HostTypeList = []
TeamInChargeList = []
SerialNumberList =[]
os.system('cls' if os.name == 'nt' else 'clear')
welcome()
installPackages()
print("installing packages completed")
login=getpass.getuser()
print("___________________login with your credentials___________________")
password = getpass.getpass(prompt=login + ' password: ') 
credentials = {'login': login, 'password': password}
loggedIn = s.post("https://intranet.linkbynet.com/v7/api/1.1/Authentification.json/LogIn", credentials)
if loggedIn.ok:
  print("your are logged in")
  readFile("Equipment_ID_Or_Name_list.txt")
else :
  os.system('cls' if os.name == 'nt' else 'clear')
  print("Wrong Credentials")
  input("press enter to exit")
  exit(0)
os.system('cls' if os.name == 'nt' else 'clear')
ticketNum = str(inputNumber('Ticket Number: '))
os.system('cls' if os.name == 'nt' else 'clear')
writeToExcel(ticketNum, IDList, NameList, HostTypeList, TeamInChargeList,SerialNumberList)
print("\n\nIf you are using this program you owe Arouven POOLIAN a lunch!")
input("press enter to exit ...")
exit(0)