#!/usr/bin/env python

import sys
import random

#
# This program simply represents the identity function.
#

for line in sys.stdin:
    print_final = random.random() < 0.7
    if print_final:
        sys.stdout.write('FinalNode: 123\n')
    else:
        sys.stdout.write(line)

