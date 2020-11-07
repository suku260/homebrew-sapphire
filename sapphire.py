from os import *
from ply import *
import sys
sys.path.insert(0, "../..")

tokens = (
    'NAME', 'FOR','WHILE','IF','NUMBER','STRING','ARRAY','OR','LE','GE','EQ','NE','AND','LBRACE','RBRACE','LPAREN','RPAREN','IN','L','G'
)

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

# Tokens
t_LE=r'<='
t_GE=r'>='
t_EQ=r'=='
t_NE=r'!='
t_OR = r'\|\|'
t_AND = r'&&'
t_G=r'>'
t_L=r'<'
t_LBRACE=r'\{'
t_RBRACE=r'\}'
t_LPAREN=r'\('
t_RPAREN=r'\)'

reserved= {
'CLASS' : 'class',
'BUILD' : 'build',
'FUNCTION' : 'function',

'NOT' : 'not',
'INPUT' : 'input'}

tokens=tokens+(tuple(reserved.values()))
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
def t_IN(t):
	r'in'
	return t
def t_FOR(t):
	r'for'
	return t
def t_WHILE(t):
	r'while'
	return t
def t_IF(t):
	r'if'
	return t
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
imports = {}
def p_statement_assign(p):
	'statement : NAME "=" expression'
	if p[1] not in tokens:
		names[p[1]] = p[3]
	else:
		print("cannot use a reserved keyword for a variable")
def p_input_assign(p):
    'statement : NAME "=" input LPAREN expression RPAREN'
    x=input('\n')
    names[p[1]] = x
def p_in_comparison(p):
	"statement : expression IN expression"
	boolean3=False
	try:
		item1=str(p[1])
		item2=str(p[3])
	except:
		item1=p[1].replace('"','')
		item2=p[3].replace('"','')
	
	if item1 in item2:
   		boolean3=True
	else:
   		boolean3=False
	print(boolean3)
def p_if_loop(p):
	'statement : IF LPAREN expression RPAREN LBRACE expression RBRACE'
	action='do'
	if p[3]==True:
		action=action
	else:
		action = 'dont do'
	print(f" if {p[3]} then {action} {p[6]}")
def p_while_loop(p):
	'statement : WHILE LPAREN expression RPAREN LBRACE expression RBRACE'
	action='do'
	if p[3]==True:
		action=action
	else:
		action = 'dont do'
	print(f" while {p[3]} then {action} {p[6]}")
def p_for_loop(p):
	'statement : FOR LPAREN expression RPAREN LBRACE expression RBRACE'
	action='do'
	if p[3]==True:
		action=action
	else:
		action = 'dont do'
	print(f" for {p[3]} then {action} {p[6]}")
def p_conditional_and(p):
    '''statement : expression L expression AND expression L expression
    			  | expression L expression AND expression G expression
    			  | expression L expression AND expression GE expression
    			  | expression L expression AND expression LE expression
    			  | expression L expression AND expression EQ expression
    			  | expression L expression AND expression NE expression
                  | expression G expression AND expression L expression
    			  | expression G expression AND expression G expression
    			  | expression G expression AND expression GE expression
    			  | expression G expression AND expression LE expression
    			  | expression G expression AND expression EQ expression
    			  | expression G expression AND expression NE expression
    			  | expression GE expression AND expression L expression
    			  | expression GE expression AND expression G expression
    			  | expression GE expression AND expression GE expression
    			  | expression GE expression AND expression LE expression
    			  | expression GE expression AND expression EQ expression
    			  | expression GE expression AND expression NE expression
    			  | expression LE expression AND expression L expression
    			  | expression LE expression AND expression G expression
    			  | expression LE expression AND expression GE expression
    			  | expression LE expression AND expression LE expression
    			  | expression LE expression AND expression EQ expression
    			  | expression LE expression AND expression NE expression
    			  | expression EQ expression AND expression L expression
    			  | expression EQ expression AND expression G expression
    			  | expression EQ expression AND expression GE expression
    			  | expression EQ expression AND expression LE expression
    			  | expression EQ expression AND expression EQ expression
    			  | expression EQ expression AND expression NE expression
    			  | expression NE expression AND expression L expression
    			  | expression NE expression AND expression G expression
    			  | expression NE expression AND expression GE expression
    			  | expression NE expression AND expression LE expression
    			  | expression NE expression AND expression EQ expression
    			  | expression NE expression AND expression NE expression'''
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
    boolean2=False
    if p[6] == '>':
    	if p[5] > p[7]:
    		boolean2=True
    elif p[6] == '<':
    	if p[5] < p[7]:
    		boolean2=True
    elif p[6] == '>=':
    	if p[5] >= p[7]:
    		boolean2=True
    elif p[6] == '<=':
    	if p[5] <= p[7]:
    		boolean2=True
    elif p[6] == '==':
    	if p[5] == p[7]:
    		boolean2=True
    elif p[6] == '!=':
    	if p[5] != p[7]:
    		boolean2=True
    if boolean==True and boolean2==True:
    	p[0]=True
    else:
    	p[0]=False
    print(p[0])
