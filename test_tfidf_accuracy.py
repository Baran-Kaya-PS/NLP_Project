import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator
import concurrent.futures

# Charger les données à partir du fichier JSON
with open('tokenized_data_cleaned.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Charger le fichier JSON des mots-clés
with open('series_keywords.json', 'r', encoding='utf-8') as file:
    keywords_data = json.load(file)

# Regrouper les textes tokenisés par série
series_tokenized_content = {}
for episode in data:
    series_name = episode['series_name']
    tokenized_content = episode['tokenized_content']
    if series_name not in series_tokenized_content:
        series_tokenized_content[series_name] = []
    tokenized_content = [str(phrase) for phrase in tokenized_content]
    series_tokenized_content[series_name].extend(tokenized_content)

# Fusionner les mots-clés avec le contenu tokenisé
for series_name, keywords in keywords_data.items():
    if series_name in series_tokenized_content:
        series_tokenized_content[series_name].extend(keywords)

# Fonction pour traduire la requête en anglais
def translate_to_english(query, source_lang='fr'):
    translator = Translator(from_lang=source_lang, to_lang="en")
    translation = translator.translate(query)
    return translation

# Modifier la fonction pour renvoyer aussi les scores
def get_top_series_with_scores(query, tfidf_vectorizer, tfidf_matrix):
    # Traduire la requête en anglais
    english_query = translate_to_english(query, source_lang='fr')
    query_vector = tfidf_vectorizer.transform([english_query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    similar_series_indices = cosine_similarities.argsort()[::-1]
    return [list(series_tokenized_content.keys())[i] for i in similar_series_indices[:3]], cosine_similarities


def test_params(params, tfidf_vectorizer):
    tfidf_vectorizer.set_params(**params)

    # Fusionner les mots-clés avec le contenu tokenisé
    for series_name, keywords in keywords_data.items():
        if series_name in series_tokenized_content:
            series_tokenized_content[series_name].extend(keywords)

    tfidf_matrix = tfidf_vectorizer.fit_transform(
        [" ".join(episodes) for series, episodes in series_tokenized_content.items()])

    correct_matches = 0
    for series_name, keywords in keywords_data.items():
        for keyword in keywords:
            top_series, _ = get_top_series_with_scores(keyword, tfidf_vectorizer, tfidf_matrix)
            if series_name in top_series:
                correct_matches += 1
    accuracy = correct_matches / sum(len(v) for v in keywords_data.values()) * 100
    print(f"Précision pour {params}: {accuracy:.4f}")
    return accuracy, params


parameter_sets = [
    {"ngram_range": (1, 1), "use_idf": True, "norm": "l2"},
    {"ngram_range": (1, 2), "use_idf": True, "norm": "l2"},
    # ... ajoutez d'autres combinaisons de paramètres ici ...
]

best_accuracy = 0
best_params = None

tfidf_vectorizer = TfidfVectorizer()

num_threads = 4  # ajustez en fonction du nombre de cœurs CPU disponibles

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(test_params, param_set, tfidf_vectorizer) for param_set in parameter_sets]
    for future in concurrent.futures.as_completed(futures):
        accuracy, params = future.result()
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_params = params

print(f"Meilleure précision obtenue: {best_accuracy:.4f}")
print(f"Meilleurs paramètres: {best_params}")
