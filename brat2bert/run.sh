#!/usr/bin/env bash

data_dir="$1"
# ann to conll files
for f in $data_dir/*.txt;
 do python scripts/tools/anntoconll.py $f;
done
# convert conll to csv (arranged by word)
python scripts/conll2csv.py --input_dir "$data_dir"
# combine all csv to sentence based csv files.
python scripts/conll2sentCSV.py -d "$data_dir"

# devide the dataset into train, dev, test and put them in the output directory.
python scripts/split_dataset.py --dir "$data_dir"



