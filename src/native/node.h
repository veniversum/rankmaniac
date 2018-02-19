//
// Created by Veniversum on 05/02/2018.
//

#ifndef RANKMANIAC_NODE_H
#define RANKMANIAC_NODE_H

#include <vector>
#include <sstream>
#include <iostream>
#include <cstdio>
#define NUM_REDUCERS 1

using namespace std;

class Node {
public:
    uint32_t id;
    uint8_t block_id;
    double pageRank{};
    double oldPageRank = 0;
    vector<uint32_t > outlinks;
    int outlinks_count = 0;
    string outlinks_str = "";

    Node(const uint32_t header, const string &content, bool expand_outlinks) {
        id = header;
        block_id = static_cast<uint8_t>(header % NUM_REDUCERS);
        auto start = 0U;
        auto end = content.find(',');
        pageRank = stod(content.substr(start, end - start));
        start = end + 1;
        end = content.find(',', start);
        if (end != string::npos) {
            oldPageRank = stod(content.substr(start, end - start));
            start = end + 1;
            outlinks_str = content.substr(start);
            if (expand_outlinks) {
                string substr;
                stringstream ss(outlinks_str);
                while (ss.good()) {
                    getline(ss, substr, ',');
                    if (!substr.empty())
                        outlinks.push_back(stoul(substr));
                }
                outlinks_count = outlinks.size();
            }
        } else {
            oldPageRank = stod(content.substr(start));
        }
    }

    inline void reemit() {
//        cout << id << '\t' << pageRank << ',' << oldPageRank << ','
//             << outlinks_str << '\n';
        if (!outlinks_str.empty())
            printf("%u\t%.10g,%.10g,%s\n", id, pageRank, oldPageRank,
                   outlinks_str.c_str());
        else
            printf("%u\t%.10g,%.10g\n", id, pageRank, oldPageRank);
    }

    inline void reemit_block() {
//        cout << id << '\t' << pageRank << ',' << oldPageRank << ','
//             << outlinks_str << '\n';
        if (!outlinks_str.empty())
            printf("%u\tN %u %.10g,%.10g,%s\n", block_id, id, pageRank, oldPageRank,
                   outlinks_str.c_str());
        else
            printf("%u\tN %u %.10g,%.10g\n", block_id, id, pageRank, oldPageRank);
    }

    inline void emitAsFinal() {
//        cout << "FinalRank:" << pageRank << '\t' << id << '\n';
        printf("FinalRank:%.10g\t%u\n", pageRank, id);
    }

    inline double outgoingPR() {
        if (outlinks_count > 0)
            return pageRank / outlinks_count;
        return pageRank;
    }
};

static inline uint8_t convert_to_block_id(const uint32_t id) {
    return static_cast<uint8_t>(id % NUM_REDUCERS);
}
#endif //RANKMANIAC_NODE_H
