#!/usr/bin/python

# Reads a strand from select-strand.py and outputs only lines that are close enough to a positive example (begin or end).
# Also converts the boolean "is-in-gene" value to Begin-End-Neither three-level enum.
# Be aware that if the input strand ends with a is-in-gene chromosome, no gene-end example is produced.

import sys
import fileinput
from collections import deque

# Include this many items before gene start
window_size_left = 30
# Include this many items after gene end
window_size_right = 30


def format_begin_end(begin, end):
	"""Takes two bools – whether the item is at the beginning and at the end of a gene – and returns the correct formatted response value."""
	if begin and not end:
		return "B"
	elif end and not begin:
		return "E"
	elif not begin and not end:
		return "N"
	else:
		raise Exception("A gene cannot begin and end at the same position.")

def print_item(item):
	"""Format an item and print it to stdout."""
	print("%s\t%s" % (item['nucleotide'], item['response_value']))

def split_input_line(line):
	"""Takes a line with a single nucleotide, returns a hashtable with the parsed data."""
	items = line.rstrip().split("\t")
	return {"nucleotide": items[0],
	 "is_in_gene": items[1] == "1"}

def writeout_deque(deq):
	"""Print all items in the deque to stdout and clear it."""
	for item in deq:
		print_item(item)
	deq.clear()



# The history of items. Old ones are automatically discarded
window = deque([], window_size_left)
time_since_last_positive = window_size_right + 2

last_item = {"is_in_gene": False} # A dummy item to ensure that genes beginning at the start are printed.

for item in map(split_input_line, fileinput.input()):
	# The previous nucleotide is not in gene and the current one is
	is_at_beginning = item["is_in_gene"] and not last_item["is_in_gene"]
	
	# The previous nucleotide is in gene and the current one is not
	is_at_end = (not item["is_in_gene"]) and last_item["is_in_gene"]
	
	# Add the formatted response value to the item
	item['response_value'] = format_begin_end(is_at_beginning, is_at_end)
	
	# We have scored a hit! Write the unwritten history.
	if is_at_beginning or is_at_end:
		time_since_last_positive = 0
		writeout_deque(window)
	
	# We are close to a previous hit, so let's print the current item
	if time_since_last_positive <= window_size_right:
		time_since_last_positive += 1
		print_item(item)
	elif time_since_last_positive == window_size_right + 1:
		# A block around the hit has just ended. Print an empty line to signify this.
		# FIXME what if another block starts before the window overfills? Maybe the empty line shouldn't be there in that case.
		time_since_last_positive += 1
		window.append(item)
		print()
	else:
		# We haven't scored a hit in a long time. Just save the item to history.
		window.append(item)
	
	last_item = item
