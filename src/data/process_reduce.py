#!/usr/bin/env python

import sys
from collections import deque


class Node:
    # Break down the input line into useful components
    def __init__(self, node_line):
        self.line = node_line

        self.final = None
        self.id = None
        self.pageRank = None
        self.oldPageRank = None
        self.original_content = None
        self.outlinks = []
        self.outlinks_count = 0

        parts = node_line.split('\t')
        header = parts[0].split(':')
        content = parts[1][0:-1]

        self.final = header[0] is 'FinalRank'

        if self.final:
            self.id = content
            self.pageRank = float(header[1])
        else:
            self.id = header[1]
            values = content.split(',')
            self.pageRank = float(values[0])
            self.oldPageRank = float(values[1])
            self.original_content = content
            self.outlinks = values[2:]
            self.outlinks_count = len(self.outlinks)

    def re_emit(self):
        sys.stdout.write(self.line)

    def emit_as_final(self):
        sys.stdout.write('FinalRank:{0}\t{1}\n'.format(self.pageRank, self.id))

queue = deque()

for line in sys.stdin:
    queue.append(Node(line))

nodes = list(queue)
nodes.sort(key=lambda x: x.pageRank, reverse=True)

count = len(nodes)
if count is 20:
    for node in nodes:
        node.emit_as_final()
else:
    SHRINKING_COEFFICIENT = 0.7
    upper_slice = int(max(20, round(count * SHRINKING_COEFFICIENT)))
    for node in nodes[0:upper_slice]:
        node.re_emit()
