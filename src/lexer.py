from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TokenType(Enum):
    CHAR= "CHAR"           # a,b,c,0-9
    STAR= "STAR"           # *
    PLUS= "PLUS"           # +
    QUESTION= "QUESTION"   # ?
    OR= "OR"               # |
    LPAREN= "LPAREN"       # (
    RPAREN= "RPAREN"       # )
    DOT= "DOT"             # .
    EOF= "EOF"             # End of input

@dataclass
class Token:
    type: TokenType
    value: str
    position: int
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"

class LexerError(Exception):
    pass

class Lexer:
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char: Optional[str] = self.text[0] if text else None
    
    def error(self, msg: str):
        raise LexerError(f"Lexer error at position {self.pos}: {msg}")
    
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def get_next_token(self) -> Token:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        
        # End of input
        if self.current_char is None:
            return Token(TokenType.EOF, '', self.pos)
        
        pos = self.pos
        char = self.current_char
        
        if char == '*':
            self.advance()
            return Token(TokenType.STAR, '*', pos)
        
        if char == '+':
            self.advance()
            return Token(TokenType.PLUS, '+', pos)
        
        if char == '?':
            self.advance()
            return Token(TokenType.QUESTION, '?', pos)
        
        if char == '|':
            self.advance()
            return Token(TokenType.OR, '|', pos)
        
        if char == '(':
            self.advance()
            return Token(TokenType.LPAREN, '(', pos)
        
        if char == ')':
            self.advance()
            return Token(TokenType.RPAREN, ')', pos)
        
        if char == '.':
            self.advance()
            return Token(TokenType.DOT, '.', pos)
        
        # Alphanumeric characters
        if char.isalnum():
            self.advance()
            return Token(TokenType.CHAR, char, pos)
        
        # Invalid
        self.error(f"Invalid character '{char}'")
    
    def tokenize(self) -> list[Token]:
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

# Helper function
def tokenize(regex: str) -> list[Token]:
    lexer = Lexer(regex)
    return lexer.tokenize()