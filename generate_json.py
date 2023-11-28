import os
import re
import json

# Liste des motifs pour extraire les numéros de saison et d'épisode
patterns = [
r'(S\d{1,2}E\d{1,2})',
    r'(\d{1}x\d{2})',
    r'(s\d{2}e\d{2})',
    r'(\d{3})',
    r'(\d{2}h\d{2})',
    r'(\[\d{1}x\d{2}\])',
    r'(s\d{2}h\d{2})',
    r'(Saison \d{2} - épisode \d{2})',
    r'(S\d{1}E\d{2})',
    r'(S\d{2}EP\d{2})',
    r'(\(S\d{2}E\d{2}\))',
    r'(S\d{1} E\d{2})',
    r'(\d{1}h\d{2})',
    r'(s\d{2}ep\d{2})'
]

# Liste des séries
nomSerie = ["24", "90210", "alias", "angel", "battlestargalactica", "betteroffted", "bionicwoman", "blade", "bloodties",
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

# Fonction pour extraire le nom de la série à partir du nom du fichier
def extract_series_name(filename):
    for serie in nomSerie:
        if serie.lower() in filename.lower():
            return serie
    return None

# Fonction pour extraire le numéro de saison et d'épisode à partir du nom du fichier
def extract_season_episode(filename):
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            # Extraction des numéros
            numbers = re.findall(r'\d+', match.group(0))
            if len(numbers) == 2:
                return int(numbers[0]), int(numbers[1])
    return None, None

# Fonction pour extraire la langue à partir du nom du fichier
def extract_language(filename):
    if re.search(r'\bVF\b', filename, re.IGNORECASE):
        return "French"
    elif re.search(r'\bVO\b', filename, re.IGNORECASE):
        return "English"
    return "English"

# Fonction principale pour structurer les données en JSON
def structure_data_to_json(root_path):
    data = []

    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(('.srt', '.sub', '.txt')):
                series_name = extract_series_name(root)
                if series_name is None:
                    continue
                season, episode = extract_season_episode(file)
                language = extract_language(file)

                # Si nous ne pouvons pas déduire la saison à partir du nom du fichier,
                # nous utilisons le nom du dossier parent
                if not season:
                    season_match = re.search(r'Saison (\d+)', root, re.IGNORECASE)
                    if season_match:
                        season = int(season_match.group(1))

                data.append({
                    "series_name": series_name,
                    "season": season,
                    "episode": episode,
                    "language": language,
                    "content": open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore').read()
                })

    # Sauvegarde des données en JSON
    with open("structured_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"{len(data)} files processed and structured into JSON.")


# Exécution de la fonction principale
if __name__ == "__main__":
    root_path = os.path.join(os.getcwd(), 'sous-titres')
    structure_data_to_json(root_path)
    
