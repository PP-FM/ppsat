# CMake generated Testfile for 
# Source directory: /home/nl437/code/ppsat
# Build directory: /home/nl437/code/ppsat
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(MyTest "runTests")
set_tests_properties(MyTest PROPERTIES  _BACKTRACE_TRIPLES "/home/nl437/code/ppsat/CMakeLists.txt;24;add_test;/home/nl437/code/ppsat/CMakeLists.txt;0;")
subdirs("src")
subdirs("Eval")
