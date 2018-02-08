#!/usr/bin/env python

import os
import sys
import shutil
import time

from score import Scorer

MAX_ITERATIONS = 50


def extract(f):
    import re
    pattern = re.compile(r'(\d+).*')
    pages = []
    for ll in f.readlines():
        match = pattern.match(ll)
        if match:
            n_id = match.group(1)
            if n_id != '-1':
                pages.append(n_id)
    return pages


def run(iterations=MAX_ITERATIONS, algorithm_path='./', evalutation_path=None):
    scorer = None
    if evalutation_path:
        scorer = Scorer(evalutation_path)
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
    shutil.copyfile('./input.txt', './output.txt')
    totaltime = 0.

    for i in range(1, iterations + 1):

        # Run the iteration
        initial = time.time()

        # os.system(
        #     'python {0}pagerank_map.py < {1}.txt > {2}.txt'.format(algorithm_path, 'output', '1_aft_pagerank_map'))
        # end = time.time()
        # print 'PageRank map took %f s' % (end - start)
        # start = time.time()
        # # os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('1_aft_pagerank_map', '2_aft_sort'))
        # os.system('python {0}pagerank_reduce.py < {1}.txt > {2}.txt'.format(algorithm_path, '1_aft_pagerank_map',
        #                                                           '3_aft_pagerank_reduce'))
        # end = time.time()
        # print 'PageRank map took %f s' % (end - start)
        # start = time.time()
        # os.system('python {0}process_map.py < {1}.txt > {2}.txt'.format(algorithm_path, '3_aft_pagerank_reduce',
        #                                                       '4_aft_process_map'))
        # end = time.time()
        # print 'PageRank map took %f s' % (end - start)
        # start = time.time()
        # # os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('4_aft_process_map', '5_aft_sort'))
        # os.system('python {0}process_reduce.py < {1}.txt > {2}.txt'.format(algorithm_path, '4_aft_process_map', 'output'))
        # end = time.time()
        # print 'PageRank map took %f s' % (end - start)
        # totaltime += end - initial

        # os.system('split -l 200000 output.txt')
        print 'Splitting file done!'
        start = time.time()
        os.system('{0}pagerank_map < {1} > {2}.txt'.format(algorithm_path, 'output.txt', '1_aft_pagerank_map'))
        # os.system('{0}pagerank_map < {1} >> {2}.txt'.format(algorithm_path, 'xab', '1_aft_pagerank_map'))
        end = time.time()
        print 'PageRank map took %f s' % (end - start)

        num_reducers = 10

        os.system('rm -f reduce*.txt')
        os.system('python shuffle.py {0} < {1}.txt'.format(num_reducers, '1_aft_pagerank_map'))

        # os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('1_aft_pagerank_map', '2_aft_sort'))
        start = time.time()
        os.system('rm -f 3_aft_pagerank_reduce.txt')
        for j in range(num_reducers):
            os.system('{0}pagerank_reduce < reduce{1}.txt >> {2}.txt'.format(algorithm_path, j, '3_aft_pagerank_reduce'))
        end = time.time()
        print 'PageRank reduce took %f s' % (end - start)
        start = time.time()
        os.system('{0}process_map < {1}.txt > {2}.txt'.format(algorithm_path, '3_aft_pagerank_reduce',
                                                   '4_aft_process_map'))
        end = time.time()
        print 'Process map took %f s' % (end - start)

        # os.system('python ../tuple-sort.py < {0}.txt > {1}.txt'.format('4_aft_process_map', '5_aft_sort'))
        start = time.time()
        os.system('{0}process_reduce < {1}.txt > {2}.txt'.format(algorithm_path, '4_aft_process_map', 'output'))
        end = time.time()
        print 'Process reduce took %f s' % (end - start)
        totaltime += end - initial

        # Print stats,
        with open('./output.txt') as f:
            total = 0
            all_lines_are_final = True
            for k, l in enumerate(f):
                total += 1
                if not l.startswith('FinalRank'):
                    all_lines_are_final = False

            print "Iteration {0}: {1} lines in output.txt. Round time: {2} Total time: {3}".format(i, total,
                                                                                                   end - initial,
                                                                                                   totaltime)

            if total < 1:
                print 'File is empty, stopping iteration process!'
                break

            if all_lines_are_final:
                print 'Generated final nodes!'
                break

            f.seek(0)

            predictions = extract(f)
            if scorer:
                scorer.score_raw(predictions)

        if i > MAX_ITERATIONS:
            print 'Reached maximum number of iterations! ({0})'.format(MAX_ITERATIONS)
            break
    if scorer:
        scorer.score('./output.txt')


if __name__ == '__main__':
    kwargs = {}
    if len(sys.argv) < 2:
        print 'You can pass an argument specifying the # of iterations. Using default value of `{0}`.'.format(
            MAX_ITERATIONS)
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
