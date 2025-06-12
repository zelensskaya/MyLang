from parser import parser  # Importujemy parser z modułu parser.py
import sys

# Odczytujemy zawartość pliku "program.txt" z kodem źródłowym
with open("program.txt", encoding="utf-8") as f:
    data = f.read()

print("Interpreter uruchomiony z main.py")  # Informacja o uruchomieniu interpretera
parser.parse(data)  # Parsujemy (analizujemy składnię) i wykonujemy kod
