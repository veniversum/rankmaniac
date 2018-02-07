//
// Created by Veniversum on 05/02/2018.
//
#include <cstdlib>
#include <iostream>
#include <map>
#include "node.h"
#include <cmath>

#define NODEID_OFFSET 7
#define ALPHA 0.85
#define EPSILON 0.0001

using namespace std;

void emit_node_walk_line(const string &node_id, double weight) {
    printf("%s\t%+.10g\n", node_id.c_str(), weight);
}

int main() {
    map<string, double> weights;
    vector<Node> nodes;
    ios_base::sync_with_stdio(false);

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
        }

        nodes.emplace_back(header, content, true);
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
    do {
        local_delta = 0;
        //local collect
        for (auto &it:nodes) {
            const double w = weights[it.id];
            weights[it.id] = 0;
            it.pageRank = w + (1 - ALPHA);
            local_delta += std::abs(it.pageRank - it.oldPageRank);
        }
        //local map
        for (auto &it:nodes) {
            const double weightsAlongEdges = it.pageRank * ALPHA;
            it.oldPageRank = it.pageRank;
            it.pageRank = 0;

            if (it.outlinks_count > 0) {
                for (const string &neighbor:it.outlinks) {
                    weights[neighbor] += weightsAlongEdges / it.outlinks_count;
                }
            } else {
                weights[it.id] += weightsAlongEdges;

            }
        }
    } while (local_delta > EPSILON * nodes.size());

    for (auto &it:nodes) {
        it.reemit();
    }
    for (const auto &it:weights) {
        emit_node_walk_line(it.first, it.second);
    }

    return 0;
}