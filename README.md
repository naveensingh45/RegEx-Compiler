# RegEx to NFA/DFA Compiler

A compiler that converts regular expressions into visual finite automata with pattern matching capabilities.

---

## 🎯 Overview

This project implements a complete compiler pipeline that converts regular expressions (like `(a|b)*c+`) into Non-deterministic Finite Automata (NFA) and Deterministic Finite Automata (DFA), with beautiful visual diagrams and a working pattern matcher.

Key Features:
- Complete compilation: Lexer → Parser → NFA → DFA
- Visual graph generation using Graphviz
- Pattern matching with execution traces
- Comparative analysis (NFA vs DFA state reduction)
- Web Interface For direct user interaction

---

## 🛠️ Installation

```bash
# Install Graphviz (required)
# macOS: brew install graphviz
# Ubuntu: sudo apt-get install graphviz
# Windows: Download from graphviz.org

# Clone and setup
git clone https://github.com/naveensingh45/RegEx-Compiler.git
cd RegEx-Compiler
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
# Compile and visualize
python main.py "(a|b)*abb" --visualize

# Test string matching
python main.py "ab*c" --test "ac" "abc" "abbc"

# With all options
python main.py "(a|b)*" --visualize --minimize --output my_regex
```

**Options:**
- `-v, --visualize` - Generate NFA/DFA graphs
- `-t, --test` - Test strings to match
- `-m, --minimize` - Minimize DFA
- `-o, --output` - Output filename

---

## 📝 Supported Syntax

| Operator | Description | Example |
|----------|-------------|---------|
| `*` | Zero or more | `a*` |
| `+` | One or more | `a+` |
| `?` | Zero or one | `a?` |
| `\|` | Alternation | `a\|b` |
| `( )` | Grouping | `(ab)*` |

**Example patterns:**
- `ab` → matches "ab"
- `a|b` → matches "a" or "b"  
- `(a|b)*c` → matches "c", "ac", "bc", "aac", etc.

---

## 📁 Project Structure

```
regex-compiler/
├── src/
│   ├── lexer.py          # Tokenization
│   ├── parser.py         # AST construction
│   ├── nfa.py            # NFA builder
│   ├── dfa.py            # DFA converter
│   ├── visualizer.py     # Graph generation
│   └── matcher.py        # Pattern matching
├── tests/                # Test suite
├── examples/outputs      # Visual Outputs
├── app.py                # Web Interface
└── requirements.txt      # requirements
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src
```


## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👥 Authors

Team Xyfer 
1. Naveen Singh
2. Shreyam Thapliyal
3. Akshat Chauhan
4. Amey Jhaldiyal

---

## 🙏 Acknowledgments

- Thompson, K. (1968) - NFA Construction Algorithm
- Aho, Sethi, Ullman - Dragon Book
- Graphviz Team - Visualization library

---

⭐ Star this repo if you find it helpful!

