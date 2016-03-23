#!/usr/bin/python

# This prints chromosome strand "left" or "right", depending on the argument.
# Usage: select-strand.py {0 | 1} < chromosome > single-strand

import sys
import re

# A pattern for recognizing correct triplets
triplet_regex = re.compile(r"\A[ACGT][01][01]\Z")

# Iterates over three-letter chunks from infile and returns correct nucleotide-triplets.
#  Incorrect triplets are ignored.
# There mustn't be any whitespace in the file, except for possibly trailing whitespace, which is stripped
def triplets(infile):
	triplet = infile.read(3)
	while len(triplet) == 3:
		if not triplet_regex.match(triplet):
			sys.stderr.write("Incorrect triplet: '" + triplet + "'\n")
			triplet = infile.read(3)
			continue
		
		yield triplet
		triplet = infile.read(3)
	
	triplet = triplet.rstrip()
	if (len(triplet) != 0) and (len(triplet) != 3):
		sys.stderr.write("Partial triplet read: '" + triplet + "' of length " + str(len(triplet)) + "\n")
		return



# A mirroring table for nucleotides
nucl_mirror = {
	'A': 'T',
	'T': 'A',
	'C': 'G',
	'G': 'C',
}

# Returns a mirrored nucleotide; e.g. A->T  T->A  C->G  G->C
def mirror_nucleotide(letter):
	return nucl_mirror[letter]


usage = ("Incorrect arguments.\nUsage:\t" + sys.argv[0] + " {0 | 1}\n"
	 + "\tSelects left (0) or right (1) strand of DNA code read from stdin.\n")







# Check the arguments and fill in the selected strand.
if len(sys.argv) == 2:
	if sys.argv[1] == "0":
		selected_strand = 0
	elif sys.argv[1] == "1":
		selected_strand = 1
	else:
		sys.exit(usage)
else:
	sys.exit(usage)



genome_to_reverse = [];

# Read the triplets.
for triplet in triplets(sys.stdin):
	if selected_strand == 0:
		sys.stdout.write(triplet[0] + "\t" + triplet[1] + "\n")
	else:
		# Negative strand → mirror the nucleotide and reverse the whole
		genome_to_reverse.append(mirror_nucleotide(triplet[0]) + "\t" + triplet[2] + "\n");


# If we selected the negative strand, reverse the output.
if selected_strand == 1:
	for dublet in reversed(genome_to_reverse):
		sys.stdout.write(dublet)
