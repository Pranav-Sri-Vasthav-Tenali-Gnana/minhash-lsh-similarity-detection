import random
from itertools import combinations
from collections import defaultdict

DATA_FILE = "u.data"
PRIME = 10007
NUM_RUNS = 5

LSH_CONFIGS = [
    (50, 5, 10),
    (100, 5, 20),
    (200, 5, 40),
    (200, 10, 20),
]

THRESHOLDS = [0.6, 0.8]


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


def generate_hash_functions(num_hashes, seed):
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
    hash_functions = generate_hash_functions(num_hashes, seed)
    signatures = {}

    for user, movies in user_movies.items():
        sig = []
        for a, b in hash_functions:
            min_hash = min(((a * movie + b) % PRIME) for movie in movies)
            sig.append(min_hash)
        signatures[user] = sig

    return signatures


def lsh_candidate_pairs(signatures, rows_per_band, num_bands):
    users = sorted(signatures.keys())
    candidate_pairs = set()

    for band in range(num_bands):
        buckets = defaultdict(list)
        start = band * rows_per_band
        end = start + rows_per_band

        for user in users:
            band_tuple = tuple(signatures[user][start:end])
            buckets[band_tuple].append(user)

        for bucket_users in buckets.values():
            if len(bucket_users) > 1:
                for u1, u2 in combinations(sorted(bucket_users), 2):
                    candidate_pairs.add((u1, u2))

    return candidate_pairs


def evaluate_pairs(exact_pairs, candidate_pairs):
    false_positives = len(candidate_pairs - exact_pairs)
    false_negatives = len(exact_pairs - candidate_pairs)
    return false_positives, false_negatives


def main():
    user_movies = load_user_movie_sets(DATA_FILE)

    print("=" * 80)
    print("Q5 - LSH ON MOVIELENS DATASET")
    print("=" * 80)
    print(f"Users loaded: {len(user_movies)}")
    print(f"Runs per configuration: {NUM_RUNS}")

    for threshold in THRESHOLDS:
        print("\n" + "=" * 80)
        print(f"SIMILARITY THRESHOLD = {threshold}")
        print("=" * 80)

        exact_pairs = compute_exact_pairs(user_movies, threshold)
        print(f"Exact pairs with similarity >= {threshold}: {len(exact_pairs)}")

        for num_hashes, r, b in LSH_CONFIGS:
            print("\n" + "-" * 80)
            print(f"Configuration: hashes={num_hashes}, r={r}, b={b}")
            print("-" * 80)

            fp_list = []
            fn_list = []

            for run in range(1, NUM_RUNS + 1):
                signatures = compute_minhash_signatures(user_movies, num_hashes, seed=run)
                candidate_pairs = lsh_candidate_pairs(signatures, r, b)
                fp, fn = evaluate_pairs(exact_pairs, candidate_pairs)

                fp_list.append(fp)
                fn_list.append(fn)

                print(f"Run {run}:")
                print(f"Candidate pairs: {len(candidate_pairs)}")
                print(f"False Positives: {fp}")
                print(f"False Negatives: {fn}")

            avg_fp = sum(fp_list) / NUM_RUNS
            avg_fn = sum(fn_list) / NUM_RUNS

            print(f"\nAverage False Positives: {avg_fp:.2f}")
            print(f"Average False Negatives: {avg_fn:.2f}")


if __name__ == "__main__":
    main()
