
import transformers
import pandas as pd
import json
import os
import re
import numpy as np
import transformers
import argparse
from brat2dict import brat2dicts

def txt2subwords(text, tokenizer = 'dmis-lab/biobert-base-cased-v1.2'):
    "Convert the text to bert subwords"

    tokenizer = transformers.BertTokenizer.from_pretrained(tok)
    raw_tokens = tokenizer.tokenize(text)
    tokens = [token[2:] if token.startswith("##") else token for token in raw_tokens]
    idx = 0
    tk_wloc = []
    for token in tokens:
        start_idx = text[idx:].lower().find(token.lower()) + idx
        end_idx = start_idx + len(token) - 1
        tk_wloc.append([token,start_idx, end_idx + 1])
        idx = end_idx + 1
    print("number of tokens: ", len(tokens))
    return tk_wloc






def brat_to_iob(tokens, anno_terms):
    """
    mapping annotation terms to tokens
    Anno_term:start_index, end_index, label, text
    tokens: subword, start, end
    """
    terms = sorted(anno_terms, key=lambda x: x[0])
    tokens_bio = [[i[0],i[1],i[2],"0"] for i in tokens]
    for term in terms:
        inside = False
        for i, token in enumerate(tokens_bio):
            if token[1] >= term[0] and token[2]  <= term[1]:
                if not inside:
                    tokens_bio[i][3] = "B-" + term[2]
                    inside = True
                else:
                    tokens_bio[i][3] = "I-" + term[2]
            elif inside and (token[1] >= term[1] or i == len(tokens_bio) - 1):
                inside = False
    return tokens_bio

if __name__ == "__main__":
    description_text = '''Converting brat to bert IOB format.
    Default tokenizer is dmis-lab/biobert-base-cased-v1.2.
    Output files are saved in corpus_v2_mine/anno_df, and aggregated in 
    corpus_v2_mine/token_annotation_aggregated.csv.'''

    parser = argparse.ArgumentParser(description=description_text)

    anno_dir_help = 'Directory of brat annotations with both txt and ann files.'
    parser.add_argument('--anno_dir', type=str, help=anno_dir_help)

    tokenizer_help = 'Tokenizer to use. Default is dmis-lab/biobert-base-cased-v1.2.'
    parser.add_argument("--tokenizer",
                        type=str,
                        default="dmis-lab/biobert-base-cased-v1.2",
                        help=tokenizer_help)

    args = parser.parse_args()

    anno_dir = args.anno_dir
    tok = args.tokenizer
    print("using tokenizer: ", tok)

    anno_df_dir = 'anno_df'
    if not os.path.exists(os.path.join(anno_dir,anno_df_dir)):
        os.makedirs(os.path.join(anno_dir,anno_df_dir))
    pmcids = [f.split(".")[0] for f in os.listdir(anno_dir) if f.endswith(".ann")]

    all_token_anno = pd.DataFrame()
    for pmcid in pmcids:
        print("--------------processing: ", pmcid)
        ann_file = os.path.join(anno_dir,pmcid + ".ann")
        text_file = os.path.join(anno_dir,pmcid + ".txt")

        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()

        anno_terms,anno_rel,anno_attr,anno_star = brat2dicts(ann_file)
        tokens= txt2subwords(text,tok)
        token_anno = brat_to_iob(tokens, anno_terms)

        anno_df = pd.DataFrame(token_anno, columns=["token", "start", "end", "label"])
        anno_df.to_csv(os.path.join(anno_dir,anno_df_dir, pmcid +".csv"),index = False)
        # put things in an aggregated df
        anno_df["pmcid"] = pmcid
        all_token_anno = pd.concat([all_token_anno, anno_df], ignore_index=True)
    all_token_anno.to_csv(os.path.join(anno_dir, "token_annotation_aggregated.csv"), index=False)

