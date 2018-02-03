#!/usr/bin/env python

import os
import sys
import shutil

iterations = 1
MAX_ITERATIONS = 100

if len(sys.argv) < 2:
    print('You can pass an argument specifying the # of iterations. Using default value of `{0}`.'.format(iterations))
else:
    iterations = int(sys.argv[1])

print('Preparing to run {0} iterations...'.format(1))

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
shutil.copyfile('./input.txt', './output.txt')

current_iter = './output.txt'
prev_iter = './output1.txt'

for i in range(1, iterations + 1):

    # Swap files for iterations
    temp = current_iter
    current_iter = prev_iter
    prev_iter = temp

    # Run the iteration
    command = 'python pagerank_map.py < {0} | sort | python pagerank_reduce.py | python process_map.py | sort | ' \
              'python process_reduce.py > {1}'.format(prev_iter, current_iter)
    os.system(command)

    # Print stats,
    with open(current_iter) as f:
        total = 0
        all_lines_are_final = True
        for k, l in enumerate(f):
            total += 1
            if not l.startswith('FinalNode'):
                all_lines_are_final = False

        print("Iteration {0}: {1} lines in output.txt".format(i, total))

        if all_lines_are_final:
            print('Generated final nodes!')
            break

    if i > MAX_ITERATIONS:
        print('Reached maximum number of iterations! ({0})'.format(MAX_ITERATIONS))
        break

if current_iter is not './output.txt':
    shutil.copyfile(current_iter, './output.txt')
    os.remove(current_iter)
else:
    os.remove(prev_iter)
