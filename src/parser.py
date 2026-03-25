from typing import Optional, List
from src.lexer import Token, TokenType, Lexer

# AST Node Classes
class ASTNode:
    pass

class CharNode(ASTNode):
    def __init__(self, char: str):
        self.char = char
    
    def __repr__(self):
        return f"Char({self.char})"


class ConcatNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Concat({self.left}, {self.right})"


class UnionNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Union({self.left}, {self.right})"


class StarNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child
    
    def __repr__(self):
        return f"Star({self.child})"


class PlusNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child
    
    def __repr__(self):
        return f"Plus({self.child})"


class QuestionNode(ASTNode):
    def __init__(self, child: ASTNode):
        self.child = child
    
    def __repr__(self):
        return f"Question({self.child})"


class ParserError(Exception):
    pass


class Parser:
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, msg: str):
        raise ParserError(f"Parse error at position {self.pos}: {msg}")
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def parse(self) -> Optional[ASTNode]:
        """Entry point - parse tokens and return AST"""
        if self.current_token.type == TokenType.EOF:
            return None
        return self.expr()
    
    def expr(self) -> ASTNode:
        """
        Handle alternation (|) - lowest precedence
        expr → term ('|' term)*
        """
        left = self.term()
        
        while self.current_token and self.current_token.type == TokenType.OR:
            self.advance()  # consume '|'
            right = self.term()
            left = UnionNode(left, right)
        
        return left
    
    def term(self) -> ASTNode:
        """
        Handle concatenation (implicit) - higher precedence
        term → factor+
        """
        factors = []
        
        # Collect all factors that should be concatenated
        while (self.current_token and 
               self.current_token.type not in [TokenType.EOF, TokenType.OR, TokenType.RPAREN]):
            factors.append(self.factor())
        
        if not factors:
            self.error("Expected at least one factor")
        
        # Build left-associative concatenation tree
        result = factors[0]
        for factor in factors[1:]:
            result = ConcatNode(result, factor)
        
        return result
    
    def factor(self) -> ASTNode:
        """
        Handle quantifiers (*, +, ?) - highest precedence
        factor → primary ('*'|'+'|'?')?
        """
        node = self.primary()
        
        if self.current_token:
            if self.current_token.type == TokenType.STAR:
                self.advance()
                return StarNode(node)
            elif self.current_token.type == TokenType.PLUS:
                self.advance()
                return PlusNode(node)
            elif self.current_token.type == TokenType.QUESTION:
                self.advance()
                return QuestionNode(node)
        
        return node
    
    def primary(self) -> ASTNode:
        """
        Handle basic elements: characters and grouped expressions
        primary → CHAR | '(' expr ')'
        """
        token = self.current_token
        
        if token.type == TokenType.CHAR:
            self.advance()
            return CharNode(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.advance()  # consume '('
            node = self.expr()  # parse inside parentheses
            
            if not self.current_token or self.current_token.type != TokenType.RPAREN:
                self.error("Expected ')' to match '('")
            
            self.advance()  # consume ')'
            return node
        
        else:
            self.error(f"Unexpected token {token.type}")


def parse(regex: str) -> Optional[ASTNode]:
    lexer = Lexer(regex)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()