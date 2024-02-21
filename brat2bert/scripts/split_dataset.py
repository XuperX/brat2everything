#!/usr/bin/env python
# coding: utf-8

# this script is stupid but it works. does a very simple thing, split the dataset into train, test and dev sets. and generate a combined train/dev/test file in the output dir
# updates 20240118: make it cli-friendly, fix the problem of int(a)+int(b) != int(a+b), and move files by pmc id instead of all ann files.


import os
import random 
import shutil
import argparse
import pandas as pd
import glob
import os

def argparser():
    description_text = '''Split the dataset into train, test and dev sets.
    Output files are saved in bertTraining_dataset/v3/train, bertTraining_dataset/v3/test, and bertTraining_dataset/v3/dev.'''
    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument('--dir', type=str, help='Directory of brat annotations with both txt and ann files.')
    parser.add_argument('--train_ratio', type=float, default=0.7, help='ratio of train set')
    parser.add_argument('--test_ratio', type=float, default=0.2, help='ratio of test set')
    parser.add_argument('--dev_ratio', type=float, default=0.1, help='ratio of dev set')
    parser.add_argument('--seed', type=int, default=10, help='random seed for deviding the dataset.')
    args = parser.parse_args()
    return args

args = argparser()
original_dir = args.dir
train_dir = os.path.join(original_dir, "train")
test_dir = os.path.join(original_dir, "test")
dev_dir = os.path.join(original_dir, "dev")

train_ratio = args.train_ratio
test_ratio = args.test_ratio
dev_ratio = args.dev_ratio
random.seed(args.seed)

def create_dir(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
create_dir(train_dir)
create_dir(test_dir)
create_dir(dev_dir)

# in the data generation pipeline, the files show in the order txt > ann > conll > csv
# ideally i need to check the valid pmcs are only the ones with all four files, but alternatively, i can just check if the csv file presents.
# but because the use of csv is so ubiquitous, i will just check if the conll instead.
all_pmc = [f.split(".")[0] for f in os.listdir(original_dir) if f.endswith(".conll")]

random.seed(args.seed)
random.shuffle(all_pmc)

train_len = int(len(all_pmc) * train_ratio)
test_len = int(len(all_pmc) * test_ratio)

train_pmc = all_pmc[:train_len]
test_pmc = all_pmc[train_len:train_len+test_len]
dev_pmc = all_pmc[train_len+test_len:]


# In[15]:

def move_files(pmcs, target_directory,src_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    for f in pmcs:
        try:
            shutil.move(os.path.join(src_directory, f+".txt"), os.path.join(target_directory, f+".txt"))
            shutil.move(os.path.join(src_directory, f + ".ann"),
                        os.path.join(target_directory, f + ".ann"))
            shutil.move(os.path.join(src_directory, f + ".csv"),
                        os.path.join(target_directory, f + ".csv"))
            shutil.move(os.path.join(src_directory, f + "_sent.csv"),
                        os.path.join(target_directory, f + "_sent.csv"))
            shutil.move(os.path.join(src_directory, f + ".conll"),
                        os.path.join(target_directory, f + ".conll"))
        except:
            print("Error moving files for " + f)
# Move files to respective directories
move_files(train_pmc, train_dir, original_dir)
move_files(test_pmc, test_dir,original_dir)
move_files(dev_pmc, dev_dir,original_dir)

leftover_files = [f for f in os.listdir(original_dir) if f.endswith(".ann")]
print("###############\n ###############\n  WARNING:," + str(len(leftover_files)) + " files are not moved to any directory \n. ###############\n  They are: " + ", ".join(leftover_files))

subdirs = [train_dir, test_dir, dev_dir]
output_dir = "output/"+ original_dir.split("/")[-1]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for subdir in subdirs:
    all_files = glob.glob(os.path.join(subdir, "*_sent.csv"))
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
    print(subdir.split("/")[-1])
    concatenated_df.to_csv(os.path.join(output_dir, subdir.split("/")[-1]+ ".csv"), index=False)

