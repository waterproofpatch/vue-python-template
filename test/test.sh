#!/bin/bash

function check_error {
    if [ $result -ne 200 ]; then
        echo "Failed."
        exit 1
    fi
}

URL='${1}'
result=`curl -sL -w "%{http_code}" ${URL} -o /dev/null`
check_error $result

URL='${1}/api/items'
result=`curl -sL -w "%{http_code}" ${URL} -o /dev/null`
check_error $result