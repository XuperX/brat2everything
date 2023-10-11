import argparse
import json
import os

def term2loc(tuples_list, key):
    # data = [(469, 473, 'Software', 'T1', 'Perl'), (487, 492, 'Software', 'T2', 'Linux')]
    # Given T1, return (469, 473)
    return next(((x[0], x[1]) for x in tuples_list if x[3] == key), None)

def brat2dicts(bratFile,path=""):
    terms, relationships, attributes, stars = [],[],[],[]
    with open(os.path.join(path,bratFile), 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if parts[0].startswith("T"):
                termid = parts[0]
                label = parts[1]
                start_offset = int(parts[2])
                end_offset = int(parts[3])
                term_text = " ".join(parts[4: ])
                terms.append((start_offset, end_offset, label,termid, term_text))
            if parts[0].startswith("A"):
                    attrid = parts[0]
                    label = parts[1]
                    attr_term = parts[2]
                    attr_start = term2loc(terms, attr_term)[0]
                    attr_end = term2loc(terms, attr_term)[1]
                    if len(parts) == 4:
                        label_value = parts[3]
                    if len(parts) == 3:
                        # for checkboxes
                        label_value = "True"
                    attributes.append((attr_start, attr_end, attrid, label, attr_term, label_value))
            if parts[0].startswith("R"):
                relid = parts[0]
                reltype = parts[1]
                rel_arg1 = parts[2].split(":")[1]
                rel_arg2 = parts[3].split(":")[1]
                arg1_start = term2loc(terms, rel_arg1)[0]
                arg1_end = term2loc(terms, rel_arg1)[1]
                arg2_start = term2loc(terms, rel_arg2)[0]
                arg2_end = term2loc(terms, rel_arg2)[1]
                relationships.append((arg1_start, arg1_end, arg2_start, arg2_end, relid, reltype, rel_arg1, rel_arg2))
            if parts[0].startswith("*"):
                starsType= parts[1]
                starsArg1 = parts[2]
                starsArg2 = parts[3]
                stars.append((starsType, starsArg1, starsArg2))
        return terms, relationships, attributes, stars

def process_file(anno_file, filepath = ""):
    header = anno_file.split(".")[0]
    anno_terms,anno_rel,anno_attr,anno_star = brat2dicts(anno_file,filepath)
    json.dump(anno_terms, open(os.path.join(filepath, header+ "_terms.json"), 'w'))
    json.dump(anno_rel, open(os.path.join(filepath, header+ "_rels.json"), 'w'))
    json.dump(anno_attr, open(os.path.join(filepath, header+ "_attrs.json"), 'w'))
    json.dump(anno_star, open(os.path.join(filepath, header+ "_stars.json"), 'w'))

if __name__ == "__main__":
    description = """Convert brat annotations to dictionaries, 
    and save entities, relationships, attributes, and starts(part of relationship)
    in seperate json files.
    Accept either a directory or a file."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--path", type=str, required=True, help="Path to a directory or a file.")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        for file in os.listdir(args.path):
            if file.endswith(".ann"):
                process_file(file, args.path)
    elif os.path.isfile(args.path):
        process_file(args.path)




