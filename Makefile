SHELL := /bin/bash

.PHONY: all clean
CHROMOSOME = NC_000001.11
# gene-short
#NC_000001.11

pompomon.tar.xz: test.tsv train.tsv
	tar -cf pompomon.tar $^
	xz -z9evv pompomon.tar



all: test.tsv train.tsv

# chromosome-1-positive: ${CHROMOSOME} select-strand.py window-filter.py make-features.py
# 	./select-strand.py 0 < $< | ./window-filter.py | ./make-features.py --header > $@
# 
# chromosome-1-negative: ${CHROMOSOME} select-strand.py window-filter.py make-features.py
# 	./select-strand.py 1 < $< | ./window-filter.py | ./make-features.py --header > $@

compressed-chromosomes.tsv: genome.tar.xz select-strand.py window-filter.py make-features.py
	tar -xOf $< |tee >(./select-strand.py 0 |./window-filter.py |./make-features.py) >(./select-strand.py 1 |./window-filter.py |./make-features.py) >/dev/null |cat > $@

gene-short: NC_000001.11
	head -c 90000000 $^ > $@


shuffled-chromosomes.tsv: compressed-chromosomes.tsv get-seeded-random.sh
	shuf --random-source=<(./get-seeded-random.sh 5345) $< |head -n 700000 > $@

test.tsv: shuffled-chromosomes.tsv
	# Take the first 1/8 of the shuffled file, add a header
	head -n $$(echo `wc -l < $<` / 8 |bc) $< |cat <(./make-features.py --header-only) - > $@

train.tsv: shuffled-chromosomes.tsv test.tsv
	# Take whatever is not in test.tsv
	head -n1 test.tsv > $@ # Copy the header
	tail -n +$$(echo `wc -l test.tsv |sed -e 's/ .*//'` + 1 |bc) $< >> $@


triplet-histogram.png: histogram-data.txt plot-triplet-histogram.gpl
	gnuplot plot-triplet-histogram.gpl > $@

ending-triplets.txt: ${CHROMOSOME}
	grep -o [ACTG]1..1..1..0. $^ |cut -c1,4,7 |sort |uniq -c |sort -rn > $@

after-end-triplets.txt: ${CHROMOSOME}
	grep -o [ACTG]1..0..0..0. $^ |cut -c4,7,10 |sort |uniq -c |sort -rn > $@

starting-triplets.txt: ${CHROMOSOME}
	grep -o [ACTG]0..1..1..1. $^ |cut -c4,7,10 |sort |uniq -c |sort -rn > $@

before-start-triplets.txt: ${CHROMOSOME}
	grep -o [ACTG]0..0..0..1. $^ |cut -c1,4,7 |sort |uniq -c |sort -rn > $@

histogram-data.txt: ending-triplets.txt after-end-triplets.txt starting-triplets.txt before-start-triplets.txt
	bash -c 'join -j2 -a1 -e0 -oauto <(sort -k2 before-start-triplets.txt) <(sort -k2 starting-triplets.txt) | join -11 -22 -a1 -e0 -oauto - <(sort -k2 ending-triplets.txt) | join -11 -22 -a1 -e0 -oauto - <(sort -k2 after-end-triplets.txt)' > $@


NC_000001.11: genome.tar.xz
	tar -xvf $< $@

genome.tar.xz:
	wget -O $@ http://jonys.cz/skola/npfl104/genes/genome.tar.xz


clean:
	rm -f ending-triplets.txt after-end-triplets.txt starting-triplets.txt before-start-triplets.txt histogram-data.txt triplet-histogram.png
	rm -f chromosome-1-positive chromosome-1-negative compressed-chromosomes.tsv shuffled-chromosomes.tsv gene-short test.tsv train.tsv





