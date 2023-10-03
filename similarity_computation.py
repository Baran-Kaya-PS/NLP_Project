import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding import model, read_sentences_from_files

def compute_similarity(vector1, vector2):
    """Compute cosine similarity between two vectors."""
    return cosine_similarity([vector1], [vector2])[0][0]

def find_most_similar_sentences(query_sentence, embeddings, sentences, top_n=5):
    """Find the top_n most similar sentences to the query_sentence."""
    # Obtain the embedding for the query sentence
    query_embedding = model.encode([query_sentence])[0]

    # Compute similarities with all sentences in the dataset
    similarities = [compute_similarity(query_embedding, emb) for emb in embeddings]

    # Get the indices of the top_n most similar sentences
    top_indices = np.argsort(similarities)[-top_n:][::-1]

    # Return the top_n most similar sentences along with their similarity scores
    return [(sentences[i], similarities[i]) for i in top_indices]
