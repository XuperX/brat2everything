## for all .conll files in a directory, convert to .csv by a header in each file, and write the new files to the same directory as a csv file.

import os
import argparse

argparser = argparse.ArgumentParser(description='Convert conll files to csv files.')
argparser.add_argument('--input_dir', type=str, help='Directory of conll files.')

args = argparser.parse_args()

input_dir = args.input_dir
cnll_files = [f for f in os.listdir(input_dir) if f.endswith(".conll")]
for f in cnll_files:
    f_csv_name = f.split(".")[0]+".csv"
    with open(os.path.join(input_dir,f), 'r', encoding='utf-8') as f:
        conll_content = f.read()
    with open(os.path.join(input_dir,f_csv_name), 'w', encoding='utf-8') as f:
        f.write("labels\tstart\tend\twords\n")
        f.write(conll_content)
