import ply.lex as lex

# Reserved words
reserved = {
    'defvar': 'DEFVAR', 'move': 'MOVE', 'skip' : 'SKIP', 
    'turn':'TURN', 'face':'FACE', 'put': 'PUT', 'pick':'PICK', 
    'null':'NULL', 'if': 'IF', 'loop':'LOOP', 'repeat':'REPEAT', 'defun':'DEFUN'
}

tokens = [
    'LPAREN', 'RPAREN',
    'IDENTIFIER', 'NUMBER', 'ASSIGN', 'DIRECTION', 'ORIENTATION', 
    'ITEM', 'MOVE_DIR', 'RUN_DIRS', 'DIRECTIONS', 'MOVE_FACE', 'CONDITION', 'CONSTANT'
] + list(reserved.values())

# Regular expressions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_DIRECTION = r':left|:right|:around|:down|:up'
t_ORIENTATION = r':north|:south|:east|:west'
t_ITEM = r':balloons|:chips'
t_DIRECTIONS = r':front|:left|:right|:back'
t_NUMBER = r'\d+'
t_ignore = ' \t'

def t_CONSTANT(t):
    r'(Dim|myXpos|myYpos|myChips|myBalloons|balloonsHere|ChipsHere|Spaces)'
    return t

def t_CONDITION(t):
    r'(facing\?|blocked\?|can\-put\?|can\-pick\?|can\-move\?|isZero\?|not)'
    return t

def t_MOVE_FACE(t):
    r'move-face'
    return t

def t_MOVE_DIR(t):
    r'move-dir'
    return t

def t_RUN_DIRS(t):
    r'run-dirs'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER') 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def tokenize(input_text):
    lexer.input(input_text)
    return [token for token in lexer]


