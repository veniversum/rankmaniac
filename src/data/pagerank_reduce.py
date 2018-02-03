#!/usr/bin/env python

import sys


def emit_node_info(node_id, new_pagerank, old_pagerank, outlinks):
    sys.stdout.write('NodeId:{0}\t{1},{2},{3}\n'.format(node_id, new_pagerank, old_pagerank, outlinks))


DAMPING_FACTOR = 0.85

prev_id = None

pagerank = 0
old_pagerank = 0
outlinks = None

for line in sys.stdin:

    parts = line.split('\t')
    node_id = parts[0]
    content = parts[1]
    content = content[0:-1]

    if node_id is not prev_id:
        if outlinks is not None:
            pagerank = 1 - DAMPING_FACTOR + (DAMPING_FACTOR * pagerank)
            emit_node_info(prev_id, pagerank, old_pagerank, outlinks)
        prev_id = node_id
        pagerank = 0
        old_pagerank = 0
        outlinks = None

    if content.startswith('x'):
        pagerank += float(content[1:])
    else:
        values = content.split(',')
        old_pagerank = values[0]
        outlinks = ','.join(values[2:])
