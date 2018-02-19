#!/usr/bin/env python

import sys
from random import random, randint

ALPHA = 0.85
EPSILON = 1 - ALPHA
NUM_WALKS = 500


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
            values = [x for x in content.split(',') if x]
            self.pageRank = float(values[0])
            self.oldPageRank = float(values[1])
            self.original_content = content
            self.outlinks = values[2:]
            self.outlinks_count = len(self.outlinks)

    @staticmethod
    def emit_node_walk_line(node_id, aux):
        sys.stdout.write('{0}\t{1}\n'.format(node_id, aux))

    @staticmethod
    def emit_node_pagerank_line(node_id, page_rank):
        # !!! Prefixes the pagerank with `x` symbol for easier parsing
        sys.stdout.write('{0}\tx{1}\n'.format(node_id, page_rank))

    @staticmethod
    def emit_node_content_line(node_id, content):
        sys.stdout.write('{0}\tPASS_{1}\n'.format(node_id, content))


for line in sys.stdin.readlines():
    parts = line.split('\t', 1)
    if parts[0] == 'ITERNUM':
        sys.stdout.write(line)
        continue
    node = Node(line)

    samples = node.pageRank * NUM_WALKS
    sample_follow_edges = samples * ALPHA
    sample_redistribute = samples * EPSILON
    if node.outlinks_count > 0:
        for neighbor in node.outlinks:
            Node.emit_node_walk_line(neighbor, sample_follow_edges / node.outlinks_count)
    else:
        Node.emit_node_walk_line(node.id, sample_follow_edges)

    Node.emit_node_walk_line('-1', sample_redistribute)

    Node.emit_node_content_line(node.id, node.original_content)
