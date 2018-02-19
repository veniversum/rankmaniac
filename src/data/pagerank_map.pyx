#!/usr/bin/env python

from __future__ import print_function
import sys
from libc.stdio cimport printf
from cython cimport view



# import base64
# import cPickle

cdef class Node:
    # Break down the input line into useful components
    cdef bytes id
    cdef double pageRank
    cdef double oldPageRank
    cdef list outlinks
    cdef int outlinks_count

    def __init__(self, id, content):
        values = [x for x in content.split(',') if x]

        self.id = id
        self.pageRank = float(values[0])
        self.oldPageRank = float(values[1])
        self.outlinks = values[2:]
        self.outlinks_count = len(self.outlinks)

    cdef reemit(self):
        # sys.stdout.write(self.id + '\t' + base64.b64encode(cPickle.dumps(self)) + '\n')
        printf("%s\t%f,%f,%s\n", self.id, self.pageRank, self.oldPageRank, <bytes>','.join(self.outlinks))

    @staticmethod
    cdef emit_node_walk_line(bytes node_id, float aux):
        printf("%s\t%+f\n", node_id, aux)

    cdef emit_as_final(self):
        printf("FinalRank:%f\t%s\n", self.pageRank, self.id)

cdef Node decode(bytes content):
    cdef list parts = content.split('\t')
    if parts[0][0] == 'N':
        return Node(parts[0].split(':')[1], parts[1].strip())
    elif parts[1][0] == '+':
        return parts[0], float(parts[1])
    else:
        # return cPickle.loads(base64.b64decode(parts[1]))
        return Node(parts[0], parts[1].strip())

cdef main():
    cdef double ALPHA = 0.85
    cdef double EPSILON = 0.00001
    cdef Node node
    for line in sys.stdin:
        if line[:4] == 'INFO':
            sys.stdout.write(line)
            continue
        node = decode(line)
        # if node is None:
        #       continue
        # if abs(node.pageRank - node.oldPageRank) < EPSILON and abs(node.pageRank - 1.) < EPSILON:
        # pass
        # PageRank of node is too low to bother,
        # continue
        sample_follow_edges = node.pageRank * ALPHA
        node.oldPageRank = node.pageRank
        node.pageRank = 0
        # sample_redistribute = node.pageRank * (1 - ALPHA)
        if node.outlinks_count > 0:
            for neighbor in node.outlinks:
                Node.emit_node_walk_line(neighbor, sample_follow_edges / node.outlinks_count)
        else:
            Node.emit_node_walk_line(node.id, sample_follow_edges)

        # Node.emit_node_walk_line('-1', sample_redistribute)

        node.reemit()


main()
