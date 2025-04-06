from sorts import *
from soultions import *

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

def solution():
    files = ["data1.txt"]
    bestSum = float('inf')

    for file in files:
        r, p, q = loadFromFile(file)
        #r, p, q = SortR(r, p, q)
        #bestSum = calculateRaw(r, p, q)
        #bestSum = findSolutionFields(r, p, q, bestSum)
        bestSum = Shrage(r, p, q)

    return bestSum

if __name__ == "__main__":
    print(solution())
