from enum import Enum
from dataclasses import dataclass
from typing import Optional


class TokenType(Enum):
    """Token types for regex operators and literals"""
    CHAR = "CHAR"           # a, b, c, 0-9
    STAR = "STAR"           # *
    PLUS = "PLUS"           # +
    QUESTION = "QUESTION"   # ?
    OR = "OR"               # |
    LPAREN = "LPAREN"       # (
    RPAREN = "RPAREN"       # )
    DOT = "DOT"             # .
    EOF = "EOF"             # End of input


@dataclass
class Token:
    """Represents a single token in the regex"""
    type: TokenType
    value: str
    position: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', pos={self.position})"


class LexerError(Exception):
    """Raised when lexer encounters invalid input"""
    pass


class Lexer:
    """Tokenizes regular expression strings"""
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char: Optional[str] = self.text[0] if text else None
    
    def error(self, msg: str):
        """Raise lexer error with position information"""
        raise LexerError(f"Lexer error at position {self.pos}: {msg}")
    
    def advance(self):
        """Move to next character"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Look ahead at next character without consuming it"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def get_next_token(self) -> Token:
        """Get the next token from input"""
        # Skip whitespace (if we want to support it later)
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        
        # End of input
        if self.current_char is None:
            return Token(TokenType.EOF, '', self.pos)
        
        # Current position for token
        pos = self.pos
        char = self.current_char
        
        # Single character operators
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
        
        # Invalid character
        self.error(f"Invalid character '{char}'")
    
    def tokenize(self) -> list[Token]:
        """Tokenize entire input and return list of tokens"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


# Helper function for easy testing
def tokenize(regex: str) -> list[Token]:
    """Convenience function to tokenize a regex string"""
    lexer = Lexer(regex)
    return lexer.tokenize()