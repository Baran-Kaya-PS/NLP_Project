import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from embedding import model, read_sentences_from_files, obtain_embeddings

def compute_similarity(vector1, vector2):
    """Compute cosine similarity between two vectors."""
    return cosine_similarity([vector1], [vector2])[0][0]

def find_most_similar_sentences(query_sentence, loaded_embeddings, sentences, top_n=5):
    """Find the top_n most similar sentences to the query_sentence."""
    # Obtain the embedding for the query sentence
    query_embeddings = obtain_embeddings(os.path.join(os.getcwd(), 'sous-titres'))

    # Compute the cosine similarity between the query embedding and all sentence embeddings
    similarity_scores = np.dot(loaded_embeddings, query_embeddings.T) / (np.linalg.norm(loaded_embeddings, axis=1) * np.linalg.norm(query_embeddings, axis=1))

    # Get the indices of the top N most similar sentences
    top_indices = np.argsort(similarity_scores, axis=0)[::-1][:top_n]

    # Get the file names, sentences, and similarity scores for the top N most similar sentences for each query sentence
    top_similar_sentences = []
    for i in range(len(query_sentence)):
        top_similar_sentences.append([(sentences[j][0], sentences[j][1], similarity_scores[j][i]) for j in top_indices[:, i]])

    return top_similar_sentences
