.PHONY: clean
CHROMOSOME = NC_000001.11

chromosome-1-positive: NC_000001.11 select-strand.py
	./select-strand.py 0 < $< > $@ 2>/dev/null

chromosome-1-negative: NC_000001.11 select-strand.py
	./select-strand.py 1 < $< > $@ 2>/dev/null


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

clean:
	rm -f ending-triplets.txt after-end-triplets.txt starting-triplets.txt before-start-triplets.txt histogram-data.txt triplet-histogram.png
	rm -f chromosome-1-positive chromosome-1-negative





