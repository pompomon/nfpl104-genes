#!/usr/bin/python

# This prints chromosome strand "left" or "right", depending on the argument.
# Usage: select-strand.py {0 | 1} < chromosome > single-strand
# Prints Nucleotide tab In-gene-mark
#  where Nucleotide is one of [ACGT] or X for other input letters
#  and In-gene-mark is 0 or 1

import sys
import re
from tempfile import TemporaryDirectory, NamedTemporaryFile


# When reversing the file, read only this many triplets into memory at once
length_limit = 1024*1024*32; # Requires approximately 2.5 GiB of memory. Adjust the limit as needed

# A pattern for recognizing correct triplets
triplet_regex = re.compile(r"\A[ACGTBKMNRWY][01][01]\Z")
#triplet_regex = re.compile(r"\A[ACGTN][01][01]\Z")

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
	
	# TODO what to do about these?
	'B': 'X',
	'K': 'X',
	'M': 'X',
	'N': 'X',
	'R': 'X',
	'W': 'X',
	'Y': 'X'
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




# Read the triplets.
if selected_strand == 0:
	# Positive strand was selected. Simply extract the right in-genome mark and print
	for triplet in triplets(sys.stdin):
		sys.stdout.write(triplet[0] + "\t" + triplet[1] + "\n")
else:
	# Negative strand was selected. We have to reverse the strand and mirror the nucleotides.
	# Reversing is done in chunks – the input might be very large, so we reverse it a chunk at a time,
	#  storing the partial results in a temporary directory. Then, these tempfiles are concatenated in
	#  reverse order; thus completing the reversal.
	
	# Create a new temporary directory that will hold our tempfiles
	with TemporaryDirectory(prefix = "revstrand") as tmpdirname:
		genome_to_reverse = []
		temp_file_names = []
		for triplet in triplets(sys.stdin):
			# Negative strand → mirror the nucleotide and store before reversing and printing
			genome_to_reverse.append(mirror_nucleotide(triplet[0]) + "\t" + triplet[2] + "\n");
			
			# We have overfilled the buffer
			if (len(genome_to_reverse) > length_limit):
				# Write the current buffer into a tempfile
				with NamedTemporaryFile(dir = tmpdirname, mode = "w+t", delete = False) as tmpfile:
					print("Writing the genome to file %s" % tmpfile.name, file = sys.stderr)
					tmpfile.write("".join(reversed(genome_to_reverse)))
					temp_file_names.append(tmpfile.name)
				
				genome_to_reverse = []
		
		
		# There might be an unprinted part in genome_to_reverse. Print that first.
		for dublet in reversed(genome_to_reverse):
			sys.stdout.write(dublet)
		del(genome_to_reverse)
		
		# Each of the files in temp_file_names now holds a reversed portion of the whole strand.
		# Concatenate them together
		for name in reversed(temp_file_names):
			with open(name, "rt") as tmpfile:
				sys.stdout.write(tmpfile.read())

