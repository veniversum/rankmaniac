import sys


class Scorer(object):
    def __init__(self, target_file):
        with open(target_file, 'r') as f:
            self.target = [i.strip() for i in f.readlines()]

    def score(self, predict_file):
        with open(predict_file, 'r') as f:
            predictions = [i.split('\t')[1].strip() for i in f.readlines()]
        if predictions is None:
            raise Exception('Invalid predictions file!')
        cum_error = 0
        for i, t in enumerate(self.target):
            try:
                cum_error += (predictions.index(t) - i) ** 2
            except ValueError:
                raise Exception('Predictions did not include top 20!')

        print 'Total error: %d' % cum_error


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Required params: Target file, Predict file'
        exit()
    scorer = Scorer(sys.argv[1])
    scorer.score(sys.argv[2])
