#!/bin/bash
sudo route add -host 192.168.1.6 eth0
./check_update.py $1
tftp 192.168.1.6 <<EOF
binary
rexmt 1
timeout 180
trace
status
put $1
EOF