def p_conditional_or(p):
    '''statement : expression L expression OR expression L expression
    			  | expression L expression OR expression G expression
    			  | expression L expression OR expression GE expression
    			  | expression L expression OR expression LE expression
    			  | expression L expression OR expression EQ expression
    			  | expression L expression OR expression NE expression
                  | expression G expression OR expression L expression
    			  | expression G expression OR expression G expression
    			  | expression G expression OR expression GE expression
    			  | expression G expression OR expression LE expression
    			  | expression G expression OR expression EQ expression
    			  | expression G expression OR expression NE expression
    			  | expression GE expression OR expression L expression
    			  | expression GE expression OR expression G expression
    			  | expression GE expression OR expression GE expression
    			  | expression GE expression OR expression LE expression
    			  | expression GE expression OR expression EQ expression
    			  | expression GE expression OR expression NE expression
    			  | expression LE expression OR expression L expression
    			  | expression LE expression OR expression G expression
    			  | expression LE expression OR expression GE expression
    			  | expression LE expression OR expression LE expression
    			  | expression LE expression OR expression EQ expression
    			  | expression LE expression OR expression NE expression
    			  | expression EQ expression OR expression L expression
    			  | expression EQ expression OR expression G expression
    			  | expression EQ expression OR expression GE expression
    			  | expression EQ expression OR expression LE expression
    			  | expression EQ expression OR expression EQ expression
    			  | expression EQ expression OR expression NE expression
    			  | expression NE expression OR expression L expression
    			  | expression NE expression OR expression G expression
    			  | expression NE expression OR expression GE expression
    			  | expression NE expression OR expression LE expression
    			  | expression NE expression OR expression EQ expression
    			  | expression NE expression OR expression NE expression'''
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
    boolean2=False
    if p[6] == '>':
    	if p[5] > p[7]:
    		boolean2=True
    elif p[6] == '<':
    	if p[5] < p[7]:
    		boolean2=True
    elif p[6] == '>=':
    	if p[5] >= p[7]:
    		boolean2=True
    elif p[6] == '<=':
    	if p[5] <= p[7]:
    		boolean2=True
    elif p[6] == '==':
    	if p[5] == p[7]:
    		boolean2=True
    elif p[6] == '!=':
    	if p[5] != p[7]:
    		boolean2=True
    if boolean==True or boolean2==True:
    	p[0]=True
    else:
    	p[0]=False
    print(p[0])
def p_function_def(p):
    'statement : function expression LPAREN expression RPAREN LBRACE expression RBRACE'
    print("function def")
def p_class_def(p):
    'statement : class expression LPAREN expression RPAREN LBRACE expression RBRACE'
    print("class def")
def p_build_def(p):
    'statement : build expression LPAREN expression RPAREN LBRACE expression RBRACE'
    print("build def")
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
        print(f"Syntax error on line {p.lineno} for position {p.lexpos} at symbol'%s'"  % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()


while True:
    try:

        s = input('Sapphire:> ')
        while ';' not in s:
        	s2=input("...")
        	lexer.lineno+=1
        	s=s+s2

        if s=='exit;':
        	exit(1)


    except EOFError:
        break
    if not s:
        continue
    if ".sap" not in s:

   		yacc.parse(s.replace(';',''))
    else:
    	lexer.lineno=1
    	if'/' not in s:
    		f = open(str(os.path.dirname(os.path.realpath(__file__)))+"/"+s.replace(";",""), "r")
    	else:
    		f = open(s.replace(";",""), "r")

    	for line in f:
    		yacc.parse(line.replace(";",""))

