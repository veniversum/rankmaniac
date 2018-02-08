//
// Created by Veniversum on 05/02/2018.
//
#include <cstdlib>
#include <iostream>
#include "node.h"

#define NODEID_OFFSET 7
#define ALPHA 0.85
#define EPSILON 0.00001

using namespace std;

void emit_node_walk_line(const uint32_t node_id, double weight) {
    printf("%u\t%+.10g\n", node_id, weight);
}

void emit_same_block_walk_line(const uint8_t block_id, const uint32_t from_id, const uint32_t to_id) {
    printf("%u\tS %u %u\n", block_id, from_id, to_id);
}

void emit_other_block_walk_line(const uint8_t block_id, const uint32_t from_id, const uint32_t to_id, const double weight) {
    printf("%u\tO %u %u %.10g\n", block_id, from_id, to_id,weight);
}

int main() {
//            ifstream in(
//            "C:\\Users\\Veniversum\\Documents\\a.School\\Caltech\\CS144\\rankmaniac\\src\\data\\input.txt");
//    cin.rdbuf(in.rdbuf());
//    map<uint32_t, double> weights;
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
        Node node(stoul(header), content, true);
//        node.pageRank += weights[node.id];
//        weights[node.id] = 0;
//        double weightsAlongEdges = (node.pageRank) * ALPHA;
        node.oldPageRank = node.pageRank;
//        visited.insert(node.id);
        if (node.outlinks_count > 0) {
//            node.pageRank = (1-ALPHA);
            for (const auto &neighbor:node.outlinks) {
//                emit_node_walk_line(neighbor,
//                                    weightsAlongEdges / node.outlinks_count);
                if (node.block_id == convert_to_block_id(neighbor)) {
                    emit_same_block_walk_line(node.block_id, node.id, neighbor);
                } else {
                    emit_other_block_walk_line(convert_to_block_id(neighbor), node.id, neighbor, node.outgoingPR());
                }
            }
        } else {
            // Hold on to the PageRank
//            weights[node.id] += weightsAlongEdges;

//            node.pageRank = (1-ALPHA) + weightsAlongEdges; // THIS LINE
            emit_same_block_walk_line(node.block_id, node.id, node.id);

//            weights[node.id] = 0;
//            emit_node_walk_line(node.id, weightsAlongEdges);
//            node.pageRank = weightsAlongEdges;
        }
        node.reemit_block();
    }

//    for (const auto &it:weights) {
//        emit_node_walk_line(it.first, it.second);
//    }

    return 0;
}