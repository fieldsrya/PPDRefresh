#!/usr/local/bin/python3.6

from dbConn import orcl
import subprocess


with orcl() as db:
  def getRestPoint():
    sql = 'SELECT NAME FROM V$RESTORE_POINT'
    data = db.dbExecuteFetchOne(sql)
    restorePointName = (data[0])

    return restorePointName
