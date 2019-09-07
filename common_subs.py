#!/usr/bin/env python2.7

from __future__ import print_function
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Finds common substrings between two ROMs.')
    parser.add_argument('file1', 
        help='first file to compare')
    parser.add_argument('file2',
        help='second file to compare')
    parser.add_argument('-m', '--min', type=int, default=16,
        help='minimum length of match (default: %(default)s)')
    parser.add_argument('-n', '--no-repeat', action='store_true',
        help='ignore strings that consist entirely of a single byte repeated')
    args = parser.parse_args()

    with open(args.file1,'rb') as fp:
        data1 = fp.read()
    with open(args.file2,'rb') as fp:
        data2 = fp.read()

    for match in find_matches(data1, data2, args.min):
        match_len, pos1, pos2 = match
        match_str = data1[pos1:pos1+match_len]
        if not args.no_repeat or not is_repeated_byte(match_str):
            print('Found match of length {0} at {1:08x}/{2:08x}:'.format(
                match_len, pos1, pos2))
            print(spaced_hexlify(data1[pos1:pos1+match_len]))
            print()

def find_matches(data1, data2, min_len=1):
    if min_len < 1: min_len = 1
    matched1, matched2 = [], []
    for p1 in range(len(data1)):
        if contains_pos(matched1, p1):
            continue
        matched2[:] = []
        for p2 in range(len(data2)):
            if contains_pos(matched2, p2):
                continue
            match_len = longest_match(data1, p1, data2, p2)
            if match_len >= min_len:
                yield (match_len, p1, p2)
                matched1.append((p1, p1+match_len))
                matched2.append((p2, p2+match_len))

def contains_pos(matched, pos):
    for rng in matched:
        if pos >= rng[0] and pos < rng[1]:
            return True
    return False

def longest_match(data1, s1, data2, s2):
    max_pos = min(len(data1)-s1, len(data2)-s2)
    pos = 0
    while pos < max_pos:
        if data1[s1+pos] != data2[s2+pos]:
            break
        pos += 1
    return pos

def spaced_hexlify(bytestring):
    return ' '.join('{0:02x}'.format(safe_ord(x)) for x in bytestring)

def safe_ord(ch):
    if isinstance(ch, int):
        return ch
    else:
        return ord(ch)

def is_repeated_byte(bytestring):
    return all(x==bytestring[0] for x in bytestring)

if __name__=='__main__':
    main()
