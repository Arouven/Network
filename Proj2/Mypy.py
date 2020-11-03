
import ssl #inbuilt in python
import OpenSSL #pip install pyOpenSSL
import pathlib
import xlsxwriter #pip install xlsxwriter
from datetime import datetime
from datetime import timedelta
import pandas as pd#pip install pandas
#pip install openpyxl xlsxwriter xlrd

def writeToExcel(ssl,expiry,sheetName=str(datetime.date(datetime.now()))):
    df = pd.DataFrame({
    'SSL':ssl,
    'Expiry Date':expiry
    })
   # df.to_excel('./SSLs.xlsx', sheet_name=sheetName, index=False)
    number_rows = len(df.index) + 1
    writer = pd.ExcelWriter('./SSLs.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheetName, index=False)
    workbook  = writer.book
    worksheet = writer.sheets[sheetName]
    format1 = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    worksheet.conditional_format("$A$1:$B$%d" % (number_rows),
                             {"type": "formula",
                              "criteria": '=INDIRECT("B"&ROW())="SUCCESS"',
                              "format": format1
                             })
    workbook.close()

def readExcel(sheetName=str(datetime.date(datetime.now()))):
    x = pd.read_excel('./SSLs.xlsx', sheet_names=sheetName)
    x.head()
        #if (expireTime > todayTime):
    #    print("valid until", expireTime - todayTime)        
    #elif (expireTime <= todayTime):
    #    print("expired by", todayTime - expireTime)


    #elif ((expireTime - timedelta(weeks=1)) < todayTime):
    #    print("Will expire in less than 1 week")

def get_SSL_Expiry_Date(host, port=443):
    cert = ssl.get_server_certificate((host, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)# x.509 protocol -- standard format of public key certificates
    todayTime = datetime.now()
    expireTime = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
    myHostList.append(host)
    myTimeList.append(expireTime)
    # writeToExcel(str(datetime.date(todayTime)))



myHostList = []
myTimeList = []


get_SSL_Expiry_Date("google.com")#for each
get_SSL_Expiry_Date("google.com")
writeToExcel(myHostList,myTimeList)
#readExcel()
