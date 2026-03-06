import random
from itertools import combinations
from collections import defaultdict

DATA_FILE = "u.data"   # keep u.data in same folder
THRESHOLD = 0.5
NUM_RUNS = 5
HASH_COUNTS = [50, 100, 200]
PRIME = 10007  # > 10000

def load_user_movie_sets(file_path):
    user_movies = defaultdict(set)

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            user_id, movie_id, rating, timestamp = line.strip().split("\t")
            user_id = int(user_id)
            movie_id = int(movie_id)
            user_movies[user_id].add(movie_id)

    return dict(user_movies)

def jaccard_similarity(set1, set2):
    union = len(set1 | set2)
    if union == 0:
        return 0.0
    return len(set1 & set2) / union

def compute_exact_pairs(user_movies, threshold):
    users = sorted(user_movies.keys())
    exact_pairs = set()

    for u1, u2 in combinations(users, 2):
        sim = jaccard_similarity(user_movies[u1], user_movies[u2])
        if sim >= threshold:
            exact_pairs.add((u1, u2))

    return exact_pairs

def generate_hash_functions(num_hashes, max_movie_id, seed):
    random.seed(seed)
    hash_functions = []
    used = set()

    while len(hash_functions) < num_hashes:
        a = random.randint(1, PRIME - 1)
        b = random.randint(0, PRIME - 1)
        if (a, b) not in used:
            used.add((a, b))
            hash_functions.append((a, b))

    return hash_functions

def compute_minhash_signatures(user_movies, num_hashes, seed):
    max_movie_id = max(movie for movies in user_movies.values() for movie in movies)
    hash_functions = generate_hash_functions(num_hashes, max_movie_id, seed)

    signatures = {}
    for user, movies in user_movies.items():
        sig = []
        for a, b in hash_functions:
            min_hash = min(((a * movie + b) % PRIME) for movie in movies)
            sig.append(min_hash)
        signatures[user] = sig

    return signatures

def estimated_similarity(sig1, sig2):
    matches = sum(1 for x, y in zip(sig1, sig2) if x == y)
    return matches / len(sig1)

def compute_estimated_pairs(signatures, threshold):
    users = sorted(signatures.keys())
    estimated_pairs = set()

    for u1, u2 in combinations(users, 2):
        sim = estimated_similarity(signatures[u1], signatures[u2])
        if sim >= threshold:
            estimated_pairs.add((u1, u2))

    return estimated_pairs

def evaluate_pairs(exact_pairs, estimated_pairs):
    false_positives = len(estimated_pairs - exact_pairs)
    false_negatives = len(exact_pairs - estimated_pairs)
    return false_positives, false_negatives

def main():
    user_movies = load_user_movie_sets(DATA_FILE)

    print("=" * 70)
    print("LOADED DATA")
    print("=" * 70)
    print(f"Number of users: {len(user_movies)}")
    print(f"Threshold: {THRESHOLD}")

    print("\n" + "=" * 70)
    print("EXACT JACCARD PAIRS (similarity >= 0.5)")
    print("=" * 70)
    exact_pairs = compute_exact_pairs(user_movies, THRESHOLD)
    print(f"Total exact pairs with similarity >= {THRESHOLD}: {len(exact_pairs)}")
    for pair in sorted(exact_pairs):
        print(pair)

    print("\n" + "=" * 70)
    print("MINHASH EXPERIMENTS")
    print("=" * 70)

    for num_hashes in HASH_COUNTS:
        print(f"\nUsing {num_hashes} hash functions")
        fp_list = []
        fn_list = []

        for run in range(1, NUM_RUNS + 1):
            signatures = compute_minhash_signatures(user_movies, num_hashes, seed=run)
            estimated_pairs = compute_estimated_pairs(signatures, THRESHOLD)
            fp, fn = evaluate_pairs(exact_pairs, estimated_pairs)

            fp_list.append(fp)
            fn_list.append(fn)

            print(f"\nRun {run}")
            print(f"Estimated pairs with similarity >= {THRESHOLD}: {len(estimated_pairs)}")
            print("Pairs:")
            for pair in sorted(estimated_pairs):
                print(pair)
            print(f"False Positives: {fp}")
            print(f"False Negatives: {fn}")

        avg_fp = sum(fp_list) / NUM_RUNS
        avg_fn = sum(fn_list) / NUM_RUNS

        print(f"\nAverage False Positives for {num_hashes} hashes: {avg_fp:.2f}")
        print(f"Average False Negatives for {num_hashes} hashes: {avg_fn:.2f}")

if __name__ == "__main__":
    main()
