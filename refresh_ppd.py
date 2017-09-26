#!/usr/local/bin/python3.6
from time import sleep
import subprocess
import flashback
import calendar
import os
from datetime import datetime

fLog = "refresh.log"
fName = "/home/oracle/ppd_refresh/ggoutput.log"
lagScriptName = "/home/oracle/ppd_refresh/test_ggsci.sh"
startScriptName = "/home/oracle/ppd_refresh/start_repppd.sh"
stopScriptName = "/home/oracle/ppd_refresh/stop_repppd.sh"
flashbackScript = "/home/oracle/ppd_refresh/flashback_ppd.sh"
setRestorePointScript = "/home/oracle/ppd_refresh/setRestPnt.sh"
fFinished = "/mnt/psnfs/refresh/csdone"
paramDir = "/u01/app/oracle/product/12.1.2.1/npd_home1/dirprm/"
replParam = "repppd.prm"
replParamDone = "repppd.prm.DONOTSTART"

def writeLogLine(line):
  log = open(fLog, "a")
  log.write(line)
  log.close()

def stopDatabase(parm1):
  writeLogLine('Stopping database and flashing back to ' + parm1 + '\n')
  f = open(fLog, "w")
  subprocess.run([flashbackScript,parm1], stdout = f)
  f.write('\n')
  f.close()

# Function to check for lag in the output file
def checkLag():
  f = open(fName, "r")

  for line in f:
    if "Last record lag" in line:
      lagLine = line.split(" ")
      lagSec = lagLine[3]
      lagSec = lagSec.replace(",","")
      writeLogLine('Current Lag is ' + lagSec + '\n')
      lagSec = int(lagSec)
      f.close()
      if lagSec > 600:
        return 0
      else:
        return 1
    elif "ERROR: sending message" in line:
      f.close()
      return 0 

def getLag():
  f = open(fName, "w")
  subprocess.run(lagScriptName,stdout = f)
  f.close()


def startReplicat():
  f = open(fLog, "a")
  subprocess.run(startScriptName,stdout = f)
  f.close()

def checkStopped():
    f = open(fName, "w")
    subprocess.run(stopScriptName,stdout = f)
    f.close()
    sleep(120)

    f = open(fName, "r")
    errCount = 0
    for line in f:
      if "ERROR" in line:
        errCount = errCount + 1
    f.close()
    if errCount > 0:
      return 0
    else:
      return 1

def stopReplicat():
  writeLogLine('Stopping Replicat and creating checkpoint\n')

  stopped = 0
  while stopped !=1: 
    sleep(60)
    stopped = checkStopped()

  os.rename(paramDir + replParam,paramDir + replParamDone)

def setNewCheckPoint(restorePoint):
  f = open(fLog, "a")
  monthNum = datetime.now().month
  monthAbbr = calendar.month_abbr[monthNum]
  hourNum = datetime.now().hour
  hourNum = str(hourNum)
  minNum = datetime.now().minute
  minNum = str(minNum)
  dayNum = datetime.now().day
  dayNum = str(dayNum)
  restPntName = monthAbbr + dayNum + hourNum + minNum
  writeLogLine('Droping Old Restore Point and Creating New')
  writeLogLine(restPntName)
  subprocess.run([setRestorePointScript,restPntName,restorePoint],stdout = f)
  f.close()

def writeFinishedFile():
  ff = open(fFinished, "w")
  ff.write('done\n')
  ff.close()

def main():
  writeLogLine('Starting PPD refresh at ' + str(datetime.now()) + ' ...\n')
  restorePoint = flashback.getRestPoint()
  writeLogLine('INFO('+ str(datetime.now())  +'): Flashing back to ' + restorePoint + '...\n')
  stopDatabase(restorePoint)
  startReplicat()
  sleep(300)
  isFinished = 0
  while isFinished != 1:
    getLag()
    sleep(300)
    isFinished = checkLag()
    if isFinished == 0:
      writeLogLine("Still Waiting!!\n")
    elif isFinished ==1:
      writeLogLine("Go Ahead!\n")
    else:
      writeLogLine("SCRIPT ERROR -- HALTING!!\n")
      exit(1)
  stopReplicat()
  setNewCheckPoint(restorePoint)
  writeFinishedFile()
  writeLogLine('Refresh Completed at ' + str(datetime.now()) + '!!\n')

main()
