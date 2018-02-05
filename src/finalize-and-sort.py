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
        content = parts[1].replace('\n', '')

        self.final = header[0] == 'FinalRank'

        if self.final:
            self.id = content
            self.pageRank = float(header[1])
        else:
            self.id = header[0]
            values = content.split(',')
            self.pageRank = float(values[0])
            self.oldPageRank = float(values[1])
            self.original_content = content
            self.outlinks = values[2:]
            self.outlinks_count = len(self.outlinks)

    @staticmethod
    def emit_node_pagerank_line(node_id, page_rank):
        # !!! Prefixes the pagerank with `x` symbol for easier parsing
        sys.stdout.write('{0}\tx{1}\n'.format(node_id, page_rank))

    @staticmethod
    def emit_node_content_line(node_id, content):
        sys.stdout.write('{0}\t{1}\n'.format(node_id, content))


queue = deque()

for line in sys.stdin:
    queue.append(Node(line))

nodes = list(queue)
nodes.sort(key=lambda n: n.pageRank, reverse=True)

for node in nodes:
    sys.stdout.write('{0:.2f}\t{1}\n'.format(node.pageRank, node.id))



