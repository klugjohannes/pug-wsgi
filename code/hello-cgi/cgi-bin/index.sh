#!/bin/env bash

NAME=`echo "$QUERY_STRING" | sed -n 's/^.*name=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

if [ -z "$NAME" ]; then
    export NAME="World"
fi

echo "########################################" 1>& 2
echo "##### err output for demo purposes #####" 1>& 2
echo "########################################" 1>& 2

echo Content-type: text/plain
echo ""
echo "Hello $NAME!"

echo ""
echo "environment variables"
echo "====================="
echo ""
/bin/env
