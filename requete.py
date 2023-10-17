import os
import json
from collections import Counter

# Charger les données
with open(os.path.join(os.getcwd(), 'tokenized_data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

# Examen des données brutes
print("Aperçu des données :")
print(data[:5])  # Afficher les 5 premières entrées

# Statistiques des données
print("\nNombre total d'entrées (séries) :", len(data))
token_lengths = [len(series["tokenized_content"]) for series in data]
print("Longueur moyenne des tokens pour chaque série :", sum(token_lengths) / len(token_lengths))
print("Série avec le plus de tokens :", data[token_lengths.index(max(token_lengths))]["series_name"])
print("Série avec le moins de tokens :", data[token_lengths.index(min(token_lengths))]["series_name"])

# Examen des tokens les plus fréquents
all_tokens = [token for series in data for token in series["tokenized_content"]]
token_counts = Counter(all_tokens)
print("\nTokens les plus courants :", token_counts.most_common(10))

# Examen des tokens les moins fréquents
#print("\nTokens les moins fréquents :", [item for item in token_counts.items() if item[1] == 1])

# Vérification de la cohérence (espace réservé pour le moment)
# ...

# Examen des requêtes précédentes (espace réservé pour le moment)
# ...

