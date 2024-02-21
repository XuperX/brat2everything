dir="/Users/user/Dropbox (The University of Manchester)/myPhD_code/20231213_corpus_v3/data/corpus_v3"

# Usoe find command to locate files matching the pattern
for f in $dir/PMC*.txt; do
    python anntoconll.py "$f"
done

