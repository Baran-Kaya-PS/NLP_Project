import json
import pymongo

# Paramètres de connexion MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "mySearch_db"
COLLECTION_NAME = "tfidf_data"

# Établir une connexion à MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Lire les données depuis le fichier JSON
with open('tfidf_matrix.json', 'r', encoding='utf-8') as file:
    tfidf_data = json.load(file)

# Insérer les données dans MongoDB
for series_name, tfidf_values in tfidf_data.items():
    document = {"series_name": series_name, "tfidf_values": tfidf_values}
    collection.insert_one(document)

print("Les données TF-IDF ont été insérées dans MongoDB.")