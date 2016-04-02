#!/usr/bin/python

# Reads a single strand of DNA, outputs features

# The window to extract features from.
window_backward = 15
window_forward = 14

import sys

# By default, the program doesn't print any headers for the TSV file. Check if we should print the header.
if len(sys.argv) == 2 and (sys.argv[1] == "--header" or sys.argv[1] == "--header-only"):
	# Print the header
	print("#response\t%s\t%s" % ("\t".join(map(lambda i: "nucleotide(%s)" % i, range(-window_backward, window_forward + 1))),
	                             "\t".join(map(lambda i: "codon(%s)" % i, range(-window_backward // 3, (window_forward + 1) // 3)))))
	
	if sys.argv[1] == "--header-only":
		sys.exit(0)
elif len(sys.argv) != 1:
	# We're not printing the header. Ensure there are no superfluous arguments.
	sys.exit("Wrong args. Either call %s without arguments or with --header or --header-only to print the header." % sys.argv[0])


# The user wants us to process the file

#import fileinput
from boltons.iterutils import windowed_iter
from itertools import zip_longest

def split_input_line(line):
	items = line.rstrip().split("\t")
	return {"nucleotide": items[0],
	 "response": items[1]}

def group_n(iterable, n, padvalue=None):
	"""group_n('abcdefg', 3, 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"""
	return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


# Print the observations
block = []
for line in sys.stdin:
	if line != "\n":
		# We're inside a single block. Carry on reading more lines
		block.append(line)
		continue
	
	# We have detected an empty line, therefore the block has just ended. Process it using a window.
	for ntuple in windowed_iter(map(split_input_line, block), window_backward + 1 + window_forward):
		#ntuple_backward = ntuple[0:window_backward]
		current_item = ntuple[window_backward]
		#ntuple_forward = ntuple[window_backward + 1:]
		
		# TODO distance from nearest beginning, distance from nearest end, …
		
		
		print("%s\t%s\t%s" % (current_item["response"],
			"\t".join(map(lambda x: x["nucleotide"], ntuple)),
			"\t".join(map(lambda x: "".join([i["nucleotide"] for i in x]), group_n(ntuple, 3))))) # TODO
	
	# Empty the block
	block = []









