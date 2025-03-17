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

def solution():
    files = ["data1.txt", "data2.txt", "data3.txt", "data4.txt"]
    sum = 0
    for file in files:
        r,p,q = loadFromFile(file)
        sum = sum + calculateSolution(r,p,q)
    return sum

if __name__ == "__main__":
    print(solution())
