# Near-Duplicate Detection with MinHash and LSH

From-scratch Python implementations of **Jaccard similarity**, **MinHash signatures** and **Locality-Sensitive Hashing (LSH)**, used first on small text documents and then to find similar users in the **MovieLens 100K** dataset without comparing every pair.

**Stack:** Python (standard library only: `itertools`, `collections`, `random`)

## What's in the repo

| File | What it does |
|---|---|
| `jaccard.py` | Compares four small documents (`minhash/D1.txt` … `D4.txt`) by exact Jaccard similarity over **character 2-grams, character 3-grams and word 2-grams** (`char2grams.py`, `char3grams.py`, `word2grams.py` hold the shingling helpers). |
| `jaccard_a.py` | Estimates the same similarities with **MinHash** for several signature lengths `t` and prints the approximation next to the exact value. |
| `movielens.py` | Loads MovieLens 100K (`minhash/u.data`), represents each user as the **set of movies they rated**, finds the exact pairs with Jaccard similarity ≥ 0.5, then estimates similarity with MinHash signatures of 50, 100 and 200 hash functions over 5 runs. |
| `movielens_lsh.py` | Adds **banded LSH** on top of the signatures and measures its quality against the exact answer. |

## How it works

1. **Shingling / sets:** every document or user becomes a set (character n-grams, word n-grams, or rated movies).
2. **Exact baseline:** all user pairs are compared with Jaccard similarity, which is correct but quadratic in the number of users.
3. **MinHash:** each set is compressed into a short signature using random hash functions of the form `(a·x + b) mod p` (p = 10007). The chance that two signatures agree at a position equals the Jaccard similarity of the sets.
4. **LSH banding:** the signature is split into `b` bands of `r` rows. Two users become a candidate pair if any band hashes to the same bucket, so only candidates need to be checked.
5. **Evaluation:** for each configuration the script compares LSH candidates with the exact pairs and reports **false positives** and **false negatives**, averaged over 5 runs with different random seeds.

Configurations tried (number of hash functions, rows per band, bands): `(50, 5, 10)`, `(100, 5, 20)`, `(200, 5, 40)` and `(200, 10, 20)`, at similarity thresholds **0.6** and **0.8**.

## Run it

```bash
cd minhash
python ../jaccard.py            # exact document similarity with n-gram shingles
python ../jaccard_a.py          # MinHash approximation of the same similarities
python ../movielens.py          # MinHash on MovieLens 100K
python ../movielens_lsh.py      # LSH banding + false positive / negative analysis
```

(The scripts read `u.data` and `D1.txt`–`D4.txt` from the working directory, so run them from the `minhash/` folder.)

## What I took from it

- More hash functions make MinHash estimates closer to the true Jaccard similarity.
- More bands with fewer rows raise recall (fewer false negatives) at the price of more candidate pairs (more false positives). The `(r, b)` choice sets the similarity "S-curve" of the filter, so it has to be tuned to the threshold you care about.
