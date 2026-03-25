from src.parser import parse, ParserError

def print_ast(node, prefix="", is_last=True):
    if node is None:
        return

    connector = "└── " if is_last else "├── "
    print(prefix + connector + str(node.value if hasattr(node, "value") else node))

    prefix += "    " if is_last else "│   "

    children = []
    
    # Adjust based on your AST structure
    if hasattr(node, "left") and node.left:
        children.append(node.left)
    if hasattr(node, "right") and node.right:
        children.append(node.right)
    if hasattr(node, "child") and node.child:
        children.append(node.child)

    for i, child in enumerate(children):
        print_ast(child, prefix, i == len(children) - 1)

print("PARSER TESTS")
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
    ("(a|b)", "Grouped alternation"),
    ("(a|b)*", "Star on group"),
    ("ab*", "Star precedence"),
    ("ab|cd", "Alternation with concat"),
    ("(a|b)c+d*", "Complex pattern"),
    ("a|b|c", "Multiple alternations"),
]

for pattern, description in test_patterns:
    print(f"\n{description}: '{pattern}'")
    ast = parse(pattern)
    print("  AST Tree:")
    print_ast(ast)

# Error test cases
error_patterns = [
    ("(ab", "Unmatched left paren"),
    ("", "Empty string (should return None)"),
]

for pattern, description in error_patterns:
    print(f"\n{description}: '{pattern}'")
    try:
        ast = parse(pattern)
        if ast is None:
            print(f"  Result: None (empty regex)")
        else:
            print("  AST Tree:")
            print_ast(ast)
    except ParserError as e:
        print(f"  ✓ Error caught: {e}")

print("\n Successfull Parsing")
