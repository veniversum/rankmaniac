#!/usr/bin/env python
import sys


# import base64
# import cPickle


class Node:
    # Break down the input line into useful components
    def __init__(self, id, content):
        values = [x for x in content.split(',') if x]

        self.id = id
        self.pageRank = float(values[0])
        self.oldPageRank = float(values[1])
        self.original_content = content
        self.outlinks = values[2:]
        self.outlinks_count = len(self.outlinks)

    def reemit(self):
        # sys.stdout.write(self.id + '\t' + base64.b64encode(cPickle.dumps(self)) + '\n')
        sys.stdout.write('{0}\t{1},{2},{3}\n'.format(self.id, self.pageRank, self.oldPageRank, ','.join(self.outlinks)))

    @classmethod
    def decode(cls, content, reemit=True):
        parts = content.split('\t', 1)
        if parts[0][0] == 'N':
            return cls(parts[0].split(':')[1], parts[1].strip())
        elif parts[1][0] == '+':
            return parts[0], float(parts[1])
        else:
            # return cPickle.loads(base64.b64decode(parts[1]))
            return cls(parts[0], parts[1].strip())

    @staticmethod
    def emit_node_walk_line(node_id, aux):
        sys.stdout.write('{0}\t+{1}\n'.format(node_id, aux))

    def emit_as_final(self):
        sys.stdout.write('FinalRank:{0}\t{1}\n'.format(self.pageRank, self.id))


def make_top_hash(node_list):
    # How many K to look at?
    PATIENCE_INTERVAL = 40
    hash = 7
    for n in node_list[:PATIENCE_INTERVAL]:
        hash = 31 * hash + int(n.id)
    return hash


def main():
    # Damping factor
    ALPHA = 0.85
    # Tolerance for floating point comparisons
    EPSILON = 0.0001
    # Stop after rank of top K pages don't change after this number of iterations
    PATIENCE = 1
    # We must output something by this iteration
    MAX_ITER = 50

    cur_iter = 1
    top_hash = None
    num_rounds_no_change = 0

    node_list = []

    for line in sys.stdin:
        if line[:4] == 'INFO':
            tokens = line.split()
            if tokens[1] == 'ITERNUM':
                cur_iter = int(tokens[2]) + 1
            elif tokens[1] == 'HASH':
                top_hash = int(tokens[2])
            elif tokens[1] == 'NUM_ROUNDS_NO_CHANGE':
                num_rounds_no_change = int(tokens[2])
            else:
                sys.stdout.write(line)
            continue

        node = Node.decode(line)
        node_list.append(node)

    shared_weights = (1 - ALPHA)
    node_list.sort(key=lambda n: n.pageRank, reverse=True)
    new_hash = make_top_hash(node_list)

    if new_hash == top_hash:
        num_rounds_no_change += 1
    else:
        num_rounds_no_change = 0

    if cur_iter >= MAX_ITER or num_rounds_no_change >= PATIENCE:
        for node in node_list[:20]:
            node.emit_as_final()

    else:
        sys.stdout.write('INFO\tITERNUM {0}\n'.format(cur_iter))
        sys.stdout.write('INFO\tNUM_ROUNDS_NO_CHANGE {0}\n'.format(num_rounds_no_change))
        for node in node_list:
            # if node.pageRank < EPSILON:
            #     break
            node.pageRank += shared_weights
            node.reemit()
        sys.stdout.write('INFO\tHASH {0}\n'.format(new_hash))


main()
