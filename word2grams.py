def get_word_ngrams(text, k):
    words = text.lower().split()
    shingles = set()

    for i in range(len(words) - k + 1):
        shingles.add(" ".join(words[i:i + k]))

    return shingles


files = ["D1.txt", "D2.txt", "D3.txt", "D4.txt"]

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()

    shingles = get_word_ngrams(text, 2)

    print("\n" + "=" * 50)
    print("Document:", file_name)
    print("Total unique word 2-grams:", len(shingles))
    print(sorted(shingles))
