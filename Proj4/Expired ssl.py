
import ssl #inbuilt in python
import OpenSSL #pip install pyOpenSSL
import pathlib
import xlsxwriter #pip install xlsxwriter
from datetime import datetime
from datetime import timedelta
import pandas as pd#pip install pandas
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl import load_workbook,styles
#pip install openpyxl xlsxwriter xlrd

def writeToExcel(ssl,today,expiry,status,sheetName=str(datetime.date(datetime.now()))):
    df = pd.DataFrame({
    'SSL':ssl,    
    'Today Date':today,
    'Expiry Date':expiry,
    'Status':status,
    })

    #df.style.apply(highlight_diff,axis=None).to_excel('SSLs.xlsx', engine='openpyxl', index=False)
  
    with pd.ExcelWriter('./Proj2/SSLs.xlsx', engine="openpyxl",  mode='a') as writer:
        df.style.apply(highlight_diff,axis=None).to_excel(writer, sheet_name=sheetName, index=False)#add to existing excel file new sheet with highlight

def highlight_diff(x): #defining what format to use for the condition col 'Status' contain the word 'valid'
    c1 = 'background-color: red'
    c2 = '' 
    m = x['Status'] != 'valid'
    df1 = pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[m, :] = c1
    return df1 

def get_SSL_Expiry_Date(host, port=443):
    cert = ssl.get_server_certificate((host, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)# x.509 protocol -- standard format of public key certificates
    todayTime = datetime.now()
    expireTime = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
    myHostList.append(host)
    myTimeList.append(datetime.date(expireTime))
    myTodayList.append(datetime.date(todayTime))
    expOrNot = ""
    if (expireTime > todayTime):
        expOrNot="valid"
    elif (expireTime <= todayTime):
        expOrNot="expired"
    else:
        expOrNot="Error"
    myExpiredOrNotList.append(expOrNot)


myHostList = []
myTimeList = []
myTodayList = []
myExpiredOrNotList = []
get_SSL_Expiry_Date("google.com")#for each
get_SSL_Expiry_Date("google.com")
writeToExcel(myHostList,myTodayList,myTimeList,myExpiredOrNotList)

