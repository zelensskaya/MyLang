import ply.lex as lex

# Definicja tokenów (symboli leksykalnych)
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'EQ', 'LT', 'GT', 'LE', 'GE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON'
]

reserved = {
    'zmienna': 'ZMIENNA',
    'wypisz': 'WYPISZ',
    'jezeli': 'JEZELI',
    'wtedy': 'WTEDY',
    'inaczej': 'INACZEJ',
    'i': 'I',
    'lub': 'LUB',
    'nie': 'NIE',
    'wczytaj': 'WCZYTAJ',
    'dopoki': 'DOPOKI',
    'wykonuj': 'WYKONUJ'
}

# Dodajemy słowa kluczowe do listy tokenów
tokens += list(reserved.values())

# regex
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_EQ        = r'=='
t_LT        = r'<'
t_GT        = r'>'
t_LE        = r'<='
t_GE        = r'>='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'

#spacje i tabulatory
t_ignore = ' \t'

#ID - identyfikatory i słowa kluczowe
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

#Jednolinijkowy komentarz
def t_comment_single(t):
    r'\#\#[^\n]*'
    pass

#Wielolinijkowy komentarz
def t_comment_multi(t):
    r'/\#(.|\n)*?\#/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Liczenie nowych linii
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#błędów leksykalnych
def t_error(t):
    print(f"Błąd leksykalny: nieznany symbol '{t.value[0]}' w linii {t.lineno}")
    t.lexer.skip(1)

# Tworzymy lexer
lexer = lex.lex()
