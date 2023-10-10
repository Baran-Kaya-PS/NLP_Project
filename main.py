import numpy as np
import os 
from Cleaner import unzip_files, process_files, clean_subtitles, unzip_single_file, remove_numbers_from_files
from embedding import obtain_embeddings, read_sentences_from_files
from similarity_computation import find_most_similar_sentences


def main():
    Path = os.path.join(os.getcwd(), 'sous-titres')

    # Unzip all files in the directory
    unzip_files(Path)

    # Process all .srt and .sub files in the directory
    process_files(Path)

    # Clean all subtitles in the directory
    clean_subtitles(Path)

    # Unzip a single file
    unzip_single_file(Path, 'example.zip')

    # Remove numbers from all files in the directory
    remove_numbers_from_files(Path)

    # Load the embeddings
    print("Loading embeddings from 'sentence_embeddings.npy'...")
    loaded_embeddings = np.load('sentence_embeddings.npy') # le fichier avec les embeddings
    print(f"Loaded {len(loaded_embeddings)} embeddings successfully!")

    # Example query
    query_sentence = "Voiture"
    print(f"\nQuery Sentence: {query_sentence}")
    
    # Obtain the embedding for the query sentence
    print("\nObtaining embedding for the query sentence...")

    # Load the sentences and file paths
    print("\nLoading sentences and file paths from the dataset...")
    sentences = read_sentences_from_files(Path)
    print(f"Loaded {len(sentences)} sentences and file paths from the dataset.")

    # Find the most similar sentences to the query
    print("\nComputing similarity scores for the query sentence...")
    top_similar_sentences = find_most_similar_sentences(query_sentence, loaded_embeddings, sentences, top_n=5)
    
    # Print the results
    print(f"\nTop 5 most similar sentences to the query '{query_sentence}':")
    for i, (file_name, sentence, score) in enumerate(top_similar_sentences[0], 1):
        print(f"{i}. {file_name}: {sentence.strip()} (Similarity Score: {score:.4f})")


if __name__ == '__main__':
    main()
