## Sommaire
1. [Introduction](#introduction)
2. [Installation et Configuration](#installation-et-configuration)
3. [Cleaner_obj.py](#cleaner_objpy)
4. [generate_json_obj.py](#generate_json_objpy)
5. [tokenizer.py](#tokenizerpy)
6. [matrix_gen_obj.py](#matrix_gen_objpy)
7. [main.py](#mainpy)
8. [Utilisation](#utilisation)

### Introduction

Cette suite de scripts est conçue pour le traitement, la tokenisation, et l'analyse de sous-titres de séries télévisées. Elle permet de décompresser, nettoyer, structurer en JSON, tokeniser et finalement créer une matrice TF-IDF pour l'analyse de contenu.

### Installation et Configuration

- Prérequis : Python 3.10, NLTK, Scikit-learn
- Installation : `pip install nltk scikit-learn`
- Configuration : Assurez-vous que les chemins des fichiers dans les scripts sont correctement configurés selon votre structure de répertoire.

### Cleaner_obj.py

- **Objectif** : Nettoyer et préparer les fichiers de sous-titres.
- **Fonctions Principales** :
  - `unzip_files` : Décompresse les fichiers `.zip`.
  - `clean_subtitles` : Nettoie les fichiers de sous-titres.
  - `process_files` : Traite les fichiers `.srt` et `.sub`.
  - `remove_numbers_from_files` : Supprime les chiffres des fichiers.
  - `remove_accents_from_files` : Supprime les accents.
  - `execute` : Exécute toutes les étapes de nettoyage.

### generate_json_obj.py

- **Objectif** : Structurer les sous-titres en JSON.
- **Fonctions Principales** :
  - `extract_series_name`, `extract_season_episode`, `extract_language` : Extraient des informations à partir des noms de fichiers.
  - `structure_data_to_json` : Structure les données en JSON.
  - `execute` : Exécute la structuration en JSON.

### tokenizer.py

- **Objectif** : Tokeniser et nettoyer le contenu textuel.
- **Fonctions Principales** :
  - `tokenize_text_simple`, `tokenize_text_with_stopwords` : Tokenisent le texte.
  - `tokenize_data` : Tokenise les données de chaque série.
  - `clean_data` : Nettoie les données tokenisées.
  - `execute` : Exécute les étapes de tokenisation et de nettoyage.

### matrix_gen_obj.py

- **Objectif** : Créer une matrice TF-IDF.
- **Fonctions Principales** :
  - `load_data`, `generate

_series_tokenized_content` : Charge et prépare le contenu tokenisé.
  - `generate_tfidf_matrix` : Génère la matrice TF-IDF.
  - `create_tfidf_json` : Convertit la matrice TF-IDF en JSON.
  - `save_json` : Sauvegarde le JSON de la matrice TF-IDF.
  - `execute` : Exécute la création et la sauvegarde de la matrice TF-IDF.

### main.py

- **Objectif** : Orchestrer l'exécution de tous les scripts.
- **Fonction Principale** :
  - `main` : Exécute les scripts principaux dans l'ordre pour réaliser le flux de travail complet.

### Utilisation

Pour utiliser ces scripts, exécutez `main.py`. Ce script appelle les autres scripts dans l'ordre nécessaire pour effectuer le traitement complet des sous-titres. Assurez-vous que les chemins des fichiers dans chaque script sont correctement configurés selon votre environnement.
