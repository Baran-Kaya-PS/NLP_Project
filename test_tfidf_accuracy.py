import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from translate import Translator

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

# Initialiser le vectoriseur TF-IDF en dehors de la fonction
tfidf_vectorizer = TfidfVectorizer()

# Fonction pour traduire la requête en anglais
def translate_to_english(query, source_lang='fr'):
    translator = Translator(from_lang=source_lang, to_lang="en")
    translation = translator.translate(query)
    return translation

# Modifier la fonction pour renvoyer aussi les scores
def get_top_series_with_scores(query, top_n=5):
    # Traduire la requête en anglais
    english_query = translate_to_english(query, source_lang='fr')
    query_vector = tfidf_vectorizer.transform([english_query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    similar_series_indices = cosine_similarities.argsort()[::-1]
    return [list(series_tokenized_content.keys())[i] for i in similar_series_indices[:top_n]], cosine_similarities

# Convertir les textes par série en vecteurs TF-IDF
tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(episodes) for series, episodes in series_tokenized_content.items()])

# Testez le modèle
correct_matches = 0
total_keywords = sum(len(v) for v in keywords_data.values())

print(f"Début des tests sur un total de {len(keywords_data)} séries...")
for idx, (series_name, keywords) in enumerate(keywords_data.items(), start=1):
    print(f"Test en cours pour la série '{series_name}' ({idx}/{len(keywords_data)})...")
    for keyword in keywords:
        top_series, _ = get_top_series_with_scores(keyword)
        if series_name in top_series:
            correct_matches += 1
accuracy = correct_matches / total_keywords * 100

print(f"\nNombre total de mots-clés testés : {total_keywords}")
print(f"Nombre total de correspondances correctes : {correct_matches}")
print(f"Précision du modèle : {accuracy:.2f}%")
