#!/bin/bash

cat /var/log/developer_test.log | while read line;
do
        arr=(${line});
        if [ "${arr[0]}" == "[Error]" ]; then
                echo "${line}"
        fi
done