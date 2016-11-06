#!/usr/bin/env python2.7

from __future__ import print_function, division
import difflib
#import diff_match_patch
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Finds the most similar files to a given file.')
    parser.add_argument('target',
        help='file for which to find matches')
    parser.add_argument('other', nargs='+',
        help='other file(s) to compare')
    parser.add_argument('-l', '--longest', action='store_true',
        help='use longest match instead of ratio')
    parser.add_argument('-s', '--scaled', action='store_true',
        help='scale ratios relative to file sizes (including '
             'initial filtering by rough ratio)')
    args = parser.parse_args()

    with open(args.target, 'rb') as fp:
        seq1 = fp.read()

    estimates = []
    matcher = difflib.SequenceMatcher()
    matcher.set_seq2(seq1)
    for fname in args.other:
        if fname == args.target:
            continue
        with open(fname, 'rb') as fp:
            seq2 = fp.read()
        matcher.set_seq1(seq2)
        ratio = matcher.quick_ratio()
        if args.scaled:
            ratio *= (len(seq1) + len(seq2)) / 2
        estimates.append((fname, ratio))
    estimates.sort(key=lambda x: x[1])
    estimates = estimates[-100:]

    actuals = []
    for idx, (fname, ratio) in enumerate(estimates):
        print('{0}/{1}'.format(idx, len(estimates)), file=sys.stderr)
        with open(fname, 'rb') as fp:
            seq2 = fp.read()
        matcher.set_seq1(seq2)
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