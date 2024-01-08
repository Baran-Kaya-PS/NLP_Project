import Cleaner_obj
import generate_json_obj
import tokenizer_obj
import matrix_gen_obj

def main(): # Modifier le nom des fichiers si c'est pas les bon noms

    Cleaner_obj.main()
    generate_json_obj.main()
    tokenizer_obj.main()
    matrix_gen_obj.main()
    
if __name__ == "__main__":
    main()
