def loadFromFile(filename):
    r = []
    p = []
    q = []

    with open(filename, 'r') as file:
        file.readline()
        for line in file:
            s = line.strip()
            s = s.split()
            r.append(int(s[0]))
            p.append(int(s[1]))
            q.append(int(s[2]))
    return r,p,q

def calculateSolution(r,p,q):
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

def SortR(r,p,q):
    zipped = zip(r,p,q)
    r, p, q = zip(*sorted(zipped, reverse=False))
    r  = list(r)
    p  = list(p)
    q  = list(q)
    for i in range (len(r)):
        print(r[i], p[i], q[i])
    return r, p, q

#zmienic sortowanie na
# pierw [0] swapujemy z kazdym n razy
# potem [1] swapujemy z kazdym n
# potem[n] swapujemy z kazdym n razy

def reshuffle(r,p,q,it):
    r[it], r[it+1] = r[it+1], r[it]
    p[it], p[it+1] = p[it+1], p[it]
    q[it], q[it+1] = q[it+1], q[it]
    return r,p,q

def solution():
    #data2.txt","data3.txt","data4.txt
    files = ["data1.txt"]
    sum = 0
    bestSum = 0
    for file in files:
        r,p,q = loadFromFile(file)
        r,p,q = SortR(r,p,q)
        #sum = sum + calculateSolution(r,p,q)
        sum = calculateSolution(r,p,q)
        bestSum = sum
        for y in range (len(r) - 1):
            copyR,copyP,copyQ = r.copy(),p.copy(),q.copy()
            for i in range(len(r)-1):
                copyR,copyP,copyQ = reshuffle(copyR,copyP,copyQ,i)
                #for i in range(len(r)):
                #    print(copyR[i],copyP[i],copyQ[i])
                #print("-------------------")
                sum = calculateSolution(copyR,copyP,copyQ)
                if sum < bestSum:
                    bestSum = sum
            r[y],p[y],q[y] = r[y+1],p[y+1],q[y+1]
            
    return bestSum

if __name__ == "__main__":
    print(solution())
