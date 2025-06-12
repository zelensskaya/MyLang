import ply.yacc as yacc
from lexer import tokens

#do przechowywania wartości zmiennych
variables = {}

#lista instrukcji
def p_program(p):
    'program : statements'
    execute(p[1])

def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]

def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]



# Deklaracja zmiennej
def p_statement_declaration(p):
    'statement : ZMIENNA ID SEMICOLON'
    p[0] = ('declare', p[2])

# Przypisanie wartości do zmiennej
def p_statement_assign(p):
    'statement : ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])

# Instrukcja wypisania (print)
def p_statement_wypisz(p):
    'statement : WYPISZ wypisz_expr SEMICOLON'
    p[0] = ('print', p[2])

# Konkatenacja wyrażeń do wypisania
def p_wypisz_expr_concat(p):
    'wypisz_expr : wypisz_expr PLUS wypisz_term'
    p[0] = p[1] + [p[3]]

def p_wypisz_expr_term(p):
    'wypisz_expr : wypisz_term'
    p[0] = [p[1]]

def p_wypisz_term_string(p):
    'wypisz_term : STRING'
    p[0] = ('str', p[1])

def p_wypisz_term_var(p):
    'wypisz_term : ID'
    p[0] = ('var', p[1])




# dodawanie/odejmowanie
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

# mnożenie/dzielenie
def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_var(p):
    'factor : ID'
    p[0] = ('var', p[1])

# Warunek - porównanie
def p_condition_comparison(p):
    '''condition : expression EQ expression
                 | expression LT expression
                 | expression GT expression
                 | expression LE expression
                 | expression GE expression'''
    p[0] = ('condition', p[2], p[1], p[3])

# Warunek logiczny AND / OR
def p_condition_logic_binop(p):
    '''condition : condition I condition
                 | condition LUB condition'''
    p[0] = ('logic', p[2], p[1], p[3])

# Negacja warunku
def p_condition_not(p):
    'condition : NIE condition'
    p[0] = ('not', p[2])

# Instrukcja if-else
def p_statement_if_else(p):
    '''statement : JEZELI LPAREN condition RPAREN WTEDY LBRACE statements RBRACE INACZEJ LBRACE statements RBRACE SEMICOLON'''
    p[0] = ('ifelse', p[3], p[7], p[11])

# Instrukcja if bez else
def p_statement_if_only(p):
    '''statement : JEZELI LPAREN condition RPAREN WTEDY LBRACE statements RBRACE SEMICOLON'''
    p[0] = ('if', p[3], p[7])

# Instrukcja wczytania zmiennej z inputa
def p_statement_wczytaj(p):
    'statement : WCZYTAJ ID SEMICOLON'
    p[0] = ('wczytaj', p[2])

# Pętla while
def p_statement_while(p):
    'statement : DOPOKI LPAREN condition RPAREN WYKONUJ LBRACE statements RBRACE SEMICOLON'
    p[0] = ('while', p[3], p[7])

def p_statement_increment(p):
    'statement : PLUS PLUS ID SEMICOLON'
    p[0] = ('inc', p[3])

def p_statement_decrement(p):
    'statement : MINUS MINUS ID SEMICOLON'
    p[0] = ('dec', p[3])

# Obsługa błędów składniowych
def p_error(p):
    if p:
        print(f"Błąd składniowy w linii {p.lineno}: nieoczekiwany token '{p.value}'")
    else:
        print("Błąd składniowy: niespodziewany koniec pliku")

# Funkcja ewaluująca wyrażenia i warunki
def evaluate(expr):
    if isinstance(expr, tuple):
        typ = expr[0]
        if typ == 'var':
            name = expr[1]
            if name not in variables:
                print(f"Błąd: zmienna '{name}' nie istnieje.")
                return 0
            return variables[name]
        elif typ == 'str':
            return expr[1]
        elif typ == 'binop':
            op = expr[1]
            left = evaluate(expr[2])
            right = evaluate(expr[3])
            if isinstance(left, str) or isinstance(right, str):
                print("Błąd: operacja arytmetyczna na tekstach niedozwolona.")
                return 0
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    print("Błąd: dzielenie przez zero.")
                    return 0
                return left // right
        elif typ == 'condition':
            op = expr[1]
            left = evaluate(expr[2])
            right = evaluate(expr[3])
            if op == '==':
                return left == right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
            elif op == '<=':
                return left <= right
            elif op == '>=':
                return left >= right
        elif typ == 'logic':
            op = expr[1]
            left = evaluate(expr[2])
            right = evaluate(expr[3])
            if op == 'i':
                return left and right
            elif op == 'lub':
                return left or right
        elif typ == 'not':
            val = evaluate(expr[1])
            return not val
    else:
        return expr

#listę instrukcji
def execute(statements):
    for stmt in statements:
        execute_statement(stmt)

#pojedynczą instrukcję
def execute_statement(stmt):
    global variables
    typ = stmt[0]
    if typ == 'declare': # Deklaracja zmiennej
        if stmt[1] not in variables:
            variables[stmt[1]] = 0
    elif typ == 'assign':  # Przypisanie wartości
        variables[stmt[1]] = evaluate(stmt[2])
    elif typ == 'print':
        output = ''.join(str(evaluate(x)) for x in stmt[1])
        print(output)
    elif typ == 'if':
        condition = evaluate(stmt[1])
        if condition:
            execute(stmt[2])
    elif typ == 'ifelse':
        condition = evaluate(stmt[1])
        if condition:
            execute(stmt[2])
        else:
            execute(stmt[3])
    elif typ == 'wczytaj':
        varname = stmt[1]
        print(f"Podaj wartosc dla {varname}: ", end='', flush=True)
        value = input()
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass  # pozostaw string
        variables[varname] = value
    elif typ == 'inc':
        if stmt[1] in variables:
            variables[stmt[1]] += 1
        else:
            print(f"Błąd: zmienna '{stmt[1]}' nie istnieje.")
    elif typ == 'dec':
        if stmt[1] in variables:
            variables[stmt[1]] -= 1
        else:
            print(f"Błąd: zmienna '{stmt[1]}' nie istnieje.")
    elif typ == 'while':
        while evaluate(stmt[1]):
            execute(stmt[2])

# parser
parser = yacc.yacc()
