#!/bin/sh
# redirect the first process to null
./runTests 1 12345 >/dev/null 2>/dev/null &
# display the second process
./runTests 2 12345

