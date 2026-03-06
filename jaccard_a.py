import random

def get_char_ngrams(text, k):
    text = text.lower()
    return set(text[i:i + k] for i in range(len(text) - k + 1))

def minhash_similarity(set1, set2, t, m=10007):
    all_shingles = list(set1 | set2)
    shingle_to_id = {shingle: idx for idx, shingle in enumerate(all_shingles)}

    ids1 = {shingle_to_id[s] for s in set1}
    ids2 = {shingle_to_id[s] for s in set2}

    random.seed(42)
    hash_functions = set()
    while len(hash_functions) < t:
        a = random.randint(1, m - 1)
        b = random.randint(0, m - 1)
        hash_functions.add((a, b))

    signature1 = []
    signature2 = []

    for a, b in hash_functions:
        min1 = min((a * x + b) % m for x in ids1)
        min2 = min((a * x + b) % m for x in ids2)
        signature1.append(min1)
        signature2.append(min2)

    matches = sum(1 for i in range(t) if signature1[i] == signature2[i])
    return matches / t

with open("D1.txt", "r", encoding="utf-8") as f:
    d1 = f.read()

with open("D2.txt", "r", encoding="utf-8") as f:
    d2 = f.read()

d1_3grams = get_char_ngrams(d1, 3)
d2_3grams = get_char_ngrams(d2, 3)

t_values = [20, 60, 150, 300, 600]

for t in t_values:
    approx_jaccard = minhash_similarity(d1_3grams, d2_3grams, t)
    print(f"t = {t} -> {approx_jaccard:.6f}")
