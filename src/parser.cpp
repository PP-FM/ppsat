#include "parser.hpp"

/******************************************************************************
 *  parser
 *****************************************************************************/

const regex Parser::re_literal = regex("-?[0-9]+");
const regex Parser::re_clause ("\\([^\\(\\)]+\\)");

int Parser::parse_literal(string text) {
    std::smatch sm;
    bool found = regex_match(text, sm, re_literal);
    if (!found) throw "No matching literal found in " + text;

    return stoi(sm[0].str());
}

vector<int> Parser::parse_literals(string text) {
    vector<int> res;

    std::smatch sm;
    while (regex_search(text, sm, Parser::re_literal)) {
        for (auto x : sm) {
            res.push_back(stoi(x.str()));
        }
        text = sm.suffix().str();
    }
    return res;
}

vector<string> Parser::parse_clauses(string text) {
    vector<string> res;

    std::smatch sm;
    while (regex_search(text, sm, Parser::re_clause)) {
        for (auto x : sm) {
            res.push_back(x.str());
        }
        text = sm.suffix().str();
    }
    return res;
}
