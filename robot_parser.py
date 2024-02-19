from tokens import tokenize


#Parsing functions 
def p_defvar(tokens):
    if len(tokens) != 5:
        return False
    
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'DEFVAR' and
        tokens[2].type == 'IDENTIFIER' and
        tokens[3].type == 'NUMBER' and
        tokens[4].type == 'RPAREN'):
        return True
    else:
        return False

def p_assign(tokens):
    if len(tokens) != 5:
        return False
    
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'ASSIGN' and
        tokens[2].type == 'IDENTIFIER' and
        tokens[3].type == 'NUMBER' and
        tokens[4].type == 'RPAREN'):
        return True
    else:
        return False
    
def p_move(tokens):
    if len(tokens) != 4:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'MOVE' and
        (tokens[2].type == 'NUMBER' or tokens[2].type == 'IDENTIFIER') and
        tokens[3].type == 'RPAREN'):
        return True
    else:
        return False
    
def p_skip(tokens):
    if len(tokens) != 4:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'SKIP' and
        (tokens[2].type == 'NUMBER' or tokens[2].type == 'IDENTIFIER') and
        tokens[3].type == 'RPAREN'):
        return True
    else:
        return False

def p_turn(tokens):
    if len(tokens) != 4:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'TURN' and
        tokens[2].type == 'DIRECTIONS' and
        tokens[3].type == 'RPAREN'):
        return True
    else:
        return False

def p_face(tokens):
    if len(tokens) != 4:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'FACE' and
        tokens[2].type == 'ORIENTATION' and
        tokens[3].type == 'RPAREN'):
        return True
    else:
        return False

def p_put(tokens):
    if len(tokens) != 5:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'PUT' and
        tokens[2].type == 'ITEM' and
        tokens[3].type == 'NUMBER' and
        tokens[4].type == 'RPAREN'):

        return True
    else:
        return False

def p_pick(tokens):
    if len(tokens) != 5:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'PICK' and
        tokens[2].type == 'ITEM' and
        tokens[3].type == 'NUMBER' and
        tokens[4].type == 'RPAREN'):

        return True
    else:
        return False

def p_move_dir(tokens):
    if len(tokens) != 5:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'MOVE_DIR' and
        tokens[2].type == 'NUMBER' and
        tokens[3].type == 'DIRECTIONS' and
        tokens[4].type == 'RPAREN'):

        return True
    else:
        return False
    
def p_run_dirs(tokens):
    if len(tokens) < 4: 
        return False

    if (tokens[0].type == 'LPAREN' and 
        tokens[1].type == 'RUN_DIRS' and 
        tokens[-1].type == 'RPAREN'):
        all_directions = all(token.type == 'DIRECTIONS' for token in tokens[2:-1])
        if all_directions:
            return True
        else:
            return False
    else:
        return False

def p_move_face(tokens):
    if len(tokens) != 5:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'MOVE_FACE' and
        (tokens[2].type == 'NUMBER' or tokens[2].type == 'IDENTIFIER') and
        tokens[3].type == 'ORIENTATION' and
        tokens[4].type == 'RPAREN'):

        return True
    else:
        return False
    
def p_null(tokens):
    if len(tokens) != 3:
        return False
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'NULL' and
        tokens[2].type == 'RPAREN'):
        return True
    else:
        return False

# Ends and Starts 
def index_blocks_conditions(tokens):
    lparen = 0
    rparen = 0
    index = 0
    for tok in tokens:
        if tok.type == 'LPAREN':
            lparen += 1
        elif tok.type == 'RPAREN':
            rparen += 1
        index += 1
        if lparen == rparen and lparen != 0:
            new_tokens = tokens[:index]
            return index, new_tokens

    return False

# Complex Strucutres Parsing 
def p_condition(tokens):
    if tokens[0].type != 'LPAREN':
        return False
    if (tokens[1].value == 'facing?' and
        tokens[2].type == 'ORIENTATION' and
        tokens[3].type == 'RPAREN'):
        return True 
    elif (tokens[1].value == 'blocked?' and
        tokens[2].type == 'RPAREN'):
        return True
    elif (tokens[1].value == 'can-put?' and
        tokens[2].type == 'ITEM' and 
        tokens[3].type == 'NUMBER'and
        tokens[4].type == 'RPAREN'):
        return True 
    elif (tokens[1].value == 'can-pick?'and
        tokens[2].type == 'ITEM' and
        tokens[3].type == 'NUMBER' and 
        tokens[4].type == 'RPAREN'):
        return True
    elif (tokens[1].value == 'can-move?'and
        tokens[2].type == 'ORIENTATION'and
        tokens[3].type == 'RPAREN'):
        return True
    elif (tokens[1].value == 'isZero?'and
        (tokens[2].type == 'NUMBER' or 
        tokens[2].type == 'IDENTIFIER') and 
        tokens[3].type == 'RPAREN'):
        return True
    elif (tokens[1].value == 'not'and
        tokens[2].type == 'CONDITION' and
        tokens[-1].type == 'RPAREN'):
        nested_tokens = tokens[2:-1]
        return p_condition(nested_tokens)
    return False
        
