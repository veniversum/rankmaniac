#!/usr/bin/env python

import os
import sys
import shutil

from score import Scorer

MAX_ITERATIONS = 50


def run(iterations=MAX_ITERATIONS, algorithm_path='./', evalutation_path=None):
    scorer = None
    if evalutation_path:
        scorer = Scorer(evalutation_path)
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
    shutil.copyfile('./input.txt', './output.txt')

    for i in range(1, iterations + 1):

        # Run the iteration
        os.system(
            'python {0}pagerank_map.py < {1}.txt > {2}.txt'.format(algorithm_path, 'output', '1_aft_pagerank_map'))
        os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('1_aft_pagerank_map', '2_aft_sort'))
        os.system('python {0}pagerank_reduce.py < {1}.txt > {2}.txt'.format(algorithm_path, '2_aft_sort',
                                                                            '3_aft_pagerank_reduce'))
        os.system('python {0}process_map.py < {1}.txt > {2}.txt'.format(algorithm_path, '3_aft_pagerank_reduce',
                                                                        '4_aft_process_map'))
        os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('4_aft_process_map', '5_aft_sort'))
        os.system('python {0}process_reduce.py < {1}.txt > {2}.txt'.format(algorithm_path, '5_aft_sort', 'output'))

        # Print stats,
        with open('./output.txt') as f:
            total = 0
            all_lines_are_final = True
            for k, l in enumerate(f):
                total += 1
                if not l.startswith('FinalRank'):
                    all_lines_are_final = False

            print "Iteration {0}: {1} lines in output.txt".format(i, total)

            if total < 1:
                print 'File is empty, stopping iteration process!'
                break

            if all_lines_are_final:
                print 'Generated final nodes!'
                break

        if i > MAX_ITERATIONS:
            print 'Reached maximum number of iterations! ({0})'.format(MAX_ITERATIONS)
            break
    if scorer:
        scorer.score('./output.txt')


if __name__ == '__main__':
    iterations = None
    kwargs = {}
    if len(sys.argv) < 2:
        print 'You can pass an argument specifying the # of iterations. Using default value of `{0}`.'.format(
            iterations)
    else:
        kwargs['iterations'] = int(sys.argv[1])

    if len(sys.argv) > 2:
        kwargs['algorithm_path'] = sys.argv[2]
        print 'Using algorithm at %s' % kwargs['algorithm_path']
    if len(sys.argv) > 3:
        kwargs['evalutation_path'] = sys.argv[3]
        print 'Using solutions at %s' % kwargs['evalutation_path']

    print 'Preparing to run {0} iterations...'.format(1)
    run(**kwargs)
