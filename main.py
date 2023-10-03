import numpy as np
from Cleaner import unzip_files, process_files, clean_subtitles, unzip_single_file, remove_numbers_from_files
from embedding import obtain_embeddings, read_sentences_from_files
from similarity_computation import find_most_similar_sentences


def main():
    Path = r'C:\Users\Baran\OneDrive\Bureau\SAE5\sous-titres'

    # Load the embeddings
    print("Loading embeddings from 'sentence_embeddings.npy'...")
    loaded_embeddings = np.load('sentence_embeddings.npy') # le fichier avec les embeddings
    print(f"Loaded {len(loaded_embeddings)} embeddings successfully!")

    # Load the sentences
    print("\nLoading sentences from the dataset...")
    sentences = read_sentences_from_files(Path)
    print(f"Loaded {len(sentences)} sentences from the dataset.")

    # Example query
    query_sentence = "Enter your query sentence here"
    print(f"\nQuery Sentence: {query_sentence}")

    # Find the most similar sentences to the query
    print("\nComputing similarity scores for the query sentence...")
    top_similar_sentences = find_most_similar_sentences(query_sentence, loaded_embeddings, sentences, top_n=5)

    # Print the results
    print(f"\nTop 5 most similar sentences to the query '{query_sentence}':")
    for i, (sentence, score) in enumerate(top_similar_sentences, 1):
        print(f"{i}. {sentence.strip()} (Similarity Score: {score:.4f})")


if __name__ == '__main__':
    main()
