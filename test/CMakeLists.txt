find_package(GTest REQUIRED)

include_directories(${GTEST_INCLUDE_DIRS})
add_executable(runTests test_all.cpp test_bi_literal.cpp test_bi_clause.cpp test_formula.cpp test_model.cpp test_state.cpp test_solver.cpp)
target_link_libraries(runTests Ppsat ${GTEST_LIBRARIES} pthread emp-tool gmp ssl crypto)
