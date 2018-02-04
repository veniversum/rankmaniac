#!/usr/bin/env python

import sys

DAMPING_FACTOR = 0.85


def emit_node_info(node_id, new_pagerank, old_pagerank, outlinks):
    new_pagerank = (1 - DAMPING_FACTOR) + (DAMPING_FACTOR * new_pagerank)
    if outlinks:
        sys.stdout.write('NodeId:{0}\t{1},{2},{3}\n'.format(node_id, new_pagerank, old_pagerank, outlinks))
    else:
        sys.stdout.write('NodeId:{0}\t{1},{2}\n'.format(node_id, new_pagerank, old_pagerank))


prev_id = None

pagerank = 0
old_pagerank = 0
outlinks = None

for line in sys.stdin:
    parts = line.strip().split('\t')
    node_id = int(parts[0])
    content = parts[1]

    if node_id != prev_id:
        if prev_id is not None:  # Not before first node; emit previous node
            emit_node_info(prev_id, pagerank, old_pagerank, outlinks)

        # New node
        prev_id = node_id
        pagerank = 0
        old_pagerank = 0
        outlinks = None

    if content.startswith('x'):  # Contributing pagerank
        pagerank += float(content[1:])
    else:  # Node metadata
        values = content.split(',')
        old_pagerank = values[0]
        outlinks = ','.join(values[2:])
        

# Make sure we emit data for the last node
emit_node_info(prev_id, pagerank, old_pagerank, outlinks)

