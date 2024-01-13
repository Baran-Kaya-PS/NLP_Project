import os
import re
import json

class JSONGenerator:
    # Motifs réguliers des épisodes et des séries
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
        r'(s\d{2}ep\d{2})',
        r'(311)',
        r'(3x02)',
        r'(0307)'
    ]

    # Liste des noms de séries à reconnaître
    nomSerie = ["24", "90210", "alias", "angel", "battlestargalactica", "betteroffted", "bionicwoman", "blade", "bloodties",
            "bones", "breakingbad", "buffy", "burnnotice", "californication", "caprica", "charmed", "chuck", "coldcase",
            "community", "criminalminds", "cupid", "daybreak", "demons", "desperatehousewives", "dexter", "dirt",
            "dirtysexymoney", "doctorwho", "dollhouse", "eleventhhour", "entourage", "eureka", "extras", "fearitself",
            "flashforward", "flashpoint", "flightoftheconchords", "fridaynightlights", "friends", "fringe", "futurama",
            "garyunmarried", "ghostwhisperer", "gossipgirl", "greek", "greysanatomy", "heroes", "house",
            "howimetyourmother", "intreatment", "Invasion", "jake", "jekyll", "jericho", "johnfromcincinnati",
            "journeyman", "knightrider", "kylexy", "legendoftheseeker", "leverage", "lietome", "life", "lost",
            "madmen", "mastersofscifi", "medium", "melroseplace", "mental", "merlin", "moonlight", "mynameisearl", 
            "ncislosangeles", "niptuck", "onetreehill", "oz" "painkillerjane", "primeval", "prisonbreak",
            "privatepractice", "psych", "pushingdaisies", "raines", "reaper", "robinhood", "rome", "samanthawho",
            "sanctuary", "scrubs", "sexandthecity", "sixfeetunder", "skins", "smallville", "sonsofanarchy", "southpark",
            "spaced", "stargateatlantis", "stargatesg1", "stargateuniverse", "supernatural", "swingtown", "the4400",
            "thebigbangtheory", "theblackdonnellys", "thekillpoint", "thelostroom", "thementalist", "thenine", "theoc",
            "thepretender", "theriches", "thesarahconnorchronicles", "theshield", "thesopranos", "thetudors",
            "thevampirediaries", "thewire", "torchwood", "traveler", "trucalling", "trueblood", "uglybetty",
            "veronicamars", "weeds", "whitechapel", "womensmurderclub", "xfiles"] # série manquante dirtysexymoney, journeyman, ncislosangeles, oz, sixfeetunder, spaced, thelostroom, thementalist

    def __init__(self, root_path):
        self.root_path = root_path

    def extract_series_name(self, filename):
        # Extrait le nom de la série du nom de fichier
        for serie in self.nomSerie:
            if serie.lower() in filename.lower():
                return serie
        return None

    def extract_season_episode(self, filename):
        # Extrait le numéro de saison et d'épisode du nom de fichier
        for pattern in self.patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                numbers = re.findall(r'\d+', match.group(0))
                if len(numbers) == 2:
                    return int(numbers[0]), int(numbers[1])
        return None, None

    def extract_language(self, filename):
        # Déduit la langue du fichier à partir de son nom
        if re.search(r'\bVF\b', filename, re.IGNORECASE):
            return "French"
        elif re.search(r'\bVO\b', filename, re.IGNORECASE):
            return "English"
        return "English"

    def structure_data_to_json(self):
        # Structure les données des fichiers sous-titres en format Json
        data = []
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(('.srt', '.sub', '.txt')):
                    series_name = self.extract_series_name(root)
                    if series_name is None:
                        continue
                    season, episode = self.extract_season_episode(file)
                    language = self.extract_language(file)

                    # Utiliser le nom du dossier pour la saison si nécessaire
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

        with open("structured_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{len(data)} files processed and structured into JSON.")

    def execute(self):
        # Exécute la fonction de structuration en Json
        self.structure_data_to_json()

if __name__ == "__main__":
    generator = JSONGenerator(os.path.join(os.getcwd(), 'sous-titres'))
    generator.execute()
