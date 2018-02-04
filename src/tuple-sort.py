#!/usr/bin/env python

import sys
from collections import deque

class SortNode:

    def __init__(self, line):
        parts = line.split('\t', 1)
        self.key = parts[0]
        self.value = parts[1]

    def re_emit(self):
        sys.stdout.write('{0}\t{1}'.format(self.key, self.value))

queue = deque()

for line in sys.stdin:
    queue.append(SortNode(line))

nodes = list(queue)
nodes.sort(key=lambda x: x.key)

for node in nodes:
    node.re_emit()
