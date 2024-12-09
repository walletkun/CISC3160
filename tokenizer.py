import re
from enum import Enum,auto


class TokenType(Enum):
    # For variables like 'x', 'y', 'counter', etc.
    IDENTIFIER = auto()

    # For numbers like '123', '0', not floating numbers like '1.23', etc.
    NUMBER = auto()

    # Operators
    PLUS = auto() # '+'
    MINUS = auto() # '-'
    MULTIPLY = auto() # '*'

    # Other symbols
    LEFT_PAREN = auto() # '('
    RIGHT_PAREN = auto() # ')'
    ASSIGNMENT = auto() # '='
    SEMICOLON = auto() # ';'

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type # This will be from our TokenType class
        
        self.value = value  # This will be the actual value of the token

    def __str__(self):
        return f'TOKEN({self.token_type.name}, {self.value})'


class Tokenizer:
    # Store patterns as class variables
    # We use r'' to make it a raw string
    PATTERNS = {
        TokenType.ASSIGNMENT: r'=',
        TokenType.SEMICOLON: r';',
        TokenType.LEFT_PAREN: r'\(',
        TokenType.RIGHT_PAREN: r'\)',
        TokenType.PLUS: r'\+',
        TokenType.MINUS: r'-',
        TokenType.MULTIPLY: r'\*',
        TokenType.IDENTIFIER: r'[a-zA-Z_]\w*',
        TokenType.NUMBER: r'0|[1-9][0-9]*',
    }

    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.last_token = None

    def skip_whitespace(self):
        # Skip whitespace characters
        while self.position < len(self.source_code) and self.source_code[self.position].isspace():
            self.position += 1 # add poition by 1

    def check_leading_zeroes(self):
        if self.source_code[self.position] == '0' and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
            raise ValueError("Leading zeroes are not allowed")

    def checking_semicolon(self):
        # We first skip any whitespace
        self.skip_whitespace()

        # we're at the next character
        if self.position < len(self.source_code):
            # If we just saw a semicolon
            if self.last_token and self.last_token.value == ';':
                # Next character cannot be another semicolon
                if self.source_code[self.position] == ';':
                    raise ValueError("Two semicolons in a row are not allowed")

            # Check for missing semicolon between statements
            if self.source_code[self.position].isalpha() or self.source_code[self.position].isdigit() and self.last_token and self.last_token.value != ';':
                if self.position == len(self.source_code) - 1 or self.source_code[self.position] == ';':
                    raise ValueError("Missing semicolon between statements")
            
            if self.position == len(self.source_code) - 1 and self.source_code[self.position] != ';':
                    raise ValueError("Missing final semicolon")
            self.position += 1
    
    def tokenize(self):
        tokens = []
        while self.position < len(self.source_code):
            self.check_leading_zeroes()
            self.skip_whitespace()
            #print(f"Current position: {self.position}, Current character: {self.source_code[self.position]}")

            match_found = False
            for token_type, pattern in self.PATTERNS.items():
                # Use re.match to match the pattern at the current position
                match = re.match(pattern, self.source_code[self.position:])
                if match:
                    # We have a match append it to the tokens list
                    value = match.group()
                    token = Token(token_type, value)
                    tokens.append(token)
                    self.position += len(value)
                    self.last_token = token
                    print(f"Matched: {token}")  # Debug print
                    match_found = True
                    break
                
            if not match_found:
                raise ValueError(f"Invalid character: {self.source_code[self.position]}")
            
        self.checking_semicolon()
        return tokens 

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self, symbol_table):
        while self.position < len(self.tokens):
            self.parse_assignment(symbol_table)

    def parse_assignment(self, symbol_table):
        # Expects an identifier
        if self.tokens[self.position].token_type != TokenType.IDENTIFIER:
            raise ValueError("Expected identifier")

        variable_name = self.tokens[self.position].value
        self.position += 1

        # Expects an assignment operator
        if self.tokens[self.position].token_type != TokenType.ASSIGNMENT:
            raise ValueError("Expected assignment operator")
        self.position += 1

        # Parse the expression
        value = self.parse_expression(symbol_table)

        # Expect a semicolon
        if self.tokens[self.position].token_type != TokenType.SEMICOLON:
            raise ValueError("Expected semicolon")
        self.position += 1

        # Store the result in the symbol table
        symbol_table[variable_name] = value.evaluate(symbol_table)

    
    def parse_term(self, symbol_table):
        left = self.parse_fact(symbol_table)

        while self.position < len(self.tokens) and self.tokens[self.position].token_type == TokenType.MULTIPLY:
            operator = self.tokens[self.position].token_type
            self.position += 1
            right = self.parse_fact(symbol_table)
            left = BinaryExpression(left, operator, right)

            
        return left

    def parse_fact(self, symbol_table):
        token = self.tokens[self.position]
        if token.token_type == TokenType.LEFT_PAREN:
            self.position += 1
            expr = self.parse_expression(symbol_table)
            if self.tokens[self.position].token_type != TokenType.RIGHT_PAREN:
                raise ValueError("Expected right parenthesis")
            self.position += 1
            return expr
        elif token.token_type == TokenType.NUMBER:
            self.position += 1
            return LiteralExpression(int(token.value))
        elif token.token_type == TokenType.IDENTIFIER:
            self.position += 1
            return VariableExpression(token.value)

        elif token.token_type in (TokenType.PLUS, TokenType.MINUS):
            self.position +=1
            operand = self.parse_fact(symbol_table)
            return UrnaryExpression(token.token_type, operand)
        else:
            raise ValueError("Invalid expression")
        
        
    def parse_expression(self, symbol_table):
        left = self.parse_term(symbol_table)

        while self.position < len(self.tokens) and self.tokens[self.position].token_type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.tokens[self.position].token_type
            self.position += 1
            right = self.parse_term(symbol_table)
            left = BinaryExpression(left, operator, right)
            
        return left

