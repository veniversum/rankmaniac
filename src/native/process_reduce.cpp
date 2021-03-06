//
// Created by Veniversum on 06/02/2018.
//

#include <cstdio>
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
//#include <fstream>
#include "node.h"

#define MAX_ITER 2
#define PATIENCE 1
#define STRICTNESS 20
#define ALPHA 0.85
#define EPSILON 0.0001
//0.066

using namespace std;


uint32_t hashTopFew(const vector<Node> &nodes) {
    uint8_t cnt = 0;
    uint32_t hash = 1;
    for (auto it = nodes.begin();
         it != nodes.end() && cnt < STRICTNESS; ++it, ++cnt) {
        hash = hash * 31 + it->id;
    }
    return hash;
}

static inline bool cmp(const Node a, const Node b) {
    return a.pageRank > b.pageRank;
};

int main() {
//    ifstream in(
//            "C:\\Users\\Veniversum\\Documents\\a.School\\Caltech\\CS144\\rankmaniac\\src\\data\\3_aft_pagerank_reduce.txt");
//    cin.rdbuf(in.rdbuf());
    ios_base::sync_with_stdio(false);
    string header;
    string content;

    vector<Node> nodes;

    uint8_t cur_iter = 1;
    uint32_t old_hash = 0;
    uint32_t new_hash = 0;
    uint8_t num_rounds_no_change = 0;

    double global_delta = 0;
    while (cin >> header >> content) {
        if (header[0] == 'I') {
            //INFO
            if (content[0] == 'I') {
                //ITERNUM
                cur_iter = static_cast<uint8_t>(stoul(content.substr(1)));
            } else if (content[0] == 'H') {
                //HASH
                old_hash = stoul(content.substr(1));
            } else if (content[0] == 'N') {
                //NUM ROUNDS NO CHANGE
                num_rounds_no_change = static_cast<uint8_t>(stoul(
                        content.substr(1)));
            } else {
                printf("%s\t%s\n", header.c_str(), content.c_str());
            }
            continue;
        } else {
            nodes.emplace_back(stoul(header), content, false);
            Node node = nodes.back();
            global_delta += abs(node.pageRank - node.oldPageRank) / node.pageRank;
        }
    }
    global_delta /= nodes.size();

    int additional_sort = max(0, STRICTNESS - 20);

    partial_sort(nodes.begin(), nodes.begin() + 20 + additional_sort,
                 nodes.end(), cmp);

    if (global_delta >= EPSILON) {
        new_hash = hashTopFew(nodes);

        if (new_hash == old_hash) {
            num_rounds_no_change++;
        } else {
            num_rounds_no_change = 0;
        }
    }

    if (cur_iter >= MAX_ITER || num_rounds_no_change >= PATIENCE ||
        global_delta < EPSILON) {
        uint8_t cnt = 0;
        for (auto it = nodes.begin();
             it != nodes.end() && cnt < 20; ++it, ++cnt) {
            it->emitAsFinal();
        }
    } else {
        printf("I\tI%d\n", cur_iter + 1);
        printf("I\tN%d\n", num_rounds_no_change);
        printf("I\tH%u\n", new_hash);
        for (auto it : nodes) {
            it.reemit();
        }
    }

    return 0;
}