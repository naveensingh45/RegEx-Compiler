from typing import Optional, Set, Dict, List
from src.parser import (
    ASTNode, CharNode, ConcatNode, UnionNode, 
    StarNode, PlusNode, QuestionNode
)


class NFAState:
    _id_counter = 0  # For generating unique IDs
    
    def __init__(self, is_accept: bool = False):
        self.id = NFAState._id_counter
        NFAState._id_counter += 1
        self.is_accept = is_accept
        # transitions: {symbol: [list of states]} or {None: [states]} for epsilon
        self.transitions: Dict[Optional[str], List['NFAState']] = {}
    
    def add_transition(self, symbol: Optional[str], state: 'NFAState'):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)
    
    def __repr__(self):
        return f"State{self.id}{'(accept)' if self.is_accept else ''}"
    
    @classmethod
    def reset_counter(cls):
        cls._id_counter = 0


class NFA:
    
    def __init__(self, start: NFAState, accept: NFAState):
        self.start = start
        self.accept = accept
        self.states: Set[NFAState] = set()
        self._collect_states()
    
    def _collect_states(self):
        visited = set()
        stack = [self.start]
        
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            self.states.add(state)
            
            # Add all reachable states
            for next_states in state.transitions.values():
                for next_state in next_states:
                    if next_state not in visited:
                        stack.append(next_state)
        
        # Make sure accept state is included
        self.states.add(self.accept)
    
    def get_alphabet(self) -> Set[str]:
        alphabet = set()
        for state in self.states:
            for symbol in state.transitions.keys():
                if symbol is not None:  # Skip epsilon
                    alphabet.add(symbol)
        return alphabet
    
    def __repr__(self):
        return f"NFA(states={len(self.states)}, start={self.start.id}, accept={self.accept.id})"


class NFABuilder:
    
    def __init__(self):
        NFAState.reset_counter()
    
    def build(self, ast: Optional[ASTNode]) -> Optional[NFA]:
        if ast is None:
            return None
        return self._visit(ast)
    
    def _visit(self, node: ASTNode) -> NFA:
        if isinstance(node, CharNode):
            return self._char_nfa(node.char)
        elif isinstance(node, ConcatNode):
            return self._concat_nfa(node.left, node.right)
        elif isinstance(node, UnionNode):
            return self._union_nfa(node.left, node.right)
        elif isinstance(node, StarNode):
            return self._star_nfa(node.child)
        elif isinstance(node, PlusNode):
            return self._plus_nfa(node.child)
        elif isinstance(node, QuestionNode):
            return self._question_nfa(node.child)
        else:
            raise ValueError(f"Unknown AST node type: {type(node)}")
    
    def _char_nfa(self, char: str) -> NFA:
        
        start = NFAState()
        accept = NFAState(is_accept=True)
        start.add_transition(char, accept)
        return NFA(start, accept)
    
    def _concat_nfa(self, left_node: ASTNode, right_node: ASTNode) -> NFA:
        
        left = self._visit(left_node)
        right = self._visit(right_node)
        
        # Connect left's accept to right's start with epsilon
        left.accept.is_accept = False
        left.accept.add_transition(None, right.start)  # epsilon transition
        
        return NFA(left.start, right.accept)
    
    def _union_nfa(self, left_node: ASTNode, right_node: ASTNode) -> NFA:
       
        left = self._visit(left_node)
        right = self._visit(right_node)
        
        start = NFAState()
        accept = NFAState(is_accept=True)
        
        # Epsilon transitions from new start to both branches
        start.add_transition(None, left.start)
        start.add_transition(None, right.start)
        
        # Epsilon transitions from both branches to new accept
        left.accept.is_accept = False
        right.accept.is_accept = False
        left.accept.add_transition(None, accept)
        right.accept.add_transition(None, accept)
        
        return NFA(start, accept)
    
    def _star_nfa(self, child_node: ASTNode) -> NFA:
       
        child = self._visit(child_node)
        
        start = NFAState()
        accept = NFAState(is_accept=True)
        
        # Can skip child entirely
        start.add_transition(None, accept)
        
        # Go through child
        start.add_transition(None, child.start)
        child.accept.is_accept = False
        child.accept.add_transition(None, accept)
        
        # Loop back
        accept.add_transition(None, child.start)
        
        return NFA(start, accept)
    
    def _plus_nfa(self, child_node: ASTNode) -> NFA:
       
        child = self._visit(child_node)
        
        start = NFAState()
        accept = NFAState(is_accept=True)
        
        # Must go through child at least once
        start.add_transition(None, child.start)
        child.accept.is_accept = False
        child.accept.add_transition(None, accept)
        
        # Loop back for repetition
        accept.add_transition(None, child.start)
        
        return NFA(start, accept)
    
    def _question_nfa(self, child_node: ASTNode) -> NFA:
       
        child = self._visit(child_node)
        
        start = NFAState()
        accept = NFAState(is_accept=True)
        
        # Can skip child
        start.add_transition(None, accept)
        
        # Or go through child
        start.add_transition(None, child.start)
        child.accept.is_accept = False
        child.accept.add_transition(None, accept)
        
        return NFA(start, accept)


def build_nfa(regex: str) -> Optional[NFA]:
    from src.parser import parse
    ast = parse(regex)
    builder = NFABuilder()
    return builder.build(ast)