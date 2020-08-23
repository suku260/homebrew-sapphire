
import sys
sys.path.insert(0, "../..")

tokens = (
    'NAME','ARRAY','STRING','CLASS','FUNCTION','SEMI','PERIOD','AND','OR','NUMBER','LE','SEP','GE','EQ','NE','G','L','LBRACK','RBRACK','LPAREN','RPAREN','LBRACE','RBRACE','IF','WHILE','FOR'
)

literals = ['=', '+','.','-', '*', '/', '(', ')','^','%',',']

# Tokens
t_LE=r'<='
t_GE=r'>='
t_EQ=r'=='
t_NE=r'!='
t_OR = r'\|\|'
t_AND = r'&&'
t_G=r'>'
t_SEP=r','
t_L=r'<'
t_CLASS=r'class'
t_FUNCTION=r'function'
t_FOR=r'for'
t_IF=r'if'
t_PERIOD = r'\.'
t_SEMI = r';'
t_WHILE=r'while'
t_LBRACK=r'\['
t_RBRACK=r'\]'
t_LBRACE=r'\{'
t_RBRACE=r'\}'
t_LPAREN=r'\('
t_RPAREN=r'\)'


t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING = r'"[a-zA-Z_][a-zA-Z_0-9]*"' 
def EOL(t):
	r';'
	pass
def comma(t):
	r','
	pass
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t  
def t_ARRAY(t):
	r'\[([^\[\]]*)\]'
	t.value= (t.value[1:-1]).split(',')
	return t
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^', '%'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]
def p_if_loop(p):
	'statement : IF LPAREN expression RPAREN LBRACE expression RBRACE'
	print(f" if {p[3]} is true then do {p[6]}")
def p_while_loop(p):
	'statement : WHILE LPAREN expression RPAREN LBRACE expression RBRACE'
	print(f" while {p[3]} is true then do {p[6]}")
def p_for_loop(p):
	'statement : FOR LPAREN expression RPAREN LBRACE expression RBRACE'
	print(f" for {p[3]} is true then do {p[6]}")

def p_statement_expr(p):
    'statement : expression'
    if p[1] != None:
    	print(p[1])

def p_bool_cond(p):
	'''expression : expression L expression
                   | expression G expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
	boolean=False
	if p[2] == '>':
		if p[1] > p[3]:
			boolean=True
	elif p[2] == '<':
		if p[1] < p[3]:
			boolean=True
	elif p[2] == '>=':
		if p[1] >= p[3]:
			boolean=True
	elif p[2] == '<=':
		if p[1] <= p[3]:
			boolean=True
	elif p[2] == '==':
		if p[1] == p[3]:
			boolean=True
	elif p[2] == '!=':
		if p[1] != p[3]:
			boolean=True
	p[0]=(boolean)
def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression
                  | expression '%' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]
def p_expression_array(p):
	"expression : ARRAY" 
	try:
		p[0] = p[1].split(',')
	except:
		p[0] = p[1]
def p_expression_string(p):
    "expression : STRING"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        p[0] = f'undefined variable {p[1]} not found'


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('Sapphire:> ')
        while ';' not in s:
        	s2=input("...")
        	s=s+s2
        if s=='exit;':
        	exit(1)


    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s.replace(';',''))
