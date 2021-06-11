from pulp import LpMaximize, LpProblem, LpVariable, LpBinary, lpSum
from pulp.apis import PULP_CBC_CMD
import random

random.seed(21)


def solver_result(P, B, ldm, d, log=False):
    for m in range(1, 13):
        ldm.append([])
        if m in (1, 3, 5, 7, 8, 10, 12):
            count = 31
        elif m in (4, 6, 9, 11):
            count = 30
        else:
            count = 28
        for i in range(count):
            ldm[m-1].append(d)
            d += 1

    prob = LpProblem('meterobalones', LpMaximize)

    x = {}
    for i in range(1, 366):
        lowerBound = 0
        upperBound = 1
        x[i] = LpVariable('x' + '_' + str(i), lowerBound, upperBound, LpBinary)

    # Add objectives
    prob += lpSum(x[i] * P[i-1] for i in range(1, 366))

    # constraints
    for month in ldm:
        prob += lpSum(x[i] for i in month) >= 1

    prob += lpSum(x[i] for i in range(1, 366)) <= B

    prob.solve(PULP_CBC_CMD(msg=log))
    objective_score = prob.objective.value()

    solution_days = []
    for v in prob.variables():
        if v.varValue is not None and v.varValue != 0:
            solution_days.append(int((v.name)[2:]))

    return objective_score, solution_days
