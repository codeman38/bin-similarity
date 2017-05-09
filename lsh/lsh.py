import sys
import zlib

MAX_HASH_CODE = 0xFFFFFFFF

def hashcode_fnv32(string):
    hashval = 0x811c9dc5
    for ch in string:
        if not isinstance(ch, int):
            ch = ord(ch)
        hashval = ((hashval * 0x1000193) & 0xFFFFFFFF) ^ ch
    return hashval

def hashcode_crc(string):
    return zlib.crc32(string) & 0xFFFFFFFF

def minhash(string, sublen, xors, hashfunc=hashcode_fnv32):
    hashes = [sys.maxsize for x in xors]
    for xor_idx, xor in enumerate(xors):
        for idx in range(len(string)+1-sublen):
            substr = string[idx:idx+sublen]
            hashval = hashfunc(substr) ^ xor
            if hashval < hashes[xor_idx]:
                hashes[xor_idx] = hashval
    return tuple(hashes)
