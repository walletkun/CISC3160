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
        TokenType.IDENTIFIER: r'[a-zA-Z_]\w*',
        TokenType.NUMBER: r'0|[1-9]\d*',
        TokenType.PLUS: r'\+',
        TokenType.MINUS: r'-',
        TokenType.MULTIPLY: r'\*',
        TokenType.LEFT_PAREN: r'\(',
        TokenType.RIGHT_PAREN: r'\)',
        TokenType.ASSIGNMENT: r'=',
        TokenType.SEMICOLON: r';',
    }

    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0

    def skip_whitespace(self):
        # Skip whitespace characters
        while self.position < len(self.source_code) and self.source_code[self.position].isspace():
            self.position += 1 # add poition by 1

    def check_leading_zeroes(self):
        if self.source_code[self.position] == '0' and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
            raise ValueError("Leading zeroes are not allowed")
    
    def tokenize(self):
        tokens = []
        while self.position < len(self.source_code):
            self.check_leading_zeroes()
            self.skip_whitespace()
            #print(f"Current position: {self.position}, Current character: {self.source_code[self.position]}")

            for token_type, pattern in self.PATTERNS.items():
                # Use re.match to match the pattern at the current position
                match = re.match(pattern, self.source_code[self.position:])
                if match:
                    # We have a match append it to the tokens list
                    value = match.group()
                    tokens.append(Token(token_type, value))
                    self.position += len(value)
    
        return tokens

if __name__ == '__main__':
    # Test cases to see if tokenizer works
    print("Test 1")
    source1  = 'x = 5;'
    tokenizer1 = Tokenizer(source1)
    tokens1 = tokenizer1.tokenize()
    print("Test 1: x = 5;")
    for token in tokens1:
        print(token)

    # More complex test
    print("Test 3")
    source3 = '(5 + x) * 3;'
    tokenizer3 = Tokenizer(source3)
    tokens3 = tokenizer3.tokenize()
    print("Test 3: result = (5 + x) * 3;")
    for token in tokens3:
        print(token)

    # Test case with invalid values
    print("Test 4")
    source= 'x = 001;'
    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    print("Test 4: x = 001;")
    for token in tokens:
        print(token)
        
        
        
    