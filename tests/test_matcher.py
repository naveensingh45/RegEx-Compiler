"""Manual test for Matcher - Run and verify matching"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nfa import build_nfa, NFAState
from src.dfa import nfa_to_dfa, DFAState
from src.matcher import Matcher

print("PATTERN MATCHING TESTS")

# Test cases: (pattern, test_strings)
test_cases = [
    ("a", {
        "should accept": ["a"],
        "should reject": ["", "b", "aa", "ab"]
    }),
    ("ab", {
        "should accept": ["ab"],
        "should reject": ["", "a", "b", "ba", "aab", "abb"]
    }),
    ("a|b", {
        "should accept": ["a", "b"],
        "should reject": ["", "ab", "ba", "aa", "bb"]
    }),
    ("a*", {
        "should accept": ["", "a", "aa", "aaa", "aaaa"],
        "should reject": ["b", "ab", "ba", "aaab"]
    }),
    ("a+", {
        "should accept": ["a", "aa", "aaa"],
        "should reject": ["", "b", "ab"]
    }),
    ("(a|b)*", {
        "should accept": ["", "a", "b", "aa", "ab", "ba", "bb", "aab", "aba"],
        "should reject": ["c", "ac", "abc"]
    }),
    ("(a|b)*abb", {
        "should accept": ["abb", "aabb", "babb", "aaabb", "ababb", "baabb"],
        "should reject": ["", "a", "ab", "abab", "abbb"]
    }),
]

for pattern, tests in test_cases:
    print(f"Pattern: '{pattern}'")
    
    # Build automaton
    NFAState.reset_counter()
    DFAState.reset_counter()
    nfa = build_nfa(pattern)
    dfa = nfa_to_dfa(nfa)
    matcher = Matcher(dfa)
    
    print(f"DFA: {len(dfa.states)} states, {len(dfa.alphabet)} symbols")
    
    # Test strings that should be accepted
    print("\nShould ACCEPT:")
    for test_string in tests["should accept"]:
        result = matcher.match(test_string)
        status = "✓" if result else "FAIL"
        display = f'"{test_string}"' if test_string else '""(empty)'
        print(f"  {display:20} → {status}")
    
    # Test strings that should be rejected
    print("\nShould REJECT:")
    for test_string in tests["should reject"]:
        result = matcher.match(test_string)
        status = "✓" if not result else "FAIL"
        display = f'"{test_string}"' if test_string else '""(empty)'
        print(f"  {display:20} → {status}")

print("DETAILED TRACE EXAMPLES")

# Show detailed traces for some examples
trace_examples = [
    ("(a|b)*abb", "abb"),
    ("(a|b)*abb", "aabb"),
    ("(a|b)*abb", "ab"),
    ("a*", "aaa"),
]

for pattern, test_string in trace_examples:
    print(f"\nPattern: '{pattern}' | Input: '{test_string}'")
    print("-" * 60)
    
    NFAState.reset_counter()
    DFAState.reset_counter()
    nfa = build_nfa(pattern)
    dfa = nfa_to_dfa(nfa)
    matcher = Matcher(dfa)
    
    result = matcher.match_with_trace(test_string)
    for line in result.trace:
        print(f"  {line}")
print("All matching tests complete!")
