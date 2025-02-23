# DFA Simulator 🖥️⚙️🔄

## Overview

The DFA Simulator is a Python tool for simulating Deterministic Finite Automata (DFAs) by reading their transition tables from an Excel file and checking if input strings are accepted by the DFA. It provides an object-oriented implementation with optional verbose output to display the DFA's 5-tuples (Q, Σ, δ, q0, F), and the result that wether a string belongs to DFA m/c or not

where,
 - Q : set of state(s)
 - Σ : set of input Alphabets
 - δ : transition function (Q x Σ = Q)
 - q0 : initial state
 - F : set of final state(s)

## Features 📌

- Reads DFA transition tables from an Excel file.
- Ensures all transitions are defined for every state and input symbol (DFA requirement).
- Offers verbose and non-verbose modes for output control.
- Includes error handling for invalid input, missing transitions, and file issues.
- Object-oriented design for maintainability and extensibility.

## Usage

### Preparing the Excel File

- Modify the pre-existing excel file `dfa_transitions.xlsx` according to your DFA

![example of excel structure](https://github.com/user-attachments/assets/45e87190-3c0b-48ac-863b-fa51d8cc970a)


**Points to Take Care of While Entering Data:** 📋
- *Representing ε* : ε(string with length 0), is represented using '' (empty string)
- *Initial State Marker* : Use the marker "-->" to indicate the start state. To prevent Excel
      from interpreting "-->" as a formula, enter it with an escape sequence (_e.g., precede it with
      a single quote: '-->_). This ensures Excel treats it as plain text.
- *Input Alphabet* : The input alphabet (Σ) may increase by adding new columns for additional
      symbols. All alphabet symbols are treated as strings by deafult, (_e.g, 1,2.. are treated as string_)
- _DFA Requirement_ : Since this script supports only DFAs, ensure a transition is defined for
      every state in Q and every symbol in Σ. Missing transitions will raise an error.

## Few examples 📋
- Transition table for a DFA, which accepts only those strings, which starts and ends with the same i/p symbol `a`, over the `Σ = {a,b}` is there in the file `dfa_transitions.xlxs` as an example

transition table in Excel would look like

|        |        | Input Alphabets|    |
|--------|--------|----------------|----|
|        | States |                |    |
|        |        | a              | b  |
| →      | q0     | q1             | ds |
| *      | q1     | q1             | q2 |
|        | q2     | q1             | q2 |
|        | ds     | ds             | ds |

- **q0**: Start state
- **q1***: Final state
- **ds**: Dead state (just a convention)

### Example 1: Non-Verbose Output for a Valid String
```python
# DFA Simulation
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w)
```
**Output:**
```
Enter a string: aaaa
Accepted
```
> **Accepted** because the string starts with 'a' and ends with 'a'.

---

### Example 2: Non-Verbose Output for an Invalid String
```python
# DFA Simulation
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w)
```
**Output:**
```
Enter a string: bbbba
Rejected
```
> **Rejected** because the string starts with 'b' and ends with 'a', not matching the requirement.

---

### Example 3: Verbose Output for a Valid String
```python
# DFA Simulation with Verbose Output
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w, verbose=True)
```
**Output:**
```
Q (States): {'q0', 'q1', 'q2', 'ds'}
Sigma (Input Alphabet): {'a', 'b'}
q0 (Start State): q0
F (Final States): {'q1'}
Transition Function (δ): {('q0', 'a'): 'q1', ('q0', 'b'): 'q2', ('q1', 'a'): 'q1', ('q1', 'b'): 'ds', ('q2', 'a'): 'ds', ('q2', 'b'): 'q2', ('ds', 'a'): 'ds', ('ds', 'b'): 'ds'}
Result for string 'aaaa': Accepted
Accepted
```
> **Accepted** because the string starts with 'a', ends with 'a', and all transitions are valid.

---

### Example 4: Verbose Output for an Invalid String
```python
# DFA Simulation with Verbose Output
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w, verbose=True)
```
**Output:**
```
Q (States): {'q0', 'q1', 'q2', 'ds'}
Sigma (Input Alphabet): {'a', 'b'}
q0 (Start State): q0
F (Final States): {'q1'}
Transition Function (δ): {('q0', 'a'): 'q1', ('q0', 'b'): 'q2', ('q1', 'a'): 'q1', ('q1', 'b'): 'ds', ('q2', 'a'): 'ds', ('q2', 'b'): 'q2', ('ds', 'a'): 'ds', ('ds', 'b'): 'ds'}
Result for string 'ab': Rejected
Rejected
```
> **Rejected** because the string starts with 'a' but ends with 'b', not meeting the requirement.

---

### Example 5: Non-Verbose Output for an Empty String
```python
# DFA Simulation
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w)
```
**Output:**
```
Enter a string:
Rejected
```
> **Rejected** because the empty string doesn't start or end with 'a', and the start state 'q0' is not a final state.

---

### Example 6: Verbose Output for an Invalid Symbol
```python
# DFA Simulation with Verbose Output
from dfa_simulator import DFASimulator

dfa = DFASimulator('dfa_transitions.xlsx')
w = input("Enter a string: ")
result = dfa.check_string(w, verbose=True)
```
**Output:**
```
Q (States): {'q0', 'q1', 'q2', 'ds'}
Sigma (Input Alphabet): {'a', 'b'}
q0 (Start State): q0
F (Final States): {'q1'}
Transition Function (δ): {('q0', 'a'): 'q1', ('q0', 'b'): 'q2', ('q1', 'a'): 'q1', ('q1', 'b'): 'ds', ('q2', 'a'): 'ds', ('q2', 'b'): 'q2', ('ds', 'a'): 'ds', ('ds', 'b'): 'ds'}
Result for string 'ac': Rejected
Rejected
```
> **Rejected** because 'c' is not in the alphabet {a, b}.

---





    
