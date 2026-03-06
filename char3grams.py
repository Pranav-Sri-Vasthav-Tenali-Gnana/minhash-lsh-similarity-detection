import os

def get_char_ngrams(text, k):
    text = text.lower()
    shingles = set()

    for i in range(len(text) - k + 1):
        shingles.add(text[i:i + k])

    return shingles


files = ["D1.txt", "D2.txt", "D3.txt", "D4.txt"]

for file_name in files:
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()

    shingles = get_char_ngrams(text, 3)

    print("\n" + "=" * 50)
    print("Document:", file_name)
    print("Total unique character 3-grams:", len(shingles))
    print(sorted(shingles))
