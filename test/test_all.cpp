#include "gtest/gtest.h"
#include "emp-sh2pc/emp-sh2pc.h"
#include "parser.hpp"
#include <vector>
#include <memory>

TEST(PARSER, parse_literal)
{
    int res1 = Parser::parse_literal("42");
    int res2 = Parser::parse_literal("-1");
    EXPECT_EQ(res1, 42);
    EXPECT_EQ(res2, -1);
}

TEST(PARSER, parse_literals)
{
    vector<int> res = Parser::parse_literals("42 \\/ -1 100, -9");
    vector<int> expected{42, -1, 100, -9};
    EXPECT_EQ(res, expected);
}

// TEST(CLAUSE, toString)
// {
//     int nvar = 10;
//     int ncls = 4;
//     unique_ptr<bi_clause> c = make_unique<bi_clause>(nvar);
//     vector<int> plist{1,2};
//     vector<int> nlist{5,6};
//     c->set(plist, nlist, PUBLIC);
//     EXPECT_EQ(c->toString(), "(1 \\/ 2 \\/ -5 \\/ -6)");
// }

int main(int argc, char **argv)
{
    int port, party;
    party = atoi(argv[1]);
	port = atoi(argv[2]);
    NetIO * io = new NetIO(party==ALICE ? nullptr : "127.0.0.1", port);
    setup_semi_honest(io, party);
    testing::InitGoogleTest(&argc, argv);
    testing::GTEST_FLAG(filter) = "UnitSearch_Evaluation";
    int res = RUN_ALL_TESTS();
    cout << CircuitExecution::circ_exec->num_and()<<endl;

    delete io;

    return res;
}