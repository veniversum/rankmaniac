#!/usr/bin/env python

import sys


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

    @staticmethod
    def emit_node_pagerank_line(node_id, page_rank):
        # !!! Prefixes the pagerank with `x` symbol for easier parsing
        sys.stdout.write('{0}\tx{1}\n'.format(node_id, page_rank))

    @staticmethod
    def emit_node_content_line(node_id, content):
        sys.stdout.write('{0}\t{1}\n'.format(node_id, content))


for line in sys.stdin:
    node = Node(line)

    ratio = node.pageRank / node.outlinks_count
    for neighbour in node.outlinks:
        Node.emit_node_pagerank_line(neighbour, ratio)

    Node.emit_node_content_line(node.id, node.original_content)
