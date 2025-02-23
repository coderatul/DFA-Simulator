import pandas as pd

"""
DFA Simulator

This script simulates a Deterministic Finite Automaton (DFA) by reading its transition table from
an Excel file and checking if input strings are accepted by the DFA. The DFA is defined by a 6-tuple:
(Q, Σ, q0, F, δ, result), where Q is the set of states, Σ is the input alphabet, q0 is the start state,
F is the set of final states, δ is the transition function, and the result indicates whether a string
is accepted or rejected.

Usage:
    Create an instance of DFASimulator with the path to your Excel file (e.g., 'dfa_transitions.xlsx'),
    then use the check_string method to test strings, optionally specifying verbose=True for detailed
    output.

Points to Take Care of While Entering Data into the Excel File:
    - Empty sting '', is interpreted as ε(string with 0 length)
    - Initial State Marker : Use the marker "-->" to indicate the start state. To prevent Excel
      from interpreting "-->" as a formula, enter it with an escape sequence (e.g., precede it with
      a single quote: '-->). This ensures Excel treats it as plain text.
    - Input Alphabet : The input alphabet (Σ) may increase by adding new columns for additional
      symbols. All alphabet symbols are treated as strings by deafult, (e.g, 1,2.. are treated as string)
    - DFA Requirement : Since this script supports only DFAs, ensure a transition is defined for
      every state in Q and every symbol in Σ. Missing transitions will raise an error.
"""

class DfaSimulator:
    def __init__(self, filename):
        """Initialize the DFA simulator by reading the Excel file and extracting components."""
        self.filename = filename
        self.df = None
        self.Q = set()  # States
        self.Sigma = set()  # Alphabet
        self.q0 = None  # Start state
        self.F = set()  # Final states
        self.transitions = {}  # Transition function
        self.load_dfa()

    def load_dfa(self):
        """Load and parse the DFA from the Excel file."""
        try:
            # Read the Excel file with no header
            self.df = pd.read_excel(self.filename, header=None)

            # Extract states (Q) - from column 1 (index 1), excluding header rows
            states = self.df[1].iloc[2:].dropna().unique().tolist()
            self.Q = set(str(state) for state in states)

            # Extract input alphabet (Sigma) - from row 1, columns 2 onward
            sigma = self.df.iloc[1, 2:].dropna().tolist()
            self.Sigma = set(str(symbol) for symbol in sigma)

            # Extract start state (q0) - look for '-->' in column 0
            start_rows = self.df[self.df[0].str.contains(r'-->', na=False)].index
            if len(start_rows) > 1:
                raise ValueError("Only a single state may be the starting state.")
            elif len(start_rows) == 0:
                raise ValueError("No start state (marked with '-->') found in the table.")
            else:
                start_row = start_rows[0]
                self.q0 = str(self.df.iloc[start_row, 1])

            # Extract final states (F) - look for '*' in column 0
            final_rows = self.df[self.df[0].str.contains(r'\*', na=False)].index
            self.F = set(str(self.df.iloc[row, 1]) for row in final_rows)

            # Extract transitions
            for index, row in self.df.iterrows():
                if index > 1:  # Skip header rows
                    state = str(row[1])
                    if pd.notna(state):
                        for col in range(2, len(self.df.columns)):
                            symbol = str(self.df.iloc[1, col])
                            next_state = str(row[col])
                            if pd.notna(next_state) and pd.notna(symbol):
                                self.transitions[(state, symbol)] = next_state

            # Check for missing transitions
            missing_transitions = []
            for state in self.Q:
                for symbol in self.Sigma:
                    key = (state, symbol)
                    if key not in self.transitions:
                        missing_transitions.append(f"State {state} with input {symbol}")
            if missing_transitions:
                raise ValueError(f"Missing transitions for DFA: {', '.join(missing_transitions)}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{self.filename}' was not found. Please check the file path.")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def check_string(self, w: str, verbose: bool = False) -> str:
        """Check if a string is accepted by the DFA, with optional verbose output, aslo returns the result"""
        if verbose:
            print("Q (States):", self.Q)
            print("Sigma (Input Alphabet):", self.Sigma)
            print("q0 (Start State):", self.q0)
            print("F (Final States):", self.F)
            print("Transition Function (delta):", self.transitions)

        # Handle empty string
        if not w:
            if self.q0 in self.F:
                result = "Accepted"
            else:
                result = "Rejected"
        else:
            # Start from the initial state
            current_state = self.q0

            # Process each symbol in the input string
            for symbol in w:
                # Check if the symbol is in the alphabet
                if symbol not in self.Sigma:
                    result = "Rejected"
                    break

                # Get the next state using the transition function
                key = (current_state, symbol)
                if key not in self.transitions:
                    result = "Rejected"
                    break
                current_state = self.transitions[key]

            # Check if the final state is in F
            else:  # Only executed if no break occurred
                if current_state in self.F:
                    result = "Accepted"
                else:
                    result = "Rejected"

        
        print(f"Result for string '{w}': {result}")
        return result

# Example usage in a script
if __name__ == "__main__":
    try:
        # Create DFA simulator instance
        dfa = DfaSimulator('dfa_transitions.xlsx')

        # Get input string from user
        w = input("Enter a string: ")
        result = dfa.check_string(w)

        # for verbose o/p 
        # result = dfa.check_string(w,verbose = True)

    except FileNotFoundError as e:
        print(e)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")