def parse_dimacs(dimacs_file):
    with open(dimacs_file) as f:
        lines = f.readlines()
    cnf = []
    for line in lines:
        if line.startswith("c") or line.startswith("p"):
            continue
        clause = list(map(int, line.split()[:-1]))
        cnf.append(clause)
    return cnf
