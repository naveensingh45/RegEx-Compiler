import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.nfa import build_nfa, NFAState

print("Testing NFA construction")
test_patterns = [
    ("a", "Single character"),
    ("ab", "Concatenation"),
    ("a|b", "Alternation"),
    ("a*", "Kleene star"),
    ("a+", "Plus"),
    ("a?", "Question"),
    ("(a|b)*", "Star on union"),
    ("(a|b)*c+", "Complex pattern"),
]

for pattern, description in test_patterns:
    print(f"\n{description}: '{pattern}'")
    NFAState.reset_counter()  # Reset for clean IDs
    nfa = build_nfa(pattern)
    
    if nfa is None:
        print("  NFA: None (empty regex)")
        continue
    
    print(f"  {nfa}")
    print(f"  States: {len(nfa.states)}")
    print(f"  Alphabet: {nfa.get_alphabet()}")
    print(f"  Start: State{nfa.start.id}")
    print(f"  Accept: State{nfa.accept.id}")
    
    # Show transitions
    print("  Transitions:")
    for state in sorted(nfa.states, key=lambda s: s.id):
        if state.transitions:
            for symbol, next_states in state.transitions.items():
                symbol_str = 'ε' if symbol is None else symbol
                for next_state in next_states:
                    print(f"    State{state.id} --{symbol_str}--> State{next_state.id}")
print("NFA TESTED SUCCESSFULLY")