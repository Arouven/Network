########## importing libraries ##########
import os
import shutil
import pathlib
import datetime
import pandas as pd  # pip install pandas
# pip install openpyxl xlsxwriter xlrd
from openpyxl import Workbook, load_workbook, styles





########## writing the methods/functions ##########
def writeToExcel(nameOfMachines, today, lastBackUp, status, sheetName=str(datetime.datetime.date(datetime.datetime.now()))):
    df = pd.DataFrame({
        # header = "Name of Machines", records = nameOfMachines(from list)
        "Name of Machines": nameOfMachines,
        # header = "Today's Date", records = today(from list)
        "Today's Date": today,
        # header = "Last Backup Date", records = lastBackUp(from list)
        "Last Backup Date": lastBackUp,
        # header = "Longer Than 2 weeks", records = status(from list)
        "Longer Than 2 weeks": status,
    })
    with pd.ExcelWriter(path + destFile, engine="openpyxl", mode="a") as writer:
        # writer.sheets['Summary'].column_dimensions['A'].width = 15 #try to set width to all columns
        df.style.apply(highlight_diff, axis=None).to_excel(writer, sheet_name=sheetName, index=False)  # filling the excel sheet

def highlight_diff(x):  # will read column "Longer Than 2 weeks" in the excel, highlight all rows that != "No"(e.i.Yes and Format Error)
    c1 = "background-color: red"
    c2 = ""
    m = x["Longer Than 2 weeks"] != "No"
    df1 = pd.DataFrame(c2, index=x.index, columns=x.columns)
    df1.loc[m, :] = c1
    return df1

def getBackup(myString):
    nameOfMachinesList.append(myString)
    todayTime = datetime.datetime.now()  # get today's date and time
    todayDateList.append(datetime.datetime.date(todayTime))  # add the date only to the list
    todayMinustwoWeeks = datetime.datetime.date(todayTime) - datetime.timedelta(weeks=2)  # remove 2 weeks from today's date
    lastBackUpDate = ""
    longerThan = ""
    try:
        lastBackUpDate = datetime.datetime.strptime(((os.path.splitext(myString)[0])[-8:]), "%Y%m%d").date()  # retrive last 8 characters and convert them to date
        if todayMinustwoWeeks < lastBackUpDate:  # if not longer than 2 weeks
            longerThan = "No"
        else:
            longerThan = "Yes"
    except:
        lastBackUpDate = "Format Error"
        longerThan = "Format Error"
    longerThan2weeks.append(longerThan)  # add the resulted string to the list
    # add the resulted string to the list
    lastBackUpDateList.append(lastBackUpDate)





########## main task running ##########
# start try except
try:
    # vars declaration/and initialisation
    nameOfMachinesList = []
    lastBackUpDateList = []
    todayDateList = []
    longerThan2weeks = []    
    path = "/usr/local/linkbynet/scripts/Audit_Reseau/"
    sourceFile = "AuditReport.xlsx.bak"
    destFile = "AuditReport.xlsx"
    htmlFile = "CR"
    
    shutil.copy(os.path.join(path, sourceFile), os.path.join(path, destFile)) # overwrite the old excel file to new one(keeping instructions and example)
    file1 = open(path + htmlFile, "r")  # opens the file in read mode
    Lines = file1.readlines()  # read all lines in file1

    # remove first 2 lines and last line
    del Lines[0]
    del Lines[0]
    del Lines[-1]

    # start for loop
    for line in Lines:
        # Strips the newline character
        # remove <br><b>Backup CKP</b><br><br>
        # remove <br><b>Backup BIGIP</b><br><br>
        # remove all remaining <br>
        mystr = (line.strip()
                 .replace("<br><b>Backup CKP</b><br><br>", "")
                 .replace("<br><b>Backup BIGIP</b><br><br>", "")
                 .replace("<br>", "")
                 .strip())
        getBackup(mystr) # call method/function
    # end for loop
    writeToExcel(nameOfMachinesList, todayDateList, lastBackUpDateList, longerThan2weeks) # call method/function
except Exception as e:
    print('<br><div style="position:absolute;width:330px;height:50px;top:50%;left:50%;transform:translate(-50%, -50%);"><h1 style="color:red;font-weight:bold;">ERROR in Highlight.py</h1></div><br><br>')
# end try except
