from typing import Set, Dict, FrozenSet, Optional
from src.nfa import NFA, NFAState


class DFAState:
    _id_counter = 0
    
    def __init__(self, nfa_states: FrozenSet[NFAState], is_accept: bool = False):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.nfa_states = nfa_states  # Set of NFA states this DFA state represents
        self.is_accept = is_accept
        self.transitions: Dict[str, 'DFAState'] = {}  # {symbol: DFAState}
    
    def add_transition(self, symbol: str, state: 'DFAState'):
        self.transitions[symbol] = state
    
    def __repr__(self):
        nfa_ids = sorted([s.id for s in self.nfa_states])
        return f"DState{self.id}{nfa_ids}{'(accept)' if self.is_accept else ''}"
    
    def __hash__(self):
        return hash(self.nfa_states)
    
    def __eq__(self, other):
        return isinstance(other, DFAState) and self.nfa_states == other.nfa_states
    
    @classmethod
    def reset_counter(cls):
        cls._id_counter = 0


class DFA:
    def __init__(self, start: DFAState, states: Set[DFAState], alphabet: Set[str]):
        self.start = start
        self.states = states
        self.alphabet = alphabet
    
    def __repr__(self):
        accept_count = sum(1 for s in self.states if s.is_accept)
        return f"DFA(states={len(self.states)}, accept={accept_count}, alphabet={self.alphabet})"


class DFAConverter:
    
    def __init__(self):
        DFAState.reset_counter()
    
    def convert(self, nfa: NFA) -> DFA:
        alphabet = nfa.get_alphabet()
        
        # Step 1: Start with epsilon-closure of NFA start state
        start_closure = self._epsilon_closure({nfa.start}, nfa)
        start_dfa = DFAState(start_closure, self._contains_accept(start_closure))
        
        # Track DFA states
        dfa_states = {start_dfa}
        unmarked = [start_dfa]
        state_map = {start_closure: start_dfa}  # Map NFA state sets to DFA states
        
        # Step 2: Process each unmarked state
        while unmarked:
            current = unmarked.pop(0)
            
            # For each symbol in alphabet
            for symbol in alphabet:
                # Compute move(current, symbol)
                moved = self._move(current.nfa_states, symbol)
                
                # Compute epsilon-closure of result
                closure = self._epsilon_closure(moved, nfa)
                
                if not closure:
                    continue
                
                # Create new DFA state if needed
                if closure not in state_map:
                    is_accept = self._contains_accept(closure)
                    new_state = DFAState(closure, is_accept)
                    state_map[closure] = new_state
                    dfa_states.add(new_state)
                    unmarked.append(new_state)
                
                # Add transition
                current.add_transition(symbol, state_map[closure])
        
        return DFA(start_dfa, dfa_states, alphabet)
    
    def _epsilon_closure(self, states: Set[NFAState], nfa: NFA) -> FrozenSet[NFAState]:
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            
            # Check for epsilon transitions (None symbol)
            if None in state.transitions:
                for next_state in state.transitions[None]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        
        return frozenset(closure)
    
    def _move(self, states: FrozenSet[NFAState], symbol: str) -> Set[NFAState]:
        result = set()
        
        for state in states:
            if symbol in state.transitions:
                result.update(state.transitions[symbol])
        
        return result
    
    def _contains_accept(self, states: FrozenSet[NFAState]) -> bool:
        return any(state.is_accept for state in states)


def nfa_to_dfa(nfa: NFA) -> DFA:
    converter = DFAConverter()
    return converter.convert(nfa)