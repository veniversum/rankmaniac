predict_file = 'data/output.txt'
target_file = 'sols/GNPn100p05'

if __name__ == '__main__':
    target = None
    predictions = None
    with open(target_file, 'r') as f:
        target = [i.strip() for i in f.readlines()]

    if target is None:
        raise Exception('Invalid target file!')

    with open(predict_file, 'r') as f:
        predictions = [i.split('\t')[1].strip() for i in f.readlines()]

    if predictions is None:
        raise Exception('Invalid predictions file!')

    cum_error = 0
    for i, t in enumerate(target):
        try:
            cum_error += (predictions.index(t) - i) ** 2
        except ValueError:
            raise Exception('Predictions did not include top 20!')

    print 'Total error: %d' % cum_error
