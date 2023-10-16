from sentence_transformers import SentenceTransformer
import os
import re

# Load the pre-trained model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def read_sentences_from_files(path):
    """
    Reads sentences from all .srt, .sub, and .txt files in the given directory and its subdirectories.
    Returns a list of (filename, sentence) pairs.
    """
    all_sentences = []  # Renamed to all_sentences to avoid naming conflict
    file_count = 0
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(('.srt', '.sub', '.txt')):
                file_count += 1
                file_path = os.path.join(root, file)
                print(f"Processing file {file_count}: {file_path}")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Split content into sentences based on common delimiters
                    for sentence in re.split(r'[.!?]', content):
                        all_sentences.append((file, sentence.strip()))  # Store filename along with the sentence
    return all_sentences


def obtain_embeddings(path):
    """
    Reads sentences from files in the given directory, obtains embeddings for each sentence,
    and returns a list of embeddings.
    """
    sentences = read_sentences_from_files(path)
    print(f"Total sentences found: {len(sentences)}")
    print("Encoding sentences to obtain embeddings...")
    embeddings = model.encode(sentences)
    print("Embeddings obtained successfully!")
    return embeddings
