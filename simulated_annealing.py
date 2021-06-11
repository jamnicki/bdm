import random
import copy
import numpy as np

random.seed(21)


def sa_result(P, B, ldm, d):
    # tworzenie vektora z danymi dotyczącymi każdego dnia
    ldm = list()
    for m in range(1, 13):
        ldm.append([])
        if m in (1, 3, 5, 7, 8, 10, 12):
            count = 31
        elif m in (4, 6, 9, 11):
            count = 30
        else:
            count = 28
        for i in range(count):
            ldm[m-1].append([d, P[d-1], 0])
            d += 1

    ldm_copy = copy.deepcopy(ldm)
    ldm_simutation = copy.deepcopy(ldm)

    # pierwotne uzuzpełnienie wektora, które potem zmieniamy
    sumaa = 0
    for m in range(1, 13):
        for i in range(3):
            ldm_copy[m-1][i][2] = 1
            sumaa += ldm[m-1][i][1]

    # funkcja sumująca prawdopodobieństwo
    def sum_funct():
        sumaa = 0
        days = []
        day_number = 0
        day_numbers = []
        for m in range(1, 13):
            for i in range(len(ldm_simutation[m-1])):
                if ldm_simutation[m-1][i][2] == 1:
                    sumaa += ldm_simutation[m-1][i][1]
                    days.append([m-1, i])
                    day_numbers.append(day_number)
                day_number += 1
        return round(sumaa, 3), day_numbers

    cost0 = sumaa

    T = 30
    factor = 0.85

    for i in range(8):
        T = T * factor
        for j in range(500):

            # najpierw w każdym miesiącu uzupełniamy jeden dzień by spełnić
            # założenie o minimum jednym balone w miesiącu

            for m in range(1, 13):
                if m in (1, 3, 5, 7, 8, 10, 12):
                    count = 31
                elif m in (4, 6, 9, 11):
                    count = 30
                else:
                    count = 28
                day = random.randint(1, count-1)
                ldm_simutation[m-1][day][2] = 1

            # później losujemy dowolne dni w roku, więc w teorii jest szansa,
            # że reszta wyników będzie tylko z jednego miesiąca

            for z in range(0, 48):
                msc = random.randint(1, 12)
                if msc in (1, 3, 5, 7, 8, 10, 12):
                    count = 31
                elif msc in (4, 6, 9, 11):
                    count = 30
                else:
                    count = 28
                day = random.randint(1, count-1)
                ldm_simutation[msc-1][day][2] = 1

            # liczymy wynik z wylosowanmych wyników, czyścimy tablicę do
            # kolejnego przejścia pętli, uzupełniamy tablicę dni, w których
            # wypuściliśmy balony i ewentualnie podmieniamy wynik, jeśli okazał
            # się lepszy od poprzdnika :D

            cost1, days = sum_funct()
            ldm_simutation = copy.deepcopy(ldm)

            if cost1 > cost0:
                cost0 = cost1
                best_days = days
            else:
                x = np.random.uniform()
                if x > np.exp((cost0 - cost1)/T):
                    cost0 = cost1
                    best_days = days

    return cost0, best_days
