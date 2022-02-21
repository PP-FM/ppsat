cmake_minimum_required(VERSION 3.10)

project(ppsat)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_FLAGS "-march=native -maes -mrdseed -O3")

include_directories(include)
include_directories(include ./emp-tool)
include_directories(include ./emp-sh2pc)
enable_testing()

add_subdirectory(src)
add_subdirectory(test)
add_subdirectory(Eval)

