#!/usr/bin/env python

import sys
from collections import defaultdict


# import base64
# import cPickle


class Node:
    # Break down the input line into useful components
    def __init__(self, id, content):
        values = [x for x in content.split(',') if x]

        self.id = id
        self.pageRank = float(values[0])
        self.oldPageRank = float(values[1])
        self.original_content = content
        self.outlinks = values[2:]
        self.outlinks_count = len(self.outlinks)

    def reemit(self):
        # sys.stdout.write(self.id + '\t' + base64.b64encode(cPickle.dumps(self)) + '\n')
        sys.stdout.write('{0}\t{1},{2},{3}\n'.format(self.id, self.pageRank, self.oldPageRank, ','.join(self.outlinks)))

    @classmethod
    def decode(cls, content, reemit=True):
        parts = content.split('\t', 1)
        if parts[0][0] == 'N':
            return cls(parts[0].split(':')[1], parts[1].strip())
        elif parts[1][0] == '+':
            return parts[0], float(parts[1])
        else:
            # return cPickle.loads(base64.b64decode(parts[1]))
            return cls(parts[0], parts[1].strip())

    @staticmethod
    def emit_node_walk_line(node_id, aux):
        sys.stdout.write('{0}\t+{1}\n'.format(node_id, aux))

    def emit_as_final(self):
        sys.stdout.write('FinalRank:{0}\t{1}\n'.format(self.pageRank, self.id))


def main():
    NODE_VISITORS = defaultdict(float)
    NODE_DATA = {}

    for line in sys.stdin:
        if line[:4] == 'INFO':
            sys.stdout.write(line)
            continue
        node = Node.decode(line)
        if isinstance(node, Node):
            NODE_DATA[node.id] = node
        else:
            NODE_VISITORS[node[0]] += node[1]

    for k, v in NODE_DATA.items():
        v.pageRank = NODE_VISITORS[k]
        v.reemit()


main()
