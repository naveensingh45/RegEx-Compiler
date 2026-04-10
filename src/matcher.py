from typing import List, Tuple, Optional
from src.dfa import DFA, DFAState


class MatchResult:
    def __init__(self, accepted: bool, trace: List[str]):
        self.accepted = accepted
        self.trace = trace
    
    def __repr__(self):
        status = "ACCEPT ✓" if self.accepted else "REJECT ✗"
        return f"MatchResult({status})"


class Matcher:
    
    def __init__(self, dfa: DFA):
        self.dfa = dfa
    
    def match(self, input_string: str) -> bool:
        
        current_state = self.dfa.start
        
        for char in input_string:
            # Check if transition exists
            if char not in current_state.transitions:
                return False
            
            # Move to next state
            current_state = current_state.transitions[char]
        
        # Accept if we end in an accept state
        return current_state.is_accept
    
    def match_with_trace(self, input_string: str) -> MatchResult:

        trace = []
        current_state = self.dfa.start
        
        # Show starting state
        nfa_ids = sorted([s.id for s in current_state.nfa_states])
        trace.append(f"Start: State {current_state.id} {nfa_ids}")
        
        # Process each character
        for i, char in enumerate(input_string):
            if char not in current_state.transitions:
                trace.append(f"Step {i+1}: '{char}' - No transition available")
                trace.append("Result: REJECT ✗ (no valid transition)")
                return MatchResult(False, trace)
            
            # Move to next state
            next_state = current_state.transitions[char]
            nfa_ids = sorted([s.id for s in next_state.nfa_states])
            trace.append(f"Step {i+1}: '{char}' → State {next_state.id} {nfa_ids}")
            current_state = next_state
        
        # Check if we're in accept state
        if current_state.is_accept:
            trace.append("Result: ACCEPTED  (reached accept state)")
            return MatchResult(True, trace)
        else:
            trace.append("Result: REJECTED  (not in accept state)")
            return MatchResult(False, trace)
    
    def match_multiple(self, test_strings: List[str]) -> List[Tuple[str, bool]]:
    
        results = []
        for string in test_strings:
            accepted = self.match(string)
            results.append((string, accepted))
        return results


def match_pattern(regex: str, input_string: str, show_trace: bool = False) -> bool:

    from src.nfa import build_nfa
    from src.dfa import nfa_to_dfa
    
    # Build NFA and convert to DFA
    nfa = build_nfa(regex)
    if nfa is None:
        return False
    
    dfa = nfa_to_dfa(nfa)
    matcher = Matcher(dfa)
    
    # Match with or without trace
    if show_trace:
        result = matcher.match_with_trace(input_string)
        for line in result.trace:
            print(f"  {line}")
        return result.accepted
    else:
        return matcher.match(input_string)