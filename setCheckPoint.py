#!/usr/local/bin/python3.6

from dbConn import orcl
import subprocess
import calendar
from datetime import datetime

with orcl() as db:
  def getRestPoint():
    monthNum = datetime.now().month
    monthAbbr = calendar.month_abbr[monthNum]
    dayNum = datetime.now().day
    dayNum = str(dayNum)
    restPntName = monthAbbr + dayNum
    print(restPntName)
    sql = 'CREATE RESTORE POINT ' + restPntName + ' GUARANTEE FLASHBACK DATABASE'
    db.dbExecuteCommand(sql)

  getRestPoint()
