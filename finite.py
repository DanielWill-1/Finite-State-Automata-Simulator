class FSA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states, is_dfa=True):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.is_dfa = is_dfa

    def simulate(self, input_string):
        if self.is_dfa:
            return self.simulate_dfa(input_string)
        else:
            return self.simulate_nfa(input_string)

    def simulate_dfa(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False  # Invalid input
            current_state = self.transitions.get((current_state, char))
            if current_state is None:
                return False  # No valid transition
        return current_state in self.accept_states

    def simulate_nfa(self, input_string):
        def dfs(state, index):
            if index == len(input_string):
                return state in self.accept_states
            char = input_string[index]
            if (state, char) in self.transitions:
                for next_state in self.transitions[(state, char)]:
                    if dfs(next_state, index + 1):
                        return True
            return False

        return dfs(self.start_state, 0)


def main():
    print("Welcome to the Finite State Automata Simulator!")
    print("Build your FSA by providing the following details.")

    # Input states
    states = input("Enter the states (comma-separated): ").split(',')
    alphabet = input("Enter the input alphabet (comma-separated): ").split(',')
    
    # Input transitions
    print("\nDefine the transitions (state, input -> next state(s)).")
    print("For DFA, enter one next state. For NFA, enter multiple states separated by commas.")
    transitions = {}
    is_dfa = input("Is this a DFA? (yes/no): ").strip().lower() == 'yes'

    while True:
        transition = input("Enter a transition (state,input -> next states), or 'done' to finish: ").strip()
        if transition == 'done':
            break
        try:
            current_state, rest = transition.split(',')
            input_symbol, next_states = rest.split('->')
            current_state = current_state.strip()
            input_symbol = input_symbol.strip()
            next_states = [state.strip() for state in next_states.split(',')]
            if is_dfa and len(next_states) > 1:
                print("Error: DFA transitions can only have one next state.")
                continue
            transitions[(current_state, input_symbol)] = next_states if not is_dfa else next_states[0]
        except ValueError:
            print("Invalid format. Try again.")

    # Input start state and accept states
    start_state = input("\nEnter the start state: ").strip()
    accept_states = input("Enter the accept states (comma-separated): ").split(',')

    # Create FSA
    fsa = FSA(
        states=states,
        alphabet=alphabet,
        transitions=transitions,
        start_state=start_state,
        accept_states=accept_states,
        is_dfa=is_dfa
    )

    # Test strings
    print("\nFSA configuration complete! Now you can test strings.")
    while True:
        test_string = input("Enter a string to test (or 'exit' to quit): ").strip()
        if test_string == 'exit':
            break
        result = fsa.simulate(test_string)
        print("Accepted" if result else "Rejected")


if __name__ == "__main__":
    main()