import re

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

def extract_episode_info(filename):
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return match.group(1)
    return None
