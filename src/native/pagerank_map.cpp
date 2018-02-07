//
// Created by Veniversum on 05/02/2018.
//
#include <cstdlib>
#include <iostream>
#include <map>
#include "node.h"
#include <cmath>
#include <algorithm>
#include <set>
#include <fstream>
#include <unordered_set>


#define NODEID_OFFSET 7
#define ALPHA 0.85
#define EPSILON 0.0001
#define MAX_LOCAL_ITERS 25

using namespace std;

void emit_node_walk_line(const string &node_id, double weight) {
    printf("%s\t%+.10g\n", node_id.c_str(), weight);
}

// Global map step
int main() {
//        ifstream in(
//            "C:\\Users\\Veniversum\\Documents\\a.School\\Caltech\\CS144\\rankmaniac\\src\\data\\xaa");
//    cin.rdbuf(in.rdbuf());
    map<string, double> weights;
    vector<Node> nodes;
    unordered_set<std::string> neighborhood = {};
    ios_base::sync_with_stdio(false);
    bool first = false;


    string header;
    string content;
    while (cin >> header >> content) {
        if (header[0] == 'I') {
            // Info string, just pass it forward
//            cout << header << '\t' << content << '\n';
            printf("%s\t%s\n", header.c_str(), content.c_str());
            continue;
        }
        if (header[0] == 'N') {
            // First run, verbose input format
            header = header.substr(NODEID_OFFSET);
            first = true;
        }

        nodes.emplace_back(header, content, true);
        neighborhood.emplace(header);
        Node node = nodes.back();
        const double weightsAlongEdges = node.pageRank * ALPHA;
        node.oldPageRank = node.pageRank;
        node.pageRank = 0;

        if (node.outlinks_count > 0) {
            for (const string &neighbor:node.outlinks) {
//                emit_node_walk_line(neighbor,
//                                    weightsAlongEdges / node.outlinks_count);
                weights[neighbor] += weightsAlongEdges / node.outlinks_count;
            }
        } else {
            // Hold on to the PageRank
            weights[node.id] += weightsAlongEdges;
//            emit_node_walk_line(node.id, weightsAlongEdges);
//            node.pageRank = weightsAlongEdges;
        }
//        node.reemit();
    }

    // Do local iteration of subgraph/partition
    double local_delta = 0;
//    for (auto &it:nodes) {
//        for (const auto &outlink:it.outlinks) {
//            if (neighborhood.find(outlink) == neighborhood.end()) {
//                it.internal = false;
//                break;
//            }
//        }
//    }
    int cnt = 0;
    do {
        local_delta = 0;
        //local collect
        for (auto &it:nodes) {
            if (it.internal) {
                const double w = weights[it.id];
                weights[it.id] = 0;
                it.pageRank = w + (1 - ALPHA);
                local_delta += std::abs(it.pageRank - it.oldPageRank);
            }
        }
        //local map
        for (auto &it:nodes) {
            if (it.internal) {
                const double weightsAlongEdges = it.pageRank * ALPHA;
                it.oldPageRank = it.pageRank;
                it.pageRank = 0;

                if (it.outlinks_count > 0) {
                    for (const string &neighbor:it.outlinks) {
                        weights[neighbor] +=
                                weightsAlongEdges / it.outlinks_count;
                    }
                } else {
                    weights[it.id] += weightsAlongEdges;
                }
            }
        }
        cnt++;
    } while (local_delta > EPSILON * nodes.size() && cnt < MAX_LOCAL_ITERS);

    for (auto &it:nodes) {
        it.reemit();
    }
    for (const auto &it:weights) {
        emit_node_walk_line(it.first, it.second);
    }

    return 0;
}