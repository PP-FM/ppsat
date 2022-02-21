cmake_minimum_required(VERSION 3.10)

project(ppsat)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_FLAGS "-march=native -maes -mrdseed -O3")

include_directories(include)
find_package(emp-ot REQUIRED)
include_directories(${EMP-OT_INCLUDE_DIRS})
enable_testing()

add_subdirectory(src)
add_subdirectory(test)
add_subdirectory(Eval)
add_subdirectory(compare)


