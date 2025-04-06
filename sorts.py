def SortR(r,p,q, reverse=False):
    
    zipped = zip(r,p,q)
    r, p, q = zip(*sorted(zipped, reverse=reverse))
    r  = list(r)
    p  = list(p)
    q  = list(q)
    return r, p, q

def reshuffle(r, p, q, i, j):
    r[i], r[j] = r[j], r[i]
    p[i], p[j] = p[j], p[i]
    q[i], q[j] = q[j], q[i]
    return r, p, q