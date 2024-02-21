## How to run
1. put all data in the data folder. the files should be paired .txt and .ann files. in the same flat directory
2. run the code. Some warnings can be ignored.

    ```sh
    cd brat2bert
    bash run.sh data/example/BioNLP-ST_2011_EPI
    ```
3. see the output in the output directory.


_this is a very inefficient code. but it works_
# Scripts
Files in `tools/` and `servers/` are copied directly from the brat repository. 
Script `anntoconll.py` was revised for better error handling.

