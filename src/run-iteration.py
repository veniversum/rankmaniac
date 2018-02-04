#!/usr/bin/env python

import os
import sys
import shutil

iterations = 50
MAX_ITERATIONS = 100

if len(sys.argv) < 2:
    print(
        'You can pass an argument specifying the # of iterations. Using default value of `{0}`.'.format(
            iterations))
else:
    iterations = int(sys.argv[1])

print('Preparing to run {0} iterations...'.format(iterations))

curr_script_path = os.path.dirname(os.path.abspath(__file__))

scripts = [
    'data/pagerank_map.py',
    'tuple-sort.py',
    'data/pagerank_reduce.py',
    'data/process_map.py',
    'tuple-sort.py',
    'data/process_reduce.py',
]
initial_input = 'local_results/initial_input.txt'
final_output = 'local_results/final_output.txt'
files = [
    'local_results/intermediate/output.txt',
    'local_results/intermediate/1_aft_pagerank_map.txt',
    'local_results/intermediate/2_aft_sort.txt',
    'local_results/intermediate/3_aft_pagerank_reduce.txt',
    'local_results/intermediate/4_aft_process_map.txt',
    'local_results/intermediate/5_aft_sort.txt',
    'local_results/intermediate/output.txt',
]

# Prepare data set for iteration process
shutil.copyfile(initial_input, files[0])

for i in range(1, iterations + 1):

    # Run the iteration
    for j in range(0, len(scripts)):
        os.system('python {0} < {1} > {2}'.format(scripts[j], files[j], files[j + 1]))

    # Print stats,
    with open(files[-1]) as f:
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

# Copy the final output
shutil.copyfile(files[-1], final_output)