class UrnaryExpression:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, symbol_table):
        value = self.operand.evaluate(symbol_table)
        if self.operator == TokenType.PLUS:
            return value
        elif self.operator == TokenType.MINUS:
            return -value
        else:
            raise ValueError("Invalid operator")

class LiteralExpression:
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        return int(self.value)

class VariableExpression:
    def __init__(self, identifier):
        self.identifier = identifier

    def evaluate(self, symbol_table):
        if self.identifier not in symbol_table:
            raise ValueError(f"Undefined variable: {self.identifier}")
        return symbol_table[self.identifier]

    

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, symbol_table):
        left_value = self.left.evaluate(symbol_table)
        right_value = self.right.evaluate(symbol_table)

        if self.operator == TokenType.PLUS:
            return left_value + right_value
        elif self.operator == TokenType.MINUS:
            return left_value - right_value
        elif self.operator == TokenType.MULTIPLY:
            return left_value * right_value
        else:
            raise ValueError("Invalid operator")
        
if __name__ == '__main__':
    # # Test cases to see if tokenizer works
    # print("Test 1")
    # source1  = 'x = 5;'
    # tokenizer1 = Tokenizer(source1)
    # tokens1 = tokenizer1.tokenize()
    # print("Test 1: x = 5;")
    # for token in tokens1:
    #     print(token)

    # # More complex test
    # print("Test 3")
    # source3 = '(5 + x) * 3;'
    # tokenizer3 = Tokenizer(source3)
    # tokens3 = tokenizer3.tokenize()
    # print("Test 3: result = (5 + x) * 3;")
    # for token in tokens3:
    #     print(token)

    # # Test case with invalid values
    # print("Test 4")
    # source= 'x = 001;'
    # tokenizer = Tokenizer(source)
    # tokens = tokenizer.tokenize()
    # print("Test 4: x = 001;")
    # for token in tokens:
    #     print(token)
        
    # print("Test 5")
    # source= 'x = 5'
    # tokenizer = Tokenizer(source)
    # tokens = tokenizer.tokenize()
    # print("Test 5: x = 5")
    # for token in tokens:
    #     print(token)

    # print("Test 6")
    # source = "x = 5;; y = 5;"  # One string with both statements
    # tokenizer = Tokenizer(source)
    # tokens = tokenizer.tokenize()

    # print("Test 6: x = 5;; y = 5;")
    # for token in tokens:
    #     print(token)

   # Test cases
    test_cases = [
        "x = 5; y = 3; z = (x + y) * 2;",
        "a = 10; b = -5; c = a * b;",
        "p = 20; q = 4; r = (p - q) * (p + q);",
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test}")
        try:
            tokenizer = Tokenizer(test)
            tokens = tokenizer.tokenize()
            print("Tokens:", " ".join(str(token) for token in tokens))

            symbol_table = {}
            parser = Parser(tokens)
            parser.parse(symbol_table)

            print("Symbol Table:")
            for var, value in symbol_table.items():
                print(f"{var} = {value}")
        except Exception as e:
            print("Error:", str(e))
