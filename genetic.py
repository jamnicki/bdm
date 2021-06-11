import random
import copy
from sys import setrecursionlimit

setrecursionlimit(2000)
random.seed(21)
_objective_score, _solution_days = None, None


def genetic_result(P, B, ldm, d):
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

    # functions needed
    def objective(sol):
        X = [0] * 365
        suma = 0
        for v in sol:
            X[v-1] = 1
        for m in ldm:
            for d in m:
                suma += X[d-1] * P[d-1]
        return suma

    def initial():
        bestlist = []
        for m in ldm:
            best = 0
            bestval = 0
            for d in m:
                if P[d-1] > bestval:
                    best = d
                    bestval = P[d-1]
            bestlist.append(best)
        newbestlist = copy.deepcopy(bestlist)
        rest = random.sample(range(1, 366), B)
        for e in rest:
            c = 0
            for b in bestlist:
                if e == b:
                    c = 1
            if c == 0 and len(newbestlist) < B:
                newbestlist.append(e)
        return newbestlist

    def replace(place, solcopy):
        new = random.randint(1, 365)
        flag = 0
        for i in solcopy:
            if new == i:
                flag = 1
        if flag == 0:
            solcopy[place] = new
        else:
            replace(place, solcopy)

    def mutation(sols):
        mlist = []
        sols.sort(key=objective, reverse=True)
        for nr in range(10):
            solcopy = sols[nr]
            change = random.sample(range(12, B), 4)
            for place in change:
                replace(place, solcopy)
                mlist.append(solcopy)
        return mlist

    # main solving loop
    def main(init, timer):
        global _objective_score, _solution_days

        sols = copy.deepcopy(init)
        timer -= 1
        muteted = mutation(sols)
        del sols[-10:]
        sols.extend(muteted)
        if timer == 0:
            sols.sort(key=objective, reverse=True)
            _objective_score, _solution_days = objective(sols[0]), sols[0]
        else:
            main(sols, timer)

    # running program
    timer = 101
    initsols = []
    for i in range(30):
        initsols.append(initial())

    main(initsols, timer)

    return _objective_score, _solution_days
