#!/bin/sh

#export ORACLE_BASE=/u01/app/oracle
#export ORACLE_HOME=$ORACLE_BASE/product/12.1.0.2/prd_home1
#export PATH=$PATH:$ORACLE_HOME/bin

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=/u01/app/oracle/product/12.1.0/client_1
export GG_HOME=/u01/app/oracle/product/12.1.2.1/npd_home1
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:$ORACLE_HOME:$LD_LIBRARY_PATH
mv $GG_HOME/dirprm/repppd.prm.DONOTSTART $GG_HOME/dirprm/repppd.prm

$GG_HOME/ggsci <<EOF
OBEY /home/oracle/ppd_refresh/startppd.oby
EOF
exit
