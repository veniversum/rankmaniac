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

for i in range(1, iterations + 1):

    # Run the iteration
    os.system('python pagerank_map.py < {0}.txt > {1}.txt'.format('output', '1_aft_pagerank_map'))
    os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('1_aft_pagerank_map', '2_aft_sort'))
    os.system('python pagerank_reduce.py < {0}.txt > {1}.txt'.format('2_aft_sort', '3_aft_pagerank_reduce'))
    os.system('python process_map.py < {0}.txt > {1}.txt'.format('3_aft_pagerank_reduce', '4_aft_process_map'))
    os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('4_aft_process_map', '5_aft_sort'))
    os.system('python process_reduce.py < {0}.txt > {1}.txt'.format('5_aft_sort', 'output'))

    # Print stats,
    with open('./output.txt') as f:
        total = 0
        all_lines_are_final = True
        for k, l in enumerate(f):
            total += 1
            if not l.startswith('FinalRank'):
                all_lines_are_final = False

        print("Iteration {0}: {1} lines in output.txt".format(i, total))

        if total < 1:
            print('File is empty, stopping iteration process!')
            break

        if all_lines_are_final:
            print('Generated final nodes!')
            break

    if i > MAX_ITERATIONS:
        print('Reached maximum number of iterations! ({0})'.format(MAX_ITERATIONS))
        break
