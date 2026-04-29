import streamlit as st
import os
import sys
from io import BytesIO

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

from src.nfa import build_nfa, NFAState
from src.dfa import nfa_to_dfa, DFAState
from src.visualizer import Visualizer
from src.matcher import Matcher
from src.parser import ParserError
from src.lexer import LexerError

# Page config
st.set_page_config(
    page_title="Regex to NFA/DFA Compiler",
    page_icon="🕸️",
    layout="wide"
)

# Title
st.title("🔄 Regular Expression to NFA/DFA Compiler")
st.markdown("### Visualize and Test Regular Expression Automata")

# Sidebar - Information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool compiles regular expressions into:
    - **NFA** (Non-deterministic Finite Automaton)
    - **DFA** (Deterministic Finite Automaton)
    
    **Supported Operators:**
    - `*` - Zero or more (Kleene star)
    - `+` - One or more
    - `?` - Zero or one (optional)
    - `|` - Alternation (OR)
    - `()` - Grouping
    
    **Examples:**
    - `a*` - Zero or more a's
    - `(a|b)*` - Any combination of a's and b's
    - `(a|b)*abb` - Ends with "abb"
    """)
    
    st.header("📚 Quick Examples")
    examples = {
        "Single character": "a",
        "Concatenation": "ab",
        "Alternation": "a|b",
        "Kleene star": "a*",
        "Complex pattern": "(a|b)*abb",
        "Plus operator": "a+b*",
    }
    
    for name, pattern in examples.items():
        if st.button(name, key=f"example_{name}"):
            st.session_state.regex_input = pattern

# Initialize session state
if 'regex_input' not in st.session_state:
    st.session_state.regex_input = ""

# Main input
st.header("📝 Enter Regular Expression")
regex_pattern = st.text_input(
    "Regex Pattern:",
    value=st.session_state.regex_input,
    placeholder="e.g., (a|b)*abb",
    help="Enter a regular expression using supported operators"
)

# Update session state
st.session_state.regex_input = regex_pattern

if regex_pattern:
    try:
        # Build NFA and DFA
        with st.spinner("Compiling regex..."):
            NFAState.reset_counter()
            DFAState.reset_counter()
            
            nfa = build_nfa(regex_pattern)
            
            if nfa is None:
                st.warning("Empty regex pattern")
            else:
                dfa = nfa_to_dfa(nfa)
                
                # Show statistics
                st.success(f"✅ Compilation successful!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("NFA States", len(nfa.states))
                with col2:
                    st.metric("DFA States", len(dfa.states))
                with col3:
                    reduction = ((len(nfa.states) - len(dfa.states)) / len(nfa.states) * 100) if len(nfa.states) > 0 else 0
                    st.metric("State Reduction", f"{reduction:.1f}%")
                with col4:
                    st.metric("Alphabet Size", len(dfa.alphabet))
                
                # Visualizations
                st.header("📊 Automata Visualizations")
                
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    st.subheader("🔵 NFA (Non-deterministic)")
                    
                    # Generate NFA visualization
                    visualizer = Visualizer()
                    nfa_dot = visualizer.visualize_nfa(nfa, filename="temp_nfa", view=False)
                    
                    # Render to PNG in memory
                    nfa_png = nfa_dot.pipe(format='png')
                    st.image(nfa_png, use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download NFA",
                        data=nfa_png,
                        file_name=f"nfa_{regex_pattern.replace('|', 'or').replace('*', 'star')}.png",
                        mime="image/png"
                    )
                    
                    with st.expander("📋 NFA Details"):
                        st.write(f"**States:** {len(nfa.states)}")
                        st.write(f"**Start State:** {nfa.start.id}")
                        st.write(f"**Accept State:** {nfa.accept.id}")
                        st.write(f"**Transition Elements:** {', '.join(sorted(nfa.get_alphabet()))}")
                
                with viz_col2:
                    st.subheader("🟢 DFA (Deterministic)")
                    
                    # Generate DFA visualization
                    dfa_dot = visualizer.visualize_dfa(dfa, filename="temp_dfa", view=False)
                    
                    # Render to PNG in memory
                    dfa_png = dfa_dot.pipe(format='png')
                    st.image(dfa_png, use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download DFA",
                        data=dfa_png,
                        file_name=f"dfa_{regex_pattern.replace('|', 'or').replace('*', 'star')}.png",
                        mime="image/png"
                    )
                    
                    with st.expander("📋 DFA Details"):
                        st.write(f"**States:** {len(dfa.states)}")
                        st.write(f"**Start State:** {dfa.start.id}")
                        accept_states = [s.id for s in dfa.states if s.is_accept]
                        st.write(f"**Accept States:** {accept_states}")
                        st.write(f"**Transition Elements:** {', '.join(sorted(dfa.alphabet))}")
                
                # String Testing Section
                st.header("🧪 Test Strings")
                st.markdown("Enter strings to test against the compiled automaton")
                
                # Multiple test strings
                test_input = st.text_area(
                    "Test Strings (one per line):",
                    value="",
                    height=150,
                    help="Enter multiple strings, one per line"
                )
                
                if st.button("🚀 Run Tests", type="primary"):
                    test_strings = [s.strip() for s in test_input.split('\n') if s.strip()]
                    
                    if test_strings:
                        st.subheader("📊 Test Results")
                        
                        matcher = Matcher(dfa)
                        
                        # Results table
                        results = []
                        for test_str in test_strings:
                            result = matcher.match_with_trace(test_str)
                            results.append({
                                'String': f'"{test_str}"' if test_str else '"" (empty)',
                                'Result': '✅ ACCEPT' if result.accepted else '❌ REJECT',
                                'Status': result.accepted
                            })
                        
                        # Display results
                        for i, res in enumerate(results):
                            color = "green" if res['Status'] else "red"
                            st.markdown(f"**{res['String']}** → :{color}[{res['Result']}]")
                        
                        # Detailed trace for first string
                        if results:
                            st.subheader("🔍 Detailed Trace (First String)")
                            first_string = test_strings[0]
                            trace_result = matcher.match_with_trace(first_string)
                            
                            with st.expander("Show step-by-step execution", expanded=True):
                                for line in trace_result.trace:
                                    st.code(line)
                    else:
                        st.warning("Please enter at least one test string")
                
                # Interactive single string tester
                st.header("🎯 Interactive String Tester")
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    single_test = st.text_input(
                        "Enter a string to test:",
                        placeholder="e.g., abb",
                        key="single_test"
                    )
                with col_b:
                    st.write("")  # Spacing
                    st.write("")  # Spacing
                    test_button = st.button("Test", type="secondary")
                
                if single_test is not None and (test_button or single_test):
                    matcher = Matcher(dfa)
                    result = matcher.match_with_trace(single_test)
                    
                    if result.accepted:
                        st.success(f"✅ ACCEPTED: \"{single_test}\" matches the pattern!")
                    else:
                        st.error(f"❌ REJECTED: \"{single_test}\" does not match the pattern")
                    
                    with st.expander("Show execution trace"):
                        for line in result.trace:
                            st.text(line)
    
    except (ParserError, LexerError) as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check your regex syntax and try again")
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.code(str(e))

else:
    st.info("👆 Enter a regular expression to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built By Team Xyfer | Regex Compiler </p>
</div>
""", unsafe_allow_html=True)

#python -m streamlit run app.py