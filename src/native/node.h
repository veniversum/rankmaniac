//
// Created by Veniversum on 05/02/2018.
//

#ifndef RANKMANIAC_NODE_H
#define RANKMANIAC_NODE_H

#include <vector>
#include <sstream>
#include <iostream>
#include <cstdio>

using namespace std;

class Node {
public:
    string id;
    double pageRank{};
    double oldPageRank = 0;
    vector<string> outlinks;
    int outlinks_count = 0;
    string outlinks_str = "";

    Node(const string &header, const string &content, bool expand_outlinks) {
        id = header;
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
                        outlinks.push_back(substr);
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
            printf("%s\t%.10g,%.10g,%s\n", id.c_str(), pageRank, oldPageRank,
                   outlinks_str.c_str());
        else
            printf("%s\t%.10g,%.10g\n", id.c_str(), pageRank, oldPageRank);
    }

    inline void emitAsFinal() {
//        cout << "FinalRank:" << pageRank << '\t' << id << '\n';
        printf("FinalRank:%.10g\t%s\n", pageRank, id.c_str());
    }
};



//decode(char *content) {
//    char *found;
//    found = strsep(&content, "\t");
//    if (found != NULL && found[0] == 'N') {
//        return constructNode(found.strsep);
//    }
//    while ((found = strsep(&string, " ")) != NULL)
//        printf("%s\n", found);
//}

#endif //RANKMANIAC_NODE_H
