#pragma once

#include <regex>
#include <vector>

using namespace std;

class Parser {
    private:
    static const regex re_literal;
    static const regex re_clause;
    public:
    static int parse_literal(string text);
    /** Extract a list of integers (including negative) from given string. */
    static vector<int> parse_literals(string text);
    /** Extract a list of strings, each encapsulated by parentheses. */
    static vector<string> parse_clauses(string text);
};