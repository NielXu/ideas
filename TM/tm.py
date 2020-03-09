"""
The simulation of Turing Machine. It is not an actual Turing Machine
and it is much slower and need to take extra steps to simulate. This
is for studying purpose only.
"""

"Pointer movement, N=not moving, L=left, R=right"
N = 0
L = 1
R = 2


ACCEPT = 0
REJECT = 1


class State:
    """
    A state of a turing machine can contain a string represents the
    name of the State

    `lab`: Label
    """
    def __init__(self, lab):
        self.lab = lab
    
    def __str__(self):
        return self.lab
    
    def __repr__(self):
        return self.__str__()


class Transit:
    """
    A transition function between states, it can perform
    1. Move pointer left (L)
    2. Move pointer right (R)
    3. Replace the char in state to a new char

    `ch`: When this ch is read, this function will be triggered

    `fs`: From state

    `ts`: To State

    `repl`: Replacement of char

    `mv`: Pointer movement
    """
    def __init__(self, ch, fs, ts, repl=None, mv=N):
        self.ch = ch
        self.fs = fs
        self.ts = ts
        self.repl = repl
        self.mv = mv

    def __str__(self):
        return "r["+str(self.ch)+"]" +\
                "fs["+str(self.fs)+"]"+\
                "ts["+str(self.ts)+"]"+\
                "rp["+str(self.repl)+"]"+\
                "mv["+str(self.mv)+"]"
    
    def __repr__(self):
        return self.__str__()


class TM:
    """
    Turing Machine Simulation

    `s`: A list of states

    `t`: A list of transition functions

    `q0`: Initial state

    `qa`: Accpeting state
    """
    def __init__(self, s, t, q0, qa):
        smap = {}
        for i in t:
            fs = i.fs
            r = i.ch
            if fs not in smap:
                smap[fs] = {r: i}
            else:
                smap[fs][r] = i
        self.smap = smap
        self.t = t
        self.q0 = q0
        self.qa = qa
    
    def run(self, inp, trace=False, maxout=-1, startspace=False, endspace=True):
        """
        Run the Turing Machine and feed the given input. Return `REJECT` if the
        steps limit is given and the machine did not halt within given number of
        steps, or if there is no next state we can go. Return `ACCEPT` if the
        machine reaches the accepting state.

        `inp`: The input string

        `trace`: Tracing the run of the TM

        `maxout`: Max steps that will be executed, if over the limit REJECT immediately.
        If it is not given, it might cause an infinite loop.

        `startspace`: Add blank character `_` to the start of the input

        `endspace`: Add blank character `_` to the end of the input
        """
        step = 0
        s = self.q0
        ptr = 0
        # Add trailing whitespaces to the input
        if endspace and not inp.endswith('_'):
            inp = inp + '_'
        # Add starting space to the input
        if startspace:
            if not inp.startswith('_'):
                inp = '_' + inp
            ptr = ptr + 1
        while True:
            # If steps exceed the limit, REJECT
            if maxout >= 0 and step >= maxout:
                return REJECT
            if trace:
                print('Config: ' + inp[:ptr] +"["+ str(s) +"]"+ inp[ptr+1:],
                    'Input: '+inp,
                    'Read: '+inp[ptr],
                    'Pointer: ' + str(ptr),
                    'At State: ' + str(s))
            # If current state is an acceptance state, ACCEPT
            if s == self.qa:
                self.last = inp
                return ACCEPT
            # Read char that current pointer pointing at
            ch = inp[ptr]
            # Get all transition functions that this state has
            fmap = self.smap[s]
            # If the char reading does not have corresponding function, REJECT
            if ch not in fmap:
                return REJECT
            # Get the corresponding function
            f = fmap[ch]
            # to: To state, repl: Replace char, mv: Pointer movement
            to = f.ts
            repl = f.repl
            mv = f.mv
            # Update current state
            s = to
            # If repl is given, replace the char that pointer is pointing at
            if repl:
                # If replacing reaching the whitespace, add more whitespaces
                if inp[ptr] == '_':
                    inp = inp[:ptr] + repl + inp[ptr+1:] + '_'
                else:
                    inp = inp[:ptr] + repl + inp[ptr+1:]
            # Remove extra spaces
            inp = self._merge_sapces(inp, startspace, endspace)
            # Move pointer
            if mv == L:
                ptr = ptr - 1
            elif mv == R:
                ptr = ptr + 1
            # Prevent pointer from moving outside the tape
            if ptr < 0:
                ptr = 0
            elif ptr > len(inp):
                ptr = len(inp) - 1
            step += 1
    
    def observe(self):
        """
        Observe the accepted result of the last run, remove spaces and only return
        the result. Or return None if there is no result from last run.
        """
        return self.last.replace('_', '') if self.last else None
    
    def _merge_sapces(self, inp, startspace, endspace):
        """
        Merge more than one spaces into one space. For example:
        __1__ to _1_, return the result string
        """
        index = len(inp) - 1
        findex = 0
        while index > 0 and inp[index] == '_':
            index -= 1
        if endspace:
            inp = inp[:index+1]+'_'
        while findex < len(inp) and inp[findex] == '_':
            findex += 1
        if startspace:
            inp = '_' + inp[findex:]
        return inp


# The following TM simulates the process of doing addition
# Number of ones represents the number, 0 represents the + sign
# 1110111 => 3 + 3
# Result: 111111 => 6

# States
q0 = State('q0')
q1 = State('q1')
q2 = State('q2')
q3 = State('q3')
q4 = State('q4')

# Transition functions
t1 = Transit('1', q0, q0, mv=R)
t2 = Transit('0', q0, q1, '1', R)
t3 = Transit('1', q1, q1, mv=R)
t4 = Transit('_', q1, q2, mv=L)
t5 = Transit('1', q2, q3, '_', L)
t6 = Transit('1', q3, q3, mv=L)
t7 = Transit('_', q3, q4, mv=R)

# Setup the Turing Machine given a list of states and functions, as well as
# the initial state and accepting state
tm = TM([q0, q1, q2, q3, q4],
    [t1, t2, t3, t4, t5, t6, t7],
    q0, q4)

# Run the machine on input 1110111(3+3), this algorithm requires starting space
print(tm.run('1110111', trace=True, startspace=True))
print(tm.observe())
