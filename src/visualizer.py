import os
import sys

# Auto-add Graphviz to PATH
GRAPHVIZ_PATH = r"C:\Program Files\Graphviz\bin"
if os.path.exists(GRAPHVIZ_PATH) and GRAPHVIZ_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + GRAPHVIZ_PATH

from graphviz import Digraph
from src.nfa import NFA
from src.dfa import DFA


class Visualizer:
    
    def visualize_nfa(self, nfa: NFA, filename: str = "nfa", view: bool = False):
        dot = Digraph(comment='NFA')
        dot.attr(rankdir='LR')
        
        # Add states
        for state in nfa.states:
            if state.is_accept:
                dot.node(str(state.id), str(state.id), shape='doublecircle')
            else:
                dot.node(str(state.id), str(state.id), shape='circle')
        
        # Add invisible start node
        dot.node('start', '', shape='none')
        dot.edge('start', str(nfa.start.id))
        
        # Add transitions
        for state in nfa.states:
            for symbol, next_states in state.transitions.items():
                label = 'ε' if symbol is None else symbol
                for next_state in next_states:
                    dot.edge(str(state.id), str(next_state.id), label=label)
        
        # Render to file if filename provided
        if filename and not filename.startswith('temp'):
            try:
                dot.render(filename, format='png', cleanup=True, view=view)
                print(f"NFA visualization saved to {filename}.png")
            except Exception as e:
                print(f"⚠ Error: {e}")
        
        return dot
    
    def visualize_dfa(self, dfa: DFA, filename: str = "dfa", view: bool = False):
        dot = Digraph(comment='DFA')
        dot.attr(rankdir='LR')
        
        # Add states
        for state in dfa.states:
            # Label shows DFA state ID and NFA states it represents
            nfa_ids = sorted([s.id for s in state.nfa_states])
            label = f"{state.id}\n{{{','.join(map(str, nfa_ids))}}}"
            
            if state.is_accept:
                dot.node(str(state.id), label, shape='doublecircle')
            else:
                dot.node(str(state.id), label, shape='circle')
        
        # Add invisible start node
        dot.node('start', '', shape='none')
        dot.edge('start', str(dfa.start.id))
        
        # Add transitions
        for state in dfa.states:
            for symbol, next_state in state.transitions.items():
                dot.edge(str(state.id), str(next_state.id), label=symbol)
        
        # Render to file if filename provided
        if filename and not filename.startswith('temp'):
            try:
                dot.render(filename, format='png', cleanup=True, view=view)
                print(f" DFA visualization saved to {filename}.png")
            except Exception as e:
                print(f"⚠ Error: {e}")
        
        return dot


def visualize_nfa(nfa: NFA, filename: str = "nfa", view: bool = False):
    visualizer = Visualizer()
    return visualizer.visualize_nfa(nfa, filename, view)


def visualize_dfa(dfa: DFA, filename: str = "dfa", view: bool = False):

    visualizer = Visualizer()
    return visualizer.visualize_dfa(dfa, filename, view)