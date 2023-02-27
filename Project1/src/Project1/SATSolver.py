from SATSolver.DIMACSparser import *

# Initialize the solver state
def initialize_solver(cnf):
    assignment = {}
    for clause in cnf:
        for literal in clause:
            if literal not in assignment:
                assignment[literal] = None
    decision_stack = []
    return assignment, cnf, decision_stack

# Choose a literal to assign a truth value
def choose_literal(assignment):
    for literal in assignment:
        if assignment[literal] is None:
            return literal
    return None

# Propagate the consequences of the assignment by simplifying the formula
def propagate(assignment, cnf):
    while True:
        simplified = False
        for clause in cnf:
            unassigned_literals = [literal for literal in clause if assignment[literal] is None]
            if len(unassigned_literals) == 0:
                continue
            elif len(unassigned_literals) == 1:
                literal = unassigned_literals[0]
                assignment[literal] = True
                simplified = True
            else:
                false_literals = [literal for literal in unassigned_literals if assignment[-literal] is True]
                if len(false_literals) == len(unassigned_literals) - 1:
                    literal = [literal for literal in unassigned_literals if literal not in false_literals][0]
                    assignment[literal] = True
                    simplified = True
        if not simplified:
            break

# Backtrack when a conflict is detected
def backtrack(assignment, decision_stack, cnf):
    while True:
        if not decision_stack:
            return None
        literal = decision_stack.pop()
        assignment[literal] = None
        assignment[-literal] = None
        cnf.append([literal])
        propagate(assignment, cnf)
        if assignment[literal] is None:
            decision_stack.append(literal)
            return literal

# Learn a new clause when a conflict is detected
def learn_clause(conflict, assignment, cnf):
    learned_clause = []
    backjump_level = 0
    for literal in reversed(conflict):
        if backjump_level > 0:
            break
        for clause in cnf:
            if -literal in clause and assignment[-literal] == True:
                backjump_level = max
