from sly import Lexer
from sly import Parser
class BasicLexer(Lexer): 
	tokens = { NAME, NUMBER, SEP, STRING,WHILE,ID, IF, ELSE ,RPAREN ,LBRACK,RBRACK, LPAREN ,RBRACE ,LBRACE ,FOR, EQ, LE, GE, NE, ARRAY } 
	ignore = '\t '
	literals = { '=', '+', '-', '/', '*', ',', ';','>','<','^','%','!',','} 


	# Define tokens as regular expressions 
	# (stored as raw strings) 
	NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
	STRING = r'\".*?\"'
	EQ      = r'=='
	LE      = r'<='
	GE      = r'>='
	NE      = r'!='
	RPAREN= r'\)'
	LPAREN= r'\('
	RBRACE= r'\}'
	LBRACE= r'\{'
	RBRACK= r'\]'
	LBRACK= r'\['
	SEP= r','
	# Number token 
	@_(r'\d+') 
	def NUMBER(self, t): 
		
		# convert it into a python integer 
		t.value = int(t.value) 
		return t 
	ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
	ID['if'] = IF
	ID['else'] = ELSE
	ID['while'] = WHILE
	ID['for'] = FOR
	ID['[]'] = ARRAY

	@_(r';.*') 
	def EOL(self, t): 
		pass
	@_(r',.*') 
	def comma(self, t): 
		pass
	@_(r'//.*') 
	def COMMENT(self, t): 
		pass
	@_(r'{.*') 
	def nest(self, t): 
		t.type = '{'
		self.nesting_level = self.nesting_level+1
		return t
	@_(r'}.*') 
	def nest(self, t): 
		t.type = '}'
		self.nesting_level = self.nesting_level-1	
		return t
	# Newline token(used only for showing 
	# errors in new line) 
	@_(r'\n+') 
	def newline(self, t): 
		self.lineno = t.value.count('\n')
class BasicParser(Parser): 
	#tokens are passed from lexer to parser 
	tokens = BasicLexer.tokens 

	precedence = ( 
		('left','^','%'),
		('left', '+', '-'), 
		('left', '*', '/'), 
		('right', 'UMINUS'), 
	) 

	def __init__(self): 
		self.env = { } 

	@_('') 
	def statement(self, p): 
		pass
	
	@_('var_assign') 
	def statement(self, p): 
		return p.var_assign 

	
	@_('NAME "=" expr') 
	def var_assign(self, p): 
		return ('var_assign', p.NAME, p.expr) 

	@_('NAME "=" STRING') 
	def var_assign(self, p): 
		return ('var_assign', p.NAME, p.STRING) 

	@_('expr') 
	def statement(self, p): 
		return (p.expr) 

	@_('expr "+" expr') 
	def expr(self, p): 
		return ('add', p.expr0, p.expr1) 
	@_('expr "%" expr') 
	def expr(self, p): 
		return ('modulo', p.expr0, p.expr1) 
	@_('expr ">" expr') 
	def expr(self, p): 
		return ('boolgreater', p.expr0, p.expr1) 
	@_('expr "<" expr') 
	def expr(self, p): 
		return ('boolless', p.expr0, p.expr1)
	
	@_('expr "-" expr') 
	def expr(self, p): 
		return ('sub', p.expr0, p.expr1) 

	@_('expr "*" expr') 
	def expr(self, p): 
		return ('mul', p.expr0, p.expr1) 

	@_('expr "^" expr') 
	def expr(self, p): 
		return ('power', p.expr0, p.expr1) 
	@_('expr "!"') 
	def expr(self, p): 
		return ('factorial', p.expr) 
	@_('expr "/" expr') 
	def expr(self, p): 
		return ('div', p.expr0, p.expr1) 
	@_('NAME "=" LBRACK expr RBRACK') 
	def expr(self, p): 
		exp=str(p.expr).split(',')
		for a in exp:
			print(a)

		return ('var_assign',p.NAME,p.expr) 

	@_('"-" expr %prec UMINUS') 
	def expr(self, p): 
		return p.expr 

	@_('NAME') 
	def expr(self, p): 
		return ('var', p.NAME) 
	
	@_('NUMBER') 
	def expr(self, p): 
		return ('num', p.NUMBER)
class BasicExecute: 
	
	def __init__(self, tree, env): 
		self.env = env 
		self.nesting_level=0
		result = self.walkTree(tree)

		if result is not None and isinstance(result, int): 
			print(result) 

		if isinstance(result, str) and result[0] == '"': 
			print(result.replace('"',''))

	def walkTree(self, node): 

		if isinstance(node, int): 
			return node 
		if isinstance(node, str): 
			return node
		if node is None: 
			return None

		if node[0] == 'program': 
			if node[1] == None: 
				self.walkTree(node[2]) 
			else: 
				self.walkTree(node[1]) 
				self.walkTree(node[2]) 

		if node[0] == 'num': 
			return node[1]
		if node[0] == 'str': 
			return node[1]
		if node[0] == 'boolgreater': 
			if int(self.walkTree(node[1])) > int(self.walkTree(node[2])): 
				return True
			else:
				return False
		if node[0] == 'boolless': 
			if int(self.walkTree(node[1])) < int(self.walkTree(node[2])): 
				return True
			else:
				return False
		
		if node[0] == 'add': 
			return self.walkTree(node[1]) + self.walkTree(node[2]) 
		elif node[0] == 'sub': 
			return self.walkTree(node[1]) - self.walkTree(node[2]) 
		elif node[0] == 'mul': 
			return self.walkTree(node[1]) * self.walkTree(node[2]) 
		elif node[0] == 'power': 
			return self.walkTree(node[1]) ** self.walkTree(node[2]) 
		elif node[0] == 'div': 
			return self.walkTree(node[1]) / self.walkTree(node[2]) 
		elif node[0] == 'modulo': 
			return self.walkTree(node[1]) % self.walkTree(node[2])
		elif node[0] == 'factorial': 
			answer=1
			if self.walkTree(node[1])>=1:
				for i in range (1,int(self.walkTree(node[1]))+1):
					answer = answer * i
			return answer

		if node[0] == 'var_assign': 
			if ',' not in str(self.walkTree(node[2])): 
				self.env[node[1]] = self.walkTree(node[2]) 
			else:
				self.env[node[1]] = str(self.walkTree(node[2])).split(',')


			return (node[1])  
		if node[0] == 'var': 
			try: 
				return self.env[node[1]] 
			except LookupError:
				if 'exit' == node[1]:
					exit(1)
				else: 
					print("Undefined variable "+node[1]) 
				return "\n"
if __name__ == '__main__':
	lexer = BasicLexer() 
	parser = BasicParser() 
	env = {} 
	
	while True: 
		
		try: 
			text = input('Sapphire:> ')
			while ';' not in text:
				text2 = input('... ')
				text=text+text2
		
		except EOFError: 
			print("EOF error")
			break
		
		if text: 
			tree = parser.parse(lexer.tokenize(text)) 
			BasicExecute(tree, env)

