#!/usr/bin/env python

from os import path
import sys
import shutil
import argparse

if __name__ == '__main__':
    print("Preparing to write data set to `local_results/initial_input.txt`...\n")

    choice = None
    if len(sys.argv) < 2 or sys.argv[1] not in ['1', '2']:
        print("Specify data set number:")
        print("  1   - GNPn100p05 data set")
        print("  2   - EmailEnron data set")
        choice = str(input('Data set number: '))
        if choice not in ['1', '2']:
            raise Exception('Invalid option provided. ' + choice)
    else:
        choice = sys.argv[1]

    dataset = 'EmailEnron' if choice == '2' else 'GNPn100p05'
    script_path = path.dirname(path.abspath(__file__))
    source = path.join(script_path, 'local_test_data', dataset)
    target = path.join(script_path, 'local_results', 'initial_input.txt')

    shutil.copyfile(source, target)
    print("Saved {0} into `local_results/initial_input.txt`!".format(dataset))
