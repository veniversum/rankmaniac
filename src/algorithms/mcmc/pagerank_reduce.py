#!/usr/bin/env python

import sys
from collections import defaultdict


def emit_node_info(node_id, old_data, num_visits):
    sys.stdout.write('NodeId:{0}\t{1}\t{2}\n'.format(node_id, old_data, num_visits))


DAMPING_FACTOR = 0.85

prev_id = None

pagerank = 0
old_pagerank = 0
outlinks = None

NODE_VISITORS = defaultdict(int)
NODE_DATA = {}

for line in sys.stdin:
    parts = line.split('\t', 1)
    if parts[0] == 'ITERNUM':
        sys.stdout.write('ITERNUM\t{0}\n'.format(int(parts[1]) + 1))
    node_id = parts[0]
    if parts[1].startswith('PASS_'):
        NODE_DATA[node_id] = parts[1][5:-1]
        continue

    NODE_VISITORS[node_id] += 1

for k, v in NODE_DATA.items():
    emit_node_info(k, v, NODE_VISITORS[k])

if '-1' in NODE_VISITORS:
    emit_node_info('-1', '0,0,0', NODE_VISITORS['-1'])
