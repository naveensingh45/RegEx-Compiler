import os
import sys

GRAPHVIZ_PATH = r"C:\Program Files\Graphviz\bin"
if GRAPHVIZ_PATH not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + GRAPHVIZ_PATH

from graphviz import Digraph
from src.nfa import NFA


class Visualizer:
    
    def visualize_nfa(self, nfa: NFA, filename: str = "nfa", view: bool = False):
       
        dot = Digraph(comment='NFA')
        dot.attr(rankdir='LR')  # Left to right layout
        
        # Add states
        for state in nfa.states:
            if state.is_accept:
                # Accept states are double circles
                dot.node(str(state.id), str(state.id), shape='doublecircle')
            else:
                # Normal states are single circles
                dot.node(str(state.id), str(state.id), shape='circle')
        
        # Add invisible start node pointing to actual start
        dot.node('start', '', shape='none')
        dot.edge('start', str(nfa.start.id))
        
        # Add transitions
        for state in nfa.states:
            for symbol, next_states in state.transitions.items():
                # Use epsilon symbol for None
                label = 'ε' if symbol is None else symbol
                for next_state in next_states:
                    dot.edge(str(state.id), str(next_state.id), label=label)
        
        # Render
        dot.render(filename, format='png', cleanup=True, view=view)
        print(f" NFA visualization saved to {filename}.png")
        
        return dot


def visualize_nfa(nfa: NFA, filename: str = "nfa", view: bool = False):
    visualizer = Visualizer()
    return visualizer.visualize_nfa(nfa, filename, view)