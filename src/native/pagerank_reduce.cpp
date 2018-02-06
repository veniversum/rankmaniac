//
// Created by Veniversum on 06/02/2018.
//

#include <cstdlib>
#include <iostream>
#include <map>
//#include <fstream>
#include "node.h"

using namespace std;

int main() {
//        ifstream in(
//            "C:\\Users\\Veniversum\\Documents\\a.School\\Caltech\\CS144\\rankmaniac\\src\\temp");
//    cin.rdbuf(in.rdbuf());
    ios_base::sync_with_stdio(false);
    map<string, Node> nodes;
    map<string, double> weights;
    string header;
    string content;
    while (cin >> header >> content) {
        if (header[0] == 'I') {
            // Info string, just pass it forward
            printf("%s\t%s\n", header.c_str(), content.c_str());
            continue;
        }
        if (content[0] == '+') {
            // First run, verbose input format
            weights[header] += stod(content);
        } else {
            nodes.emplace(header, Node(header, content, false));
        }
    }
    for (auto &node_pair : nodes) {
        node_pair.second.pageRank = weights[node_pair.first];
        node_pair.second.reemit();
    }

    return 0;
}