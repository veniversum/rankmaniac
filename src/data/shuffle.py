import sys
if __name__ == '__main__':
    num_reducers = int(sys.argv[1])
    files = []
    for i in range(num_reducers):
        files.append(open('reduce%d.txt' % i, 'a'))
    for line in sys.stdin:
        parts = line.split('\t', 1)
        block = 0
        try:
            block = int(parts[0])
        except ValueError:
            pass
        files[block].write(line)
    for f in files:
        f.close()
