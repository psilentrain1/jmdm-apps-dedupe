### JMDM Dedupe

A program to search recursively through a directory to find duplicate files.

(Only tested on UNIX based systems so far. Windows testing to come.)

#### Using JMDM Dedupe

Run JMDM:

```
python dedupe.py
```

When prompted, enter the directory to search.
For example:

```
/Users/username/Documents/Images
```

The program will scan all the files in the root directory and subdirectories and save a file called `duplicated_hash_list.csv` into the root directory. The CSV file contains the paths and MD5 hashes of all suspected duplicate files.

#### Building JMDM Dedupe

`TODO`
