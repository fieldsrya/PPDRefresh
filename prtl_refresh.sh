#!/bin/bash

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/12.1.0/client_1
export GG_HOME=/u01/app/oracle/product/12.1.2.1/npd_home1
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$ORACLE_HOME:$LD_LIBRARY_PATH
PATH=$PATH:$ORACLE_HOME/bin


export PATH

## Set your variables here
SOURCE_DB=PP91HCA2
SOURCE_LOGIN="system/KuwQ_wIGYs"
DEST_DB=PP91PPD2
DEST_LOGIN="system/DcEDrAIrpP"
PUMP_DIR=NFSDIR
DUMPFILE=pp91hca2_ppd_%u.dmp
SCHEMAS=SYSADM
PARALLEL_PROCS=4
TBL_EX_ACT=REPLACE

## Shouldn't have to edit beyond here!!! ##
# get environment
#source /home/oracle/.bash_profile
rm -f /mnt/util/dpdir/pp91hca2_ppd_*.dmp

echo "Exporting database"

expdp $SOURCE_LOGIN@$SOURCE_DB DIRECTORY=$PUMP_DIR DUMPFILE=$DUMPFILE PARALLEL=$PARALLEL_PROCS SCHEMAS=$SCHEMAS

echo "INFO: database is $ODB_IMP, ORACLE_SID is $ORACLE_SID"

echo "INFO: Importing Schema"

impdp $DEST_LOGIN@$DEST_DB DIRECTORY=$PUMP_DIR DUMPFILE=$DUMPFILE PARALLEL=$PARALLEL_PROCS TABLE_EXISTS_ACTION=$TBL_EX_ACT

echo "INFO: Restarting database"

ssh odbmgmt1 -t "/home/oracle/remote_exec_restart_db.sh"

echo "INFO: Touching the done file"

touch /mnt/psnfs/refresh/ihdone

ls -l /mnt/psnfs/refresh/ihdone

echo "INFO: Done."
