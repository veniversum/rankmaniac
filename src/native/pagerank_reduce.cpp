//
// Created by Veniversum on 06/02/2018.
//

#include <cstdlib>
#include <iostream>
#include <map>
#include <unordered_set>
#include <cmath>
#include <fstream>
#include "node.h"

using namespace std;
#define EPSILON 0.0001
#define ALPHA 0.85
#define PATIENCE 30


double iter_block(map<uint32_t, Node> &nodes,
                  map<uint32_t, unordered_set<uint32_t>> block_incomings,
                  map<uint32_t, double> weights) {
    double resid = 0;
    for (auto &it : nodes) {
        double newPR = 0;
        uint32_t id = it.first;
        if (block_incomings.find(id) != block_incomings.end()) {
            for (uint32_t from_id : block_incomings[id]) {
                newPR += (*nodes.find(from_id)).second.outgoingPR();
            }
        }
        newPR += weights[id];
        newPR = ALPHA * newPR + (1 - ALPHA);
        resid += abs(it.second.pageRank - newPR) / newPR;
        it.second.pageRank = newPR;
    }
    return resid / nodes.size();
}

int main() {
//        ifstream in(
//            "C:\\Users\\Veniversum\\Documents\\a.School\\Caltech\\CS144\\rankmaniac\\src\\data\\1_aft_pagerank_map.txt");
//    cin.rdbuf(in.rdbuf());
    ios_base::sync_with_stdio(false);
    map<uint8_t, map<uint32_t, unordered_set<uint32_t>>> block_incomings;
    map<uint8_t, map<uint32_t, Node>> nodes;
    map<uint8_t, map<uint32_t, double>> weights;
    string header;
    string content;
    while (cin >> header >> content) {
        uint8_t block_id;
        if (header[0] == 'I') {
            // Info string, just pass it forward
            printf("%s\t%s\n", header.c_str(), content.c_str());
            continue;
        } else {
            block_id = static_cast<uint8_t>(stoul(header));
        }
        if (content[0] == 'N') {
            // Node
            string id_str, inner_content;
            cin >> id_str >> inner_content;
            uint32_t id = stoul(id_str);
            nodes[block_id].emplace(id, Node(id, inner_content, true));
        } else if (content[0] == 'S') {
            // Same block
            string from_id, to_id;
            cin >> from_id >> to_id;
            block_incomings[block_id][stoul(to_id)].insert(stoul((from_id)));
        } else if (content[0] == 'O') {
            string from_id, to_id, weight;
            cin >> from_id >> to_id >> weight;
            weights[block_id][stoul(to_id)] += stod(weight);
        }
    }
    for (auto &it : nodes) {
        uint8_t cur_iter = 0;
        double resid = 0;
        uint8_t block_id = it.first;
        do {
            resid = iter_block(it.second, block_incomings[block_id],
                               weights[block_id]);
            cur_iter++;
        } while (cur_iter < PATIENCE && resid > EPSILON);
        for (auto node:it.second) {
            node.second.reemit();
        }
    }
//    for (auto &node_pair : nodes) {
//        node_pair.second.pageRank += weights[node_pair.first];
//        node_pair.second.reemit();
//    }

    return 0;
}
