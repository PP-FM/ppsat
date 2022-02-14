#!/bin/sh
# redirect the first process to null
./test_all 1 12345 >/dev/null 2>/dev/null &
# display the second process
./test 2 12345
