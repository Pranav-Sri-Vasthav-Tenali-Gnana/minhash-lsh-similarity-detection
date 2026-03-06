import os

def get_char_ngrams(text, k):
    text = text.lower()
    shingles = set()

    for i in range(len(text) - k + 1):
        shingles.add(text[i:i + k])

    return shingles


base_path = os.getcwd()

files = ["D1.txt", "D2.txt", "D3.txt", "D4.txt"]
docs = {}

for file_name in files:
    file_path = os.path.join(base_path, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        docs[file_name] = f.read()

for file_name, text in docs.items():
    shingles = get_char_ngrams(text, 2)

    print("\n" + "=" * 50)
    print("Document:", file_name)
    print("Total unique character 2-grams:", len(shingles))
    print(sorted(shingles))
