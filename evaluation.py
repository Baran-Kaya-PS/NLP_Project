import json
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

# Chargement des données
with open('structured_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Préparation des données pour la classification
texts = [episode['content'] for episode in data]
labels = [1 if episode['language'] == 'English' else 0 for episode in data]  # 1 pour anglais, 0 pour français

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Vectorisation des textes
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Entraînement du modèle
clf = MultinomialNB()
clf.fit(X_train_counts, y_train)

# Prédiction sur l'ensemble de test
y_pred = clf.predict(X_test_counts)

# Calcul du F1 Score
f1 = f1_score(y_test, y_pred, average='weighted')
print(f'F1 Score: {f1}')

# Cross-validation
scores = cross_val_score(clf, X_train_counts, y_train, cv=5, scoring='f1_weighted')
print(f'Cross-validation scores: {scores}')
print(f'Average score: {np.mean(scores)}')

# Enregistrement des résultats dans un fichier
with open('python_test.txt', 'w') as file:
    file.write(f'F1 Score: {f1}\n')
    file.write(f'Cross-validation scores: {scores}\n')
    file.write(f'Average score: {np.mean(scores)}\n')