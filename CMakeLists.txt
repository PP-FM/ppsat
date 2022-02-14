cmake_minimum_required(VERSION 3.10)

project(ppsat)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_FLAGS "-march=native -maes -mrdseed -O3")

include_directories(include)

enable_testing()

add_subdirectory(src)
#add_subdirectory(test)
add_subdirectory(Eval)


# unit
# add_executable(unit unit.cpp literal.cpp clause.cpp formula.cpp utils.cpp state.cpp heuristics.cpp solver.cpp)
# target_link_libraries(unit PUBLIC emp-tool gmp ssl crypto)

# GTest
add_test (NAME MyTest COMMAND runTests)
