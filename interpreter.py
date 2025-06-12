# from parser import parser
# from lexer import lexer
# import sys

# # Funkcja do uruchomienia interpretera na pliku
# def run_file(filename):
#     with open(filename, 'r') as f:
#         code = f.read()
#         parser.parse


from parser import parser
from lexer import lexer
import sys

# Funkcja do uruchomienia interpretera na pliku
def run_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
        parser.parse(code, lexer=lexer)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Użycie: python interpreter.py <plik_z_programem>")
    else:
        run_file(sys.argv[1])
