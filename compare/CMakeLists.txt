find_package(REQUIRED)
set(CMAKE_CXX_FLAGS "-march=native -maes -mrdseed -O3")
add_executable(solver solver.cpp)
target_link_libraries(solver Ppsat pthread emp-tool gmp ssl crypto)
