import random
import copy
from sys import setrecursionlimit

setrecursionlimit(2000)
random.seed(21)
_objective_score, _solution_days = None, None


def tabu_search_result(P, B, ldm, d):
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

    # functions needed to tabu serach
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

    def neighbourhood(sol):
        nhlist = []
        for nr in range(8):
            solcopy = copy.deepcopy(sol)
            change = random.sample(range(12, B), 4)
            for place in change:
                replace(place, solcopy)
                nhlist.append(solcopy)
        return nhlist

    def pickbest(nhlist):
        nbest = []
        nbestv = 0
        for n in nhlist:
            value = objective(n)
            if value > nbestv:
                nbestv = value
                nbest = n
        return nbest

    def is_tabo(sol):
        for t in tabo:
            if sol == t:
                return True
        return False

    def is_aspiration(sol, historical):
        if objective(sol) > historical:
            return True
        return False

    def managetabo():
        if len(tabo) > 7:
            tabo.pop(0)

    def filter(nb, historical, act):
        bn = pickbest(nb)
        if is_tabo(bn):
            if is_aspiration(bn, historical):
                act = objective(bn)
                historical = act
                for t in range(len(tabo)):
                    if bn == tabo[t]:
                        tabo.pop(t)
                tabo.append(bn)
                return bn
            else:
                for n in range(len(nb)):
                    if nb[n] == bn:
                        nb.pop(n)
                filter(nb, historical, act)
        else:
            act = objective(bn)
            if act > historical:
                historical = act
            tabo.append(bn)
            managetabo()
            return bn

    def main(init, historical, act, timer):
        global _objective_score, _solution_days

        sol = copy.deepcopy(init)
        timer -= 1
        nb = neighbourhood(sol)
        sol = filter(nb, historical, act)
        if timer == 0:
            _objective_score, _solution_days = objective(sol), sol
        else:
            main(sol, historical, act, timer)

    timer, tabo, act, historical = 600, [], 0, 0
    initsol = initial()

    # main solving loop
    main(initsol, historical, act, timer)

    return _objective_score, _solution_days
