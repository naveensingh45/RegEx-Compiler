from src.lexer import Lexer, TokenType

print("LEXER TESTS")
# Test cases
test_patterns = [
    ("a", "Single character"),
    ("ab", "Concatenation"),
    ("abc", "Multiple concatenation"),
    ("a*", "Kleene star"),
    ("a+", "Plus operator"),
    ("a?", "Question mark"),
    ("a|b", "Alternation"),
    ("(ab)", "Parentheses"),
    ("(a|b)*", "Grouped alternation with star"),
    ("(a|b)*c+", "Complex pattern"),
]

for pattern, description in test_patterns:
    print(f"\n{description}: '{pattern}'")
    lexer = Lexer(pattern)
    tokens = lexer.tokenize()
    
    print("  Tokens: ", end="")
    for token in tokens[:-1]: 
        print(f"{token.type.name}({token.value}) ", end="")
    print()
print("\nSuccessfull tokenization")