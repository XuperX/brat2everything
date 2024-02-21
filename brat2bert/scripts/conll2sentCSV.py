# for each train file, combine the token based annotations to sentence level annotations. also create an aggregated csv file.

import pandas as pd
import os
import argparse
import re

def load_data(data_file):
    # Read the data file with the specified column names
    raw_data = pd.read_csv(data_file, sep="\\t", skip_blank_lines=False)
    return raw_data


def words2sentences(df):
    df['words'].replace('', pd.NA, inplace=True)
    df['labels'].replace('', pd.NA, inplace=True)

    # Identify the indices of empty rows which mark the end of sentences
    sentence_end_indices = df[df['words'].isna()].index

    sentences = []
    labels = []

    # Initialize the start index of the first sentence
    start_idx = 0

    # Iterate over the end indices and slice the DataFrame to create sentences
    for end_idx in sentence_end_indices:
        current_sentence = df.loc[start_idx:end_idx - 1, 'words'].tolist()
        current_labels = df.loc[start_idx:end_idx - 1, 'labels'].tolist()
        sentences.append(current_sentence)
        labels.append(current_labels)
        start_idx = end_idx + 1
    # if no empty row at the end of DF
    if start_idx < len(df):
        sentences.append(df.loc[start_idx:, 'words'].tolist())
        labels.append(df.loc[start_idx:, 'labels'].tolist())

    sentence_df = pd.DataFrame({
        # todo this might be wrong
        'words': sentences,
        'labels': labels
    })

    # sentence_df["words] = sentence_df["words"].apply(lambda x: ast.literal_eval(x))
    # sentence_df["labels"] = sentence_df["labels"].apply(lambda x: ast.literal_eval(x))

    # sentence_df.to_csv("bertTraining_dataset/train_3files_sentences.csv")
    # input()
    return sentence_df

parser = argparse.ArgumentParser(description="Process a directory or a file.")

# Create a mutually exclusive group
group = parser.add_mutually_exclusive_group(required=True)

# Add arguments to the group
group.add_argument('-d', '--directory', type=str, help='Directory to process')
group.add_argument('-f', '--file', type=str, help='File to process')

# Parse the arguments
args = parser.parse_args()

if args.directory:
    print("move to dir")
    target_dir = args.directory
    target_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith('.csv') and not f.endswith('_sent.csv')]
    for target_file in target_files:
        print(target_file)
        all_data = pd.DataFrame()
        data = load_data(target_file)
        sentence_df = words2sentences(data)
        print("number of words: " + str(len(sentence_df)))
        all_data = all_data.append(sentence_df)
        all_data.to_csv(target_file.split(".")[0] + "_sent.csv", index=False)

if args.file:
    target_file = args.file
    print(target_file)
    all_data = pd.DataFrame()
    data = load_data(target_file)
    sentence_df = words2sentences(data)
    print("number of words: " + str(len(sentence_df)))
    all_data = all_data.append(sentence_df)
    all_data.to_csv(target_file.split(".")[0] + "_sent.csv", index=False)
