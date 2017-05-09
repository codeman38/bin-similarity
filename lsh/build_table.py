#!/usr/bin/env python3

from __future__ import print_function
import argparse
import io
import random
import pickle
import sys
import os
import lsh

def main():
    parser = argparse.ArgumentParser(
        description="Generates a locality sensitive hashing table "
                    "from a collection of files.")
    parser.add_argument('-s', '--size', type=int, default=256,
        help='length of hash to generate (default: %(default)d)')
    parser.add_argument('-l', '--length', type=int, default=8,
        help='length of substring to use for hashing (default: %(default)d)')
    parser.add_argument('-r', '--random', type=int, default=None,
        help='use this specific random seed')
    parser.add_argument('outfile',
        help='file in which to generate table')
    parser.add_argument('infile', nargs='+',
        help='file(s) to index in table')
    args = parser.parse_args()

    if os.path.isfile(args.outfile):
        parser.error('{0} already exists! Exiting.'.format(args.outfile))

    if args.random:
        random.seed(args.random)
    xors = [random.randint(0, lsh.MAX_HASH_CODE) 
            for _ in range(args.size)]

    out = io.open(args.outfile, 'wb')
    pickler = pickle.Pickler(out, 2) # Py2 compatibility
    pickler.dump(xors)
    pickler.dump(args.length)

    for fname in args.infile:
        with io.open(fname, 'rb') as fp:
            data = fp.read()
        minhash = lsh.minhash(data, args.length, xors)
        pickler.dump(minhash)
        pickler.dump(fname)
        print(fname, file=sys.stderr)

    out.close()

if __name__=='__main__':
    main()