def p_blocks(tokens):
    if tokens[0].type != 'LPAREN':
        return False
    command_type = tokens[1].type
    parser_function = command_parsers.get(command_type)
    if parser_function:
        return parser_function(tokens)
    else:
        return False
    
def p_repeat(tokens):
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'REPEAT' and 
        tokens[2].type == 'NUMBER' and  
        tokens[-1].type == 'RPAREN'):
        nested_tokens = tokens[3:-1]
        return p_blocks(nested_tokens)
    return False

def p_loop(tokens):
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'LOOP' and   
        tokens[-1].type == 'RPAREN'):
        nested_tokens = tokens[2:-1]
        index, t_condition = index_blocks_conditions(nested_tokens)
        if p_condition(t_condition):
            nested_tokens = tokens[2+index:-1]
            return p_blocks(nested_tokens)
    return False
    
def p_if(tokens):
    if (tokens[0].type == 'LPAREN' and
        tokens[1].type == 'IF' and
        tokens[-1].type == 'RPAREN'):
        nested_tokens = tokens[2:-1]
        
        condition_end_index, condition_tokens = index_blocks_conditions(nested_tokens)
        if condition_end_index is None:  
            return False
        if not p_condition(condition_tokens):  
            return False
        first_block_start_index = condition_end_index
        b1_end_index, b1_tokens = index_blocks_conditions(nested_tokens[first_block_start_index:])
        if b1_end_index is None:  
            return False
        if not p_blocks(b1_tokens): 
            return False
        second_block_start_index = first_block_start_index + b1_end_index
        _, b2_tokens = index_blocks_conditions(nested_tokens[second_block_start_index:])
        if not p_blocks(b2_tokens): 
            return False
        return True
    return False


# Group Tokens 
def group_tokens_by_command(token_list):
    commands = []
    current_command = []
    depth = 0  

    for token in token_list:
        if token.type == 'LPAREN':
            depth += 1
            if depth == 1:
                current_command = [token] 
            else:
                current_command.append(token)
        elif token.type == 'RPAREN':
            depth -= 1
            current_command.append(token)
            if depth == 0:
                commands.append(current_command) 
        else:
            current_command.append(token)
    token_types_list = [[token.type for token in tokens_group] for tokens_group in commands]
    print(token_types_list)
    return commands

# Commands 
command_parsers = {
    'DEFVAR': p_defvar,
    'ASSIGN': p_assign,  
    'MOVE': p_move,
    'SKIP': p_skip,
    'TURN': p_turn,
    'FACE': p_face,
    'PUT': p_put,
    'PICK': p_pick,
    'MOVE_DIR': p_move_dir,
    'RUN_DIRS': p_run_dirs,
    'MOVE_FACE': p_move_face,
    'NULL': p_null,
    'IF': p_if, 
    'REPEAT' :p_repeat, 
    'LOOP' :p_loop
    
}
# Parsing function for a full program
def parse_program(input_text):
    tokens = tokenize(input_text)
    commands = group_tokens_by_command(tokens)
    #for tok in tokens:
        #print(tok)
    for command in commands:
        if command[1].type == 'DEFVAR' and not p_defvar(command):
            return False
        elif command[1].type == 'ASSIGN' and not p_assign(command):
            return False
        elif command[1].type == 'MOVE'and not p_move(command):
            return False
        elif command[1].type == 'SKIP'and not p_skip(command):
            return False
        elif command[1].type == 'TURN'and not p_turn(command):
            return False
        elif command[1].type == 'FACE'and not p_face(command):
            return False
        elif command[1].type == 'PUT'and not p_put(command):
            return False
        elif command[1].type == 'PICK'and not p_pick(command):
            return False
        elif command[1].type == 'MOVE_DIR'and not p_move_dir(command):
            return False
        elif command[1].type == 'RUN_DIRS'and not p_run_dirs(command):
            return False
        elif command[1].type == 'MOVE_FACE'and not p_move_face(command):
            return False
        elif command[1].type == 'NULL'and not p_null(command):
            return False
        elif command[1].type == 'REPEAT'and not p_repeat(command):
            return False
        elif command[1].type == 'IF'and not p_if(command):
            return False
        elif command[1].type == 'LOOP'and not p_loop(command):
            return False
    return True





