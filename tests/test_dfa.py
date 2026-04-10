"""Manual test for DFA - Run and visually verify output"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nfa import build_nfa, NFAState
from src.dfa import nfa_to_dfa, DFAState
from src.visualizer import visualize_nfa, visualize_dfa

print("DFA CONVERSION TESTS")


# Create output directory
output_dir = "examples/outputs"
os.makedirs(output_dir, exist_ok=True)

test_patterns = [
    ("a", "single_char"),
    ("ab", "concat"),
    ("a|b", "union"),
    ("a*", "star"),
    ("(a|b)*", "star_on_union"),
    ("(a|b)*c", "complex"),
]

for pattern, name in test_patterns:
    print(f"\n{'='*60}")
    print(f"Pattern: '{pattern}'")
    print(f"{'='*60}")
    
    # Build NFA
    NFAState.reset_counter()
    nfa = build_nfa(pattern)
    print(f"NFA: {nfa}")
    print(f"  States: {len(nfa.states)}")
    print(f"  Alphabet: {nfa.get_alphabet()}")
    
    # Convert to DFA
    DFAState.reset_counter()
    dfa = nfa_to_dfa(nfa)
    print(f"\nDFA: {dfa}")
    print(f"  States: {len(dfa.states)}")
    print(f"  Reduction: {len(nfa.states)} → {len(dfa.states)} states")
    
    # Show DFA transitions
    print(f"\nDFA Transitions:")
    for state in sorted(dfa.states, key=lambda s: s.id):
        nfa_ids = sorted([s.id for s in state.nfa_states])
        accept_str = " (ACCEPT)" if state.is_accept else ""
        print(f"  State {state.id} {nfa_ids}{accept_str}")
        for symbol, next_state in sorted(state.transitions.items()):
            print(f"    --{symbol}--> State {next_state.id}")
    
    # Visualize both
    nfa_file = os.path.join(output_dir, f"nfa_{name}")
    dfa_file = os.path.join(output_dir, f"dfa_{name}")
    
    visualize_nfa(nfa, nfa_file)
    visualize_dfa(dfa, dfa_file)
print("✓ All DFA conversions complete!")

