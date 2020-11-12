import ssl #inbuilt in python
import OpenSSL #pip install pyOpenSSL
import pathlib
#import xlsxwriter #pip install xlsxwriter
import datetime
import pandas as pd#pip install pandas
from openpyxl import Workbook,load_workbook,styles
import os
#pip install openpyxl xlsxwriter xlrd

def writeToExcel(nameOfMachines,today,lastBackUp,status,sheetName=str(datetime.datetime.date(datetime.datetime.now()))):
    df = pd.DataFrame({
    'Name of Machines':nameOfMachines,
    'Today Date':today,
    'Last Backup Date':lastBackUp,
    'Longer Than 2 weeks':status,
    })

    #df.style.apply(highlight_diff,axis=None).to_excel('SSLs.xlsx', engine='openpyxl', index=False)
    try:
        with pd.ExcelWriter(path + 'AuditReport.xlsx', engine="openpyxl",  mode='a') as writer:
            df.style.apply(highlight_diff,axis=None).to_excel(writer, sheet_name=sheetName, index=False)
            #writer.sheets['Summary'].column_dimensions['A'].width = 15
    except Exception as e:
        print("error")


def highlight_diff(x):
    c1 = 'background-color: red'
    c2 = ''
    m = x['Longer Than 2 weeks'] != 'No'
    df1 = pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[m, :] = c1
    return df1

def getBackup(myString):
    nameOfMachinesList.append(myString)
    todayTime = datetime.datetime.now()
    todayDateList.append(datetime.datetime.date(todayTime))
    todayMinustwoWeeks = datetime.datetime.date(todayTime) - datetime.timedelta(weeks=2)
    lastBackUpDate = ""
    longerThan = ""
    try:
        lastBackUpDate = datetime.datetime.strptime(((os.path.splitext(myString)[0])[-8:]), '%Y%m%d').date()
        #print(lastBackUpDate)
        if (todayMinustwoWeeks < lastBackUpDate):
            longerThan ="No"
        else:
            longerThan="Yes"
    except:
        lastBackUpDate = "Format Error"
        longerThan = "Format Error"

    longerThan2weeks.append(longerThan)
    lastBackUpDateList.append(lastBackUpDate)



nameOfMachinesList = []
lastBackUpDateList = []
todayDateList = []
longerThan2weeks = []



#for root, dirs, files in os.walk("."):
#    for filename in files:
#        if(filename in "Harsha.py"):
#            print("escape python file")
#        else:
#            getBackup(filename)

# /usr/local/linkbynet/scripts/Audit_Reseau/CR
#writeToExcel(nameOfMachinesList,todayDateList,lastBackUpDateList,longerThan2weeks)
path = '/usr/local/linkbynet/scripts/Audit_Reseau/'

# Using readlines()
file1 = open(path + 'CR', 'r')

Lines = file1.readlines()
del Lines[0]
del Lines[0]
del Lines[-1]
# Strips the newline character
for line in Lines:
    mystr = line.strip().replace('<br><b>Backup CKP</b><br><br>', '').replace('<br><b>Backup BIGIP</b><br><br>', '').replace('<br>', '').strip()
    #print(mystr)
    getBackup(mystr)

writeToExcel(nameOfMachinesList,todayDateList,lastBackUpDateList,longerThan2weeks)

#os.system("/bin/bash /usr/local/linkbynet/scripts/Audit_Reseau/sendmail.sh")
