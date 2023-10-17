import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class TFIDFSearch:

    def __init__(self, load_existing=True):
        with open(os.path.join(os.getcwd(), 'tokenized_data.json'), 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        # Préparation des données pour le TF-IDF
        self.series_contents = [" ".join(series["tokenized_content"]) for series in self.data]

        # Initialisation du vectorizer
        self.vectorizer = TfidfVectorizer(max_df=0.70, min_df=6, ngram_range=(1, 2))

        if load_existing:
            with open('tfidf_matrix.pkl', 'rb') as f:
                self.tfidf_matrix = pickle.load(f)
            with open('vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
        else:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.series_contents)
            with open('tfidf_matrix.pkl', 'wb') as f:
                pickle.dump(self.tfidf_matrix, f)
            with open('vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)

    def search(self, query):
        # Transformation de la requête en vecteur TF-IDF
        query_vector = self.vectorizer.transform([query])

        # Calcul des scores de similarité
        cosine_similarities = linear_kernel(query_vector, self.tfidf_matrix).flatten()

        # Récupération des indices des séries en fonction de leur score de similarité
        related_series_indices = cosine_similarities.argsort()[:-5:-1]

        # Récupération des séries les plus pertinentes
        results = []
        for index in related_series_indices:
            series_name = self.data[index]["series_name"]
            results.append(series_name)

        return results


if __name__ == "__main__":
    searcher = TFIDFSearch(load_existing=False)
    predefined_queries = ["ile, crash, avion", "drogue", "voiture"]  # Remplacez par vos requêtes prédéfinies

    for query in predefined_queries:
        results = searcher.search(query)
        print(f"Results for query '{query}':")
        for series in results:
            print(series)
        print("\n")
