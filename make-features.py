#!/usr/bin/python

# Reads a single strand of DNA, outputs features

window_backward = 6
window_forward = 6



import fileinput
from boltons.iterutils import windowed_iter

def format_bool(b):
	if b:
		return "1"
	else:
		return "0"


def split_input_line(line):
	items = line.rstrip().split("\t")
	return {"nucleotide": items[0],
	 "is_in_gene": items[1] == "1"}

for ntuple in windowed_iter(map(split_input_line, fileinput.input()), window_backward + 1 + window_forward):
	ntuple_backward = ntuple[0:window_backward]
	current_item = ntuple[window_backward]
	ntuple_forward = ntuple[window_backward + 1:]
	
	# The previous nucleotide is not in gene and the current one is
	is_at_beginning = (not ntuple_backward[-1]["is_in_gene"]) and current_item["is_in_gene"]
	
	# The previous nucleotide is in gene and the current one is not
	is_at_end = (not current_item["is_in_gene"]) and ntuple_backward[-1]["is_in_gene"]
	
	# TODO distance from nearest beginning, distance from nearest end, …
	
	
	print(format_bool(is_at_beginning) + "\t" + "\t".join(map(lambda x: x["nucleotide"], ntuple)))









