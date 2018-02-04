#!/usr/bin/env python

import sys
from collections import deque

MAX_ITER = 50
NUM_WALKS = 50


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
        content = parts[1]
        count = float(parts[2])

        self.final = header[0] is 'FinalRank'

        if self.final:
            self.id = content
            self.pageRank = float(header[1])
        else:
            self.id = header[1]
            values = content.split(',')
            self.pageRank = count
            self.oldPageRank = float(values[0])
            self.original_content = content
            self.outlinks = values[2:]
            self.outlinks_count = len(self.outlinks)

    def re_emit(self):
        sys.stdout.write(
            'NodeId:{0}\t{1},{2},{3}\n'.format(self.id, self.pageRank, self.oldPageRank, ','.join(self.outlinks)))

    def emit_as_final(self):
        sys.stdout.write('FinalRank:{0}\t{1}\n'.format(self.pageRank, self.id))


queue = deque()
cur_iter = 1
shared_weights = 0

node_list = []

for line in sys.stdin:
    if str(line).startswith('ITERNUM'):
        cur_iter = int(line.split('\t')[1])
        continue
    node = Node(line)
    if node.id == '-1':
        shared_weights = node.pageRank
    else:
        node_list.append(node)

shared_weights /= len(node_list)

if cur_iter >= MAX_ITER:
    for node in sorted(node_list, key=lambda n: n.pageRank, reverse=True):
        node.pageRank += shared_weights
        node.pageRank /= NUM_WALKS
        node.emit_as_final()
else:
    sys.stdout.write('ITERNUM\t{0}\n'.format(cur_iter))
    for node in node_list:
        node.pageRank += shared_weights
        node.pageRank /= NUM_WALKS
        node.re_emit()
