import os

def load_manuals():
    base_path = "data/manuals/"
    texts = []

    for file in os.listdir(base_path):
        with open(os.path.join(base_path, file), "r") as f:
            texts.append(f.read())

    return "\n".join(texts)