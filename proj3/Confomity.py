
import json
import getpass
import os
import pathlib
import subprocess
import platform
import requests# pip install requests
import pandas as pd  # pip install pandas

# fc = open("Credentials.txt", "r")
# lines = fc.readlines()
# login = lines[0].replace("login = ", "").replace("'", "").strip()
# password = lines[1].replace("password = ", "").replace("'", "").strip()
# fc.close()
def welcome():
  print("___________________welcome " + getpass.getuser() + "___________________")
def installPackages():
  print("installing required packages")
  os.system("pip install requests > dev/null")
  os.system("pip install pandas > dev/null")
  os.system("pip install xlsxwriter > dev/null")
  os.system("pip install xlrd > dev/null")
def logging(login=getpass.getuser()):
  print("___________________login with your credentials___________________")
  password = getpass.getpass(prompt=login + ' password: ') 
  #s = requests.Session()
  credentials = {'login': login, 'password': password}
  loggedIn = requests.Session().post("https://intranet.linkbynet.com/v7/api/1.1/Authentification.json/LogIn", credentials)
  return loggedIn
def populateLists():
  print("opening file 'Equipment_ID_Or_Name_list.txt'")
  fe = open("Equipment_ID_Or_Name_list.txt", "r")
  Lines = fe.readlines()
  for line in Lines:
    equipmentIDOrName = str(line.strip())
    #loggedIn =
    #requests.Session().post("https://intranet.linkbynet.com/v7/api/1.1/Authentification.json/LogIn",
    #credentials)
    reqID = requests.Session().get("https://intranet.linkbynet.com/v7/api/1.1/Equipment.json/Search?Query=" + equipmentIDOrName)
    equipmentID = ''
    Name = ''
    TeamInCharge = ''
    HostType = ''
    if reqID.ok:
      jsonQueryDictionary = json.loads(json.dumps(reqID).json())[0]
      equipmentID = jsonQueryDictionary['Id']
      reqData = requests.Session().get("https://intranet.linkbynet.com/v7/api/1.1/Equipment.json/" + str(equipmentID) + "/General/Technical")
      if reqData.ok:      
        jsonTechnicalData = json.dumps(reqData.json())
        jsonTech = json.loads(jsonTechnicalData)
        # print(jsonTech)
        Name = jsonTech['Name']
        TeamInCharge = jsonTech['TeamInCharge']
        HostType = jsonTech['HostType']        
      else:
        Name = "fail to get data"
        TeamInCharge = "fail to get data"
        HostType = "fail to get data"
    else:
      equipmentID = "fail to get ID"
      Name = "fail to get ID"
      TeamInCharge = "fail to get ID"
      HostType = "fail to get ID"

    IDList.append(equipmentID)
    NameList.append(Name)
    HostTypeList.append(HostType)
    TeamInChargeList.append(TeamInCharge)
    # print(equipmentID)
    #print(TeamInCharge)
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
    #os.system("start Equipment_ID_Or_Name_list.txt")
def writeToExcel(ticketNumber,IDList, NameList, HostTypeList, TeamInChargeList):
  print("Writing data to excel")
  df = pd.DataFrame({
    "IDs of Machines": IDList,
    "Names of Machines": NameList,
    "Host Type": HostTypeList,
    "Team In Charge": TeamInChargeList,
  })
  writer = pd.ExcelWriter(str('conformity_followup_' + ticketNumber + '.xlsx'), engine='xlsxwriter')# pylint: disable=abstract-class-instantiated
  df.to_excel(writer, sheet_name=str('conformity_followup_' + ticketNumber), index=False)
  writer.save()
  openFile(str('conformity_followup_' + ticketNumber + '.xlsx'))
  # with pd.ExcelWriter(path + destFile, engine="openpyxl", mode="a") as
  # writer:
  #   # writer.sheets['Summary'].column_dimensions['A'].width = 15 #try to set
  #   width to all columns
  #   df.style.apply(highlight_diff, axis=None).to_excel(writer,
  #   sheet_name=sheetName, index=False) # filling the excel sheet
def getTicketNumber():
  ticketNumber = 0
  while True:
    try:
      ticketNumber = int(input('Ticket Number: '))      
      break
    except SyntaxError:
      ticketNumber = 0
      print("That wasn't a number!")
  return ticketNumber



##########################################
IDList = []
NameList = []
HostTypeList = []
TeamInChargeList = []
os.system('cls' if os.name == 'nt' else 'clear')
welcome()
os.system('cls' if os.name == 'nt' else 'clear')
installPackages()
while True:
  if logging().ok :
    os.system('cls' if os.name == 'nt' else 'clear')
    readFile("Equipment_ID_Or_Name_list.txt")
    break
  else :
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Wrong Credentials")
    #logging()
os.system('cls' if os.name == 'nt' else 'clear')
ticketNum = getTicketNumber()
os.system('cls' if os.name == 'nt' else 'clear')
writeToExcel(ticketNum, IDList, NameList, HostTypeList, TeamInChargeList)
print("\n\nIf you are using this program you owe Arouven POOLIAN a lunch!")