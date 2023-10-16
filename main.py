import numpy as np
import os 
from Cleaner import unzip_files, process_files, clean_subtitles, unzip_single_file, remove_numbers_from_files,remove_accents_from_files
from embedding import obtain_embeddings, read_sentences_from_files
from similarity_computation import find_most_similar_sentences

def main():
    Path = os.path.join(os.getcwd(), 'sous-titres')
    unzip_files(Path)
    remove_numbers_from_files(Path)
    remove_accents_from_files(Path)
    process_files(Path)

if __name__ == '__main__':
    main()
