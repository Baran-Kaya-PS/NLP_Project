import requests
import json

# Vos configurations
API_KEY = "172303ab8e417bb8d39940995feb9d0b"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNzIzMDNhYjhlNDE3YmI4ZDM5OTQwOTk1ZmViOWQwYiIsInN1YiI6IjY1MzdhMjgzZjQ5NWVlMDBjNTE2NGFlOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YjIjKrLFRgKKj6TM3clDOScd26GS622poDHzhaF31uI"
BASE_URL = "https://api.themoviedb.org/3"

# Liste de vos séries
series_names = ["24", "90210", "alias", "angel", "battlestargalactica", "betteroffted", "bionicwoman", "blade", "bloodties",
            "bones", "breakingbad", "buffy", "burnnotice", "californication", "caprica", "charmed", "chuck", "coldcase",
            "community", "criminalminds", "cupid", "daybreak", "demons", "desperatehousewives", "dexter", "dirt",
            "dirtysexymoney", "doctorwho", "dollhouse", "eleventhhour", "entourage", "eureka", "extras", "fearitself",
            "flashforward", "flashpoint", "flightoftheconchords", "fridaynightlights", "friends", "fringe", "futurama",
            "garyunmarried", "ghostwhisperer", "gossipgirl", "greek", "greysanatomy", "heroes", "house",
            "howimetyourmother", "intreatment", "Invasion", "jake", "jekyll", "jericho", "johnfromcincinnati",
            "Journeyman", "knightrider", "kylexy", "legendoftheseeker", "leverage", "lietome", "life", "lost",
            "madmen", "mastersofscifi", "medium", "melroseplace", "mental", "merlin", "moonlight", "mynameisearl",
            "nas", "ncislosangeles", "niptuck", "onetreehill", "painkillerjane", "primeval", "prisonbreak",
            "privatepractice", "psych", "pushingdaisies", "raines", "reaper", "robinhood", "rome", "samanthawho",
            "sanctuary", "scrubs", "sexandthecity", "sixfeetunder", "skins", "smallville", "sonsofanarchy", "southpark",
            "spaced", "stargateatlantis", "stargatesgl", "stargateuniverse", "supernatural", "swingtown", "the4400",
            "thebigbangtheory", "theblackdonnellys", "thekillpoint", "thelostroom", "thementalist", "thenine", "theoc",
            "thepretender", "theriches", "thesarahconnorchronicles", "theshield", "esopranos", "thetudors",
            "thevampirediaries", "thewire", "torchwood", "traveler", "trucalling", "trueblood", "uglybetty",
            "veromcamars", "weeds", "whitechapel", "womensmurderclub", "xfiles"]

# Dictionnaire pour stocker les résultats
series_keywords = {}

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}

for series in series_names:
    # Chercher l'ID de la série sur TMDb
    search_url = f"{BASE_URL}/search/tv?api_key={API_KEY}&query={series}"
    response = requests.get(search_url, headers=headers).json()

    if response["results"]:
        series_id = response["results"][0]["id"]

        # Une fois que vous avez l'ID, récupérez les mots-clés
        keywords_url = f"{BASE_URL}/tv/{series_id}/keywords?api_key={API_KEY}"
        response = requests.get(keywords_url, headers=headers).json()

        if "results" in response:
            keywords = [k["name"] for k in response["results"]]
            series_keywords[series] = keywords

# Sauvegarder les résultats dans un fichier JSON
with open("series_keywords.json", "w", encoding="utf-8") as file:
    json.dump(series_keywords, file, ensure_ascii=False, indent=4)

print("Extraction terminée.")
