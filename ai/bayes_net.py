import random


prob_table = {
    # Table for P(C)
    "P(C=0)": 0.70,
    "P(C=1)": 0.30,
    # Table for P(S|C) because S depends on C
    "P(S=0|C=0)": 0.80,
    "P(S=0|C=1)": 0.50,
    "P(S=1|C=0)": 0.20,
    "P(S=1|C=1)": 0.50,
    # Table for P(R|C) because R depends on C
    "P(R=0|C=0)": 0.99,
    "P(R=0|C=1)": 0.20,
    "P(R=1|C=0)": 0.01,
    "P(R=1|C=1)": 0.80,
    # Table for P(W|S, R) because W depends on S, R
    "P(W=0|S=0,R=0)": 0.99,
    "P(W=0|S=0,R=1)": 0.10,
    "P(W=0|S=1,R=0)": 0.05,
    "P(W=0|S=1,R=1)": 0.01,
    "P(W=1|S=0,R=0)": 0.01,
    "P(W=1|S=0,R=1)": 0.90,
    "P(W=1|S=1,R=0)": 0.95,
    "P(W=1|S=1,R=1)": 0.99,
}


def random_sampling(n, weight=1.0, observed={}):
    result = []
    for _ in range(n):
        cp_weight = weight
        c = 0
        s = 0
        r = 0
        w = 0
        # P(C), starts with C because it does not depends on anything.
        # If it is observed we set it to the observed value and modify
        # the weight accordingly.
        if 'c' in observed:
            c = observed['c']
            cp_weight = cp_weight * prob_table[f"P(C={observed['c']})"]
        else:
            rand = random.uniform(0, 1)
            if rand > prob_table["P(C=0)"]:
                c = 1
        # P(S|C)
        if 's' in observed:
            s = observed['s']
            cp_weight = cp_weight * prob_table[f"P(S={observed['s']}|C={c})"]
        else:
            rand = random.uniform(0, 1)
            if rand > prob_table[f"P(S=0|C={c})"]:
                s = 1
        # P(R|C)
        if 'r' in observed:
            r = observed['r']
            cp_weight = cp_weight * prob_table[f"P(R={observed['r']}|C={c})"]
        else:
            rand = random.uniform(0, 1)
            if rand > prob_table[f"P(R=0|C={c})"]:
                r = 1
        # P(W|S, R)
        if 'w' in observed:
            w = observed['w']
            cp_weight = cp_weight * prob_table[f"P(W={observed['w']}|S={s},R={r})"]
        else:
            rand = random.uniform(0, 1)
            if rand > prob_table[f"P(W=0|S={s},R={r})"]:
                w = 1
        result.append([c, s, r, w, cp_weight])
    return result


def count(variables, table):
    indices = []
    for v in variables:
        if v == "c":
            indices.append((0, 'c'))
        if v == "s":
            indices.append((1, 's'))
        elif v == "r":
            indices.append((2, 'r'))
        elif v == "w":
            indices.append((3, 'w'))
    count_var = 0
    for t in table:
        keep = True
        for i, c in indices:
            if t[i] != variables[c]:
                keep = False
                break
        if keep:
            count_var += t[4]
    return count_var


table = random_sampling(10000)
# P(R=1) = (# of rows in the table with R=1) / (# of rows)
r = count({ "r": 1 }, table)
print("P(R=1) = {0:.4f}".format(r/len(table)))
# P(C=1, W=0) = (# of rows in the table with C=1, W=0) / (# of rows)
cw = count({ "c": 1, "w": 0 }, table)
print("P(C=1, W=0) = {0:.4f}".format(cw / len(table)))

table = random_sampling(10000, observed={'r': 1})
sm = sum(t[4] for t in table)
# P(C=0) = (sum of rows with C=0 * w_row) /  (sum of all rows * w_row)
c = count({"c": 0}, table)
print("P(C=0) [observed R=1] = {0:.4f}".format(c/sm))

table = random_sampling(10000, observed={'r': 0, 'w': 1})
sm = sum(t[4] for t in table)
# P(C=0) = (sum of rows with C=0 * w_row) /  (sum of all rows * w_row)
c = count({"c": 0}, table)
print("P(C=0) [observed R=0, W=1] = {0:.4f}".format(c/sm))
