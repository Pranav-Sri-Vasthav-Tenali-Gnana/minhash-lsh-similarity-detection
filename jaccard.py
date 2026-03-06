from itertools import combinations

def get_char_ngrams(text, k):
    text = text.lower()
    return set(text[i:i + k] for i in range(len(text) - k + 1))

def get_word_ngrams(text, k):
    words = text.lower().split()
    return set(" ".join(words[i:i + k]) for i in range(len(words) - k + 1))

def jaccard_similarity(set1, set2):
    union = len(set1 | set2)
    if union == 0:
        return 0.0
    intersection = len(set1 & set2)
    return intersection / union

files = ["D1.txt", "D2.txt", "D3.txt", "D4.txt"]
docs = {}

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as f:
        docs[file_name] = f.read()

char2 = {name: get_char_ngrams(text, 2) for name, text in docs.items()}
char3 = {name: get_char_ngrams(text, 3) for name, text in docs.items()}
word2 = {name: get_word_ngrams(text, 2) for name, text in docs.items()}

pairs = list(combinations(files, 2))

print("Character 2-grams")
for a, b in pairs:
    print(f"{a}-{b} = {jaccard_similarity(char2[a], char2[b]):.6f}")

print("\nCharacter 3-grams")
for a, b in pairs:
    print(f"{a}-{b} = {jaccard_similarity(char3[a], char3[b]):.6f}")

print("\nWord 2-grams")
for a, b in pairs:
    print(f"{a}-{b} = {jaccard_similarity(word2[a], word2[b]):.6f}")
