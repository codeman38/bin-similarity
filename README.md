# bin-similarity

Miscellaneous Python scripts for finding similar code segments among binaries.

So far, these include:

## most_similar.py

This script, given a binary and a set of other binaries for comparison, will use difflib to narrow down the search (using quick_ratio) and then identify the closest matching files from the filtered list.

Options:

* `-s`: Instead of using the ratio of matching bytes, the absolute number of matching bytes (i.e., the ratio multiplied by half the combined length) will be used when ranking the results. (Note that this scaling is *not* applied during quick_ratio filtering, as the estimates for large files tend to be very high after scaling.)

* `-l`: For ranking, instead of using the total number of matching bytes, use only the length of the longest contiguous match.

* `-m`: Read only this many bytes from each file, rather than using the entire file.

## common_subs.py

This script will do a brute-force comparison of two files to find non-overlapping substrings above a given length which occur in both files, and will print the hexlified substrings along with their offsets within the two files.

Options:

* `-n`: Omit strings consisting entirely of a single byte repeated (e.g., `00 00 00 00`) when displaying the output.
