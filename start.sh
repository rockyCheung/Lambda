#!/bin/bash
DEPLOY_DIR=`pwd`
STDOUT_FILE="cobra.log"
nohup python main.py > $STDOUT_FILE 2>&1 &
echo "OK!"
PIDS=`ps -f | grep python | grep "$DEPLOY_DIR" | awk '{print $2}'`
echo "PID: $PIDS"
echo "STDOUT: $STDOUT_FILE"