#!/bin/bash

err_code=-1

while [ $err_code -ne 0 ]; do
  python ts.py
  err_code=$?
  echo "faied with $err_code code"
  sleep 1
  killall firefox
  delay=$(( ( RANDOM % 100 )  + 1 ))
  echo "sleeping for $delay seconds"
done
