#!/usr/bin/env python2.7

from __future__ import print_function, division
try:
    from cdifflib import CSequenceMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Finds the most similar files to a given file.')
    parser.add_argument('target',
        help='file for which to find matches')
    parser.add_argument('other', nargs='+',
        help='other file(s) to compare')
    parser.add_argument('-n', '--num', type=int, default=0,
        help='use quick_ratio to identify this many best guesses '
             'before calculating the true similarity ratios')
    parser.add_argument('-l', '--longest', action='store_true',
        help='use longest match instead of ratio')
    parser.add_argument('-s', '--scaled', action='store_true',
        help='scale ratios relative to file sizes (including '
             'initial filtering by rough ratio)')
    args = parser.parse_args()

    with open(args.target, 'rb') as fp:
        seq1 = fp.read()

    matcher = SequenceMatcher()
    matcher.set_seq2(list(seq1))

    if args.num > 0:
        estimates = []
        for fname in args.other:
            if fname == args.target:
                continue
            with open(fname, 'rb') as fp:
                seq2 = fp.read()
            matcher.set_seq1(list(seq2))
            ratio = matcher.quick_ratio()
            estimates.append((fname, ratio))
        estimates.sort(key=lambda x: x[1])
        estimates = estimates[-args.num:]
        nbest = [x[0] for x in estimates]
    else:
        nbest = args.other

    actuals = []
    for idx, fname in enumerate(nbest):
        print('{0}/{1}'.format(idx, len(nbest)), file=sys.stderr)
        with open(fname, 'rb') as fp:
            seq2 = fp.read()
        matcher.set_seq1(list(seq2))
        metric = matcher.ratio()
        if args.longest:
            metric = max(x.size for x in matcher.get_matching_blocks())
        else:
            metric = matcher.ratio()
            if args.scaled:
                metric *= (len(seq1) + len(seq2)) / 2
        actuals.append((fname, metric))
    actuals.sort(key=lambda x: x[1])
    for stat in actuals:
        print('{0}\t{1}'.format(stat[1], stat[0]))

if __name__=='__main__':
    main()
