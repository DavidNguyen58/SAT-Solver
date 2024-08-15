def load_dimacs(file_name):
    #file_name will be of the form "problem_name.txt"
    clauses = []
    with open(file_name, 'r') as f:
        for line in f:
            if (line[0] != 'p'):
                clause = []
                data = line.rstrip('\n').split(' ')
                for i in data:
                    if int(i) != 0:
                        clause += [int(i)]
                clauses += [clause]
    return clauses

# Simple Sat Sat_solve
def simple_sat_solve(clause_set):
    # Find all the literals of the clause_set
    def var_f(cnf):
        varf = list()
        for clause in cnf:
            for literal in clause:
                if literal == []:
                    return []
                elif (abs(literal) not in varf):
                    varf.append(abs(literal))
        return varf
    # Generate all the possible truth assignments
    def truth_assignments(variables, partial_solution, solution, i):
        if (i == len(variables)):
            solution.append(partial_solution[:])
            return
        for l in [variables[i], -variables[i]]:
            partial_solution.append(l)
            truth_assignments(variables, partial_solution, solution, i + 1)
            partial_solution.pop()
        return solution
    # Check the truth value of a clause under the truth assignment
    def check_single_clause(clause, truth_assignment):
        for i in truth_assignment:
            if (i in clause):
                if i in clause:
                    return True
        return False
    # Check for every clause
    def check_clause_set(clause_set, truth_assignment):
        for clause in clause_set:
            if not check_single_clause(clause, truth_assignment):
                return False
        return True
    # SAT-solver
    def solve(clauses, truth_assignments):
        for i in truth_assignments:
            if check_clause_set(clauses, i):
                return i
        return False
    
    varF = var_f(clause_set)
    assignment = truth_assignments(varF, [], [], 0)
    print(assignment, len(assignment))
    return solve(clause_set, assignment)

def branching_sat_solve(clause_set, partial_assignment=[]):
    # Get all the variables in the clause set for branching
    def var_f(cnf):
        if [] in cnf:
            return []
        varf = list()
        for clause in cnf:
            for literal in clause:
                if (abs(literal) not in varf):
                    varf.append(abs(literal))
        return varf
    
    # Update a clause after the assignment of a literal
    def update_clause(F, literal):
        new_F = []
        for clause in F:
            if literal not in clause:
                if -literal in clause:
                    new_F.append([i for i in clause if i != -literal])
                else:
                    new_F.append(clause)
        return new_F
    
    var = var_f(clause_set)

    def sat_solve(clause_set, i):
        varF = var_f(clause_set)
        # If the clause contains an empty clause, return False
        if len(varF) == 0 and len(clause_set) != 0:
            return False
        # We build up the partial assignment untils it contains the truth values of all variables
        if i == len(var):
            return True
        # For each variable, we branch on two truth values
        for v in [-var[i], var[i]]:
            partial_assignment.append(v)
            if sat_solve(update_clause(clause_set, v), i + 1):
                return True
            partial_assignment.pop()
        return False
    # SAT-solver
    if sat_solve(clause_set, 0):
        # Adding condition to make sure it returns a full partial_assignment
        if len(partial_assignment) != len(var):
            for i in var:
                if i not in partial_assignment and -i not in partial_assignment:
                    partial_assignment.append(i)
        return partial_assignment
    else:
        return False

def unit_propagate(clause_set):
    def check_for_unit_clause(clause_set):
        for i in range(len(clause_set)):
            if len(clause_set[i]) == 1:
                return True, i
        return False, None

    # Update clause after an assignment of literal
    def update_clause(F, literal):
        new_F = []
        for clause in F:
            if literal not in clause:
                if -literal in clause:
                    new_F.append([i for i in clause if i != -literal])
                else:
                    new_F.append(clause)
        return new_F
    
    # Iteratively loop through
    new_clause = clause_set
    while True:
        a, b = check_for_unit_clause(new_clause)
        if a == False:
            return new_clause
        else:
            new_clause = update_clause(new_clause, new_clause[b][0])

def dpll_sat_solve(clause_set, partial_assignment=[]):

    def check_for_unit_clause(clause_set):
        for i in range(len(clause_set)):
            if len(clause_set[i]) == 1:
                return True, i
        return False, None
    
    def var_f(F):
        if [] in F:
            return [], None
        varf = dict()
        if len(F) == 0:
            return [], None
        j, m = 0, len(F[0])
        for i in range(len(F)):
            if len(F[i]) < m:
                m = len(F[i])
                j = i
            for literal in F[i]:
                if (abs(literal) not in varf):
                    varf[abs(literal)] = 1
                else:
                    varf[abs(literal)] += 1
        return varf, j

    def update_clause(F, literal):
        new_F = []
        for clause in F:
            if literal not in clause:
                if -literal in clause:
                    new_F.append([i for i in clause if i != -literal])
                else:
                    new_F.append(clause)
        return new_F
    
    def unit_propagate(clause_set):
        new_clause = clause_set
        p = []
        while True:
            a, b = check_for_unit_clause(new_clause)
            if a == False:
                return new_clause, p
            else:
                p.append(new_clause[b][0])
                new_clause = update_clause(new_clause, new_clause[b][0])
    
    def pure_literal(F):
        def find_literal(F):
            table = dict()
            p = []
            for clause in F:
                for literal in clause:
                    if (-literal in p) and table[abs(literal)] == True:
                        p.remove(-literal)
                    elif (literal not in p) and abs(literal) not in table:
                        table[abs(literal)] = True #Indicate the variable has appeared
                        p.append(literal)
                    
            return p
        def update_clause(F, literal):
            new_F = []
            for clause in F:
                if literal not in clause:
                    if -literal in clause:
                        new_F.append([i for i in clause if i != -literal])
                    else:
                        new_F.append(clause)
            return new_F
        result = []
        while True:
            p = find_literal(F)
            if len(p) == 0:
                return F, result
            for l in p:
                result.append(l)
                F = update_clause(F, l) 


    def sat_solve(clause_set, partial_assignment):
        # Unit Propagation
        clause_set, p = unit_propagate(clause_set)
        clause_set, q = pure_literal(clause_set)
        varf, j = var_f(clause_set)
        # Save the initial partial_assignment
        tmp = partial_assignment[:]
        # Extend the initial partial assignment following from UP
        partial_assignment.extend(p)
        partial_assignment.extend(q)
        if len(varf) == 0:
            if len(clause_set) == 0:
                return True
            # If UP fails, then we backtrack.
            partial_assignment.clear()
            partial_assignment.extend(tmp)
            return False
        
        # Decision Heuristic, we choose a variable that occurs most in the clause set
        x, y = clause_set[j][0], varf[abs(clause_set[j][0])]
        for i in clause_set[j]:
            if varf[abs(i)] > y:
                y = varf[abs(i)]
                x = i

        for i in [-x, x]:
            partial_assignment.append(i)
            if sat_solve(update_clause(clause_set, i), partial_assignment):
                return True
            partial_assignment.pop()
        # If there are no satisfying assignments, then we also backtrack
        partial_assignment.clear()
        partial_assignment.extend(tmp)
        return False
    
    var, z = var_f(clause_set)
    if sat_solve(clause_set, partial_assignment):
        # Return full satisfying assignment
        if len(partial_assignment) != len(var):
            for i in var:
                if i not in partial_assignment and -i not in partial_assignment:
                    partial_assignment.append(i)
        return partial_assignment
    return False
