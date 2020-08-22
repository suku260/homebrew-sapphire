from sly import Lexer
from sly import Parser
class EmeraldLexer(Lexer): 
	tokens = { ADD, ALTER, COLUMN, TABLE, ALL, ANY, CREATE, DATABASE, DROP, FOREIGN_KEY, PRIMARY_KEY, JOIN, NOT, NULL, OR, SELECT, FROM ,UPDATE, WHERE }
	literals= {'*',';','>','<'}
	ignore = '\t '
	@_(r';.*') 
	def EOL(self, t): 
		pass
	@_(r'\n+') 
	def newline(self, t): 
		self.lineno = t.value.count('\n')
class BasicParser(Parser): 
	#tokens are passed from lexer to parser 
	tokens = EmeraldLexer.tokens 
	def __init__(self): 
		self.env = { } 

	@_('') 
	def statement(self, p): 
		pass
	
class BasicExecute: 
	
	def __init__(self, tree, env): 
		self.env = env 
		self.nesting_level=0
		result = self.walkTree(tree)

		if result is not None and isinstance(result, int): 
			print(result) 

		if isinstance(result, str) and result[0] == '"': 
			print(result)
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
if __name__ == '__main__':
	lexer = EmeraldLexer() 
	parser = BasicParser() 
	env = {} 
	while True: 
		
		try: 
			text = input('Emerald:> ')
			while ';' not in text:
				text2 = input('... ')
				text=text+text2
		
		except EOFError: 
			print("EOF error")
			break
		
		if text: 
			tree = parser.parse(lexer.tokenize(text)) 
			BasicExecute(tree, env)