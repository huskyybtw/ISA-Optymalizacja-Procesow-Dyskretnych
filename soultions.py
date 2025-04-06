from sorts import *

def calculateRaw(r,p,q):
    r,p,q = r.copy(), p.copy(), q.copy()
    Cmax = 0

    for i in range(len(r)):
        if r[i] >  Cmax:
            Cmax = r[i]
        Cmax = Cmax + p[i]
        q[i] = Cmax + q[i]

    maxCooling = max(q)

    if maxCooling > Cmax:
        Cmax = maxCooling

    return Cmax

def findSolutionFields(r, p, q, bestSum):
    for i in range(len(r)):
        for j in range(i + 1, len(r)):
            copyR, copyP, copyQ = r.copy(), p.copy(), q.copy()
            copyR, copyP, copyQ = reshuffle(copyR, copyP, copyQ, i, j)
            currentSum = calculateRaw(copyR, copyP, copyQ)
            if currentSum < bestSum:
                bestSum = currentSum
    return bestSum

def Shrage(r, p, q):
    r, p, q = SortR(r, p, q)
    start = 1
    end = len(r)
    timespent = 0

    ready = []
    timespent = r[0]
    ready.append(0)

    for x in r:
        for i in range(start, end):
            if timespent >= r[i]:
                ready.append(i)
            else:
                start = i
                break
        
        _r, _p, _q = [], [], []
        for i in ready:
            _r.append(r[i])
            _p.append(p[i])
            _q.append(q[i])
        _r, _p, _q = SortR(_r, _p, _q, reverse=True)

        for i in range(len(_r)):
            timespent += _p[i]
            q[i] = timespent + q[i]
        ready = []

    maxCooling = max(q)
    if maxCooling > timespent:
        timespent = maxCooling
    return timespent
    
        
        
    

        
        

        

    
    