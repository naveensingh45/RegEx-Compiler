import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nfa import build_nfa, NFAState
from src.visualizer import visualize_nfa

print("NFA Visualization Tests")
# Create output directory
output_dir = "examples/outputs"
os.makedirs(output_dir, exist_ok=True)

test_patterns = [
    ("a", "single_char"),
    ("ab", "concat"),
    ("a|b", "union"),
    ("a*", "star"),
    ("a+", "plus"),
    ("a?", "question"),
    ("(a|b)*", "star_on_union"),
    ("(a|b)*c+", "complex"),
]

print("\nGenerating NFA visualizations...")
print(f"Output directory: {output_dir}\n")

for pattern, name in test_patterns:
    print(f"Pattern '{pattern}' → {name}.png")
    NFAState.reset_counter()
    nfa = build_nfa(pattern)
    
    if nfa:
        filepath = os.path.join(output_dir, f"nfa_{name}")
        visualize_nfa(nfa, filepath, view=False)

print("NFA Visualization successfully generated for all test patterns")