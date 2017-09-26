#!/bin/bash

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/12.1.0/client_1
export GG_HOME=/u01/app/oracle/product/12.1.2.1/npd_home1
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$ORACLE_HOME:$LD_LIBRARY_PATH
PATH=$PATH:$ORACLE_HOME/bin


export PATH

/home/oracle/ppd_refresh/refresh_ppd.py

cat /home/oracle/refresh.log >> /mnt/util/dpdir/refresh.log
mailx -r ppdrefresh@ucmail.uc.edu -s "PPD Refresh Results" </home/oracle/refresh.log psadmin@ucmail.uc.edu
rm /home/oracle/refresh.log
