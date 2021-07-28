def rotate(s):
    res = s[-1]
    for i in range(len(s) - 1):
        res = res + s[i]
    return res

def apply(s, perm, v):
    res = ""
    permuted = v
    for i in range(len(v)):
        permuted = permuted[0:i] + v[perm[i] - 1] + permuted[(i + 1):]
    for i in range(len(v)):
        newchar = str((int(permuted[i]) + int(s[i])) % 2)
        res = res + newchar
    return res
    

def autocycle(s, perm, v):
    # s is string we add; give as string e.g. "1001"
    # perm is the permutation; give as list where the ith element (1-indexed) is where i maps to e.g. [2,3,1,4]
    # Note [2,3,1,4] is the 3 cycle (1 3 2)
    # v is the initial vertex; give as string e.g. "1110"
    res = []
    curr = v
    while (res == []) or (curr != v):
        curr = apply(s, perm, curr)
        res.append(curr)
    return res

def edgecycle(s, perm, v, w):
    res = []
    curr1, curr2 = v, w
    while (res == []) or (curr1 != v and curr2 != w):
        curr1 = apply(s, perm, curr1)
        curr2 = apply(s, perm, curr2)
        res.append({curr1, curr2})
    return res
    
def compose(s1, perm1, s2, perm2):
    # Apply (s2, perm2) first
    # i.e. result is (s1, perm1) o (s2, perm2)
    perm = []
    s = ""
    for i in range(len(perm1)):
        perm.append(perm1[perm2[i] - 1])
    iden = "0" * len(s1)
    s2permuted = apply(iden, perm1, s2)
    for i in range(len(s1)):
        newchar = str((int(s1[i]) + int(s2permuted[i])) % 2)
        s = s + newchar
    return (s, perm)

def perm2String(perm):
    s = ""
    for p in perm:
        s = s + str(p)
    return s

def string2Perm(s):
    perm = list(s)
    for i in range(len(perm)):
        perm[i] = int(perm[i])
    return perm    

def cycGroup(s, perm):
    G = set()
    currS, currPerm = s, perm2String(perm)
    while (currS, currPerm) not in G:
        G.add((currS, currPerm))
        currS, currPerm = compose(s, perm, currS, string2Perm(currPerm))
        currPerm = perm2String(currPerm)
    return G

# represent edges as "101*1", where * is the coordinate change

def noOverlap(Es):
    # Es is a list of sets of edges that are all the same size
    total = len(Es) * len(Es[0])
    U = set()
    for E in Es:
        U = set.union(U, E)
    return len(U) == total

def applytoedge(s, perm, e):
    # e = "101*1"
    res = ""
    permuted = e
    for i in range(len(e)):
        permuted = permuted[0:i] + e[perm[i] - 1] + permuted[(i + 1):]
    for i in range(len(e)):
        c = permuted[i]
        if c == "*":
            res = res + "*"
        else:
            newchar = str((int(c) + int(s[i])) % 2)
            res = res + newchar
    return res

def applytoedgeset(s, perm, E):
    res = set()
    for e in E:
        res.add(applytoedge(s, perm, e))
    return res

def edgesetcycle(s, perm, E):
    Es = []
    for (currS, currPerm) in cycGroup(s, perm):
        Es.append(applytoedgeset(currS, string2Perm(currPerm), E))
    return Es

def isValidSubgroup(s, perm, E):
    dim = len(s)
    totalEdges = dim * (2 ** (dim - 1))
    edges = len(E)
    copies = len(cycGroup(s, perm))
    # First check edge/group size divisibility
    if (edges * copies) != totalEdges:
        return False
    return noOverlap(edgesetcycle(s, perm, E))

def getSs(n):
    if n == 1:
        return ["0", "1"]
    else:
        res = []
        for s in getSs(n - 1):
            res.append(s + "0")
            res.append(s + "1")
        return res
    
def getPerms(L):
    l = len(L)
    if l == 1:
        return [L]
    perms = []
    for i in range(l):
        m = L[i]
        rest = L[0:i] + L[(i + 1):]
        for p in getPerms(rest):
            perms.append([m] + p)
    return perms
    

def getAuts(n):
    auts = []
    ss = getSs(n)
    perms = getPerms([i + 1 for i in range(n)])
    for s in ss:
        for perm in perms:
            auts.append((s, perm))
    return auts

# n in Qn
# findCyclic(4, {"000*", "00*0", "0*00", "*000"})
def findCyclic(n, E):
    auts = getAuts(n)
    for (s, perm) in auts:
        if isValidSubgroup(s, perm, E):
            return (s, perm)
    return "None"
    
def toEdge(v, d):
    loc = int(d) - 1
    return v[:loc] + "*" + v[(loc + 1):]

def traverse(v, d):
    loc = int(d) - 1
    new = "0"
    if v[loc] == "0":
        new = "1"
    return v[:loc] + new + v[(loc + 1):]

def toEdgeList(start, dirseq):
    # start = "000000"
    # dirseq = "315136315416325236325416315136315416325236325416"
    seq = list(dirseq)
    s = []
    curr = start
    for d in seq:
        s.append(toEdge(curr, d))
        curr = traverse(curr, d)
    return s

def dircyc(n, dirseq):
    return findCyclic(n, set(toEdgeList("0" * n, dirseq)))

def seqs(choices, l):
    if l == 1:
        return choices
    else:
        prev = seqs(choices, l - 1)
        res = []
        for c in choices:
            for p in prev:
                res.append(p + c)
        return res

def spec(A, B):
    res = []
    for a in A:
        for b in B:
            res.append(a + b)
    return res

def test():
    S = spec(spec(["1"], spec(["1", "3", "4", "5"], seqs([str(i + 1) for i in range(5)], 5))), ["1", "2", "3", "4", "5"])
    for dirseq in S:
        if isValidSubgroup("10000", [5,1,2,3,4], set(toEdgeList("00000", dirseq))):
            return dirseq
    return "None"

def smallestSubgroup(S):
    res = S.copy()
    for (s1, p1) in S:
        for (s2, p2) in S:
            (s, p) = compose(s1, string2Perm(p1), s2, string2Perm(p2))
            res.add((s, perm2String(p)))
    print(len(S))
    if res == S:
        return res
    else:
        return smallestSubgroup(res)
            
def applyautgroup(G, E):    
    Es = []
    for (currS, currPerm) in G:
        Es.append(applytoedgeset(currS, string2Perm(currPerm), E))
    return Es
    
def validautgroup(n, G, E):
    dim = n
    totalEdges = dim * (2 ** (dim - 1))
    edges = len(E)
    copies = len(G)
    # First check edge/group size divisibility
    if (edges * copies) != totalEdges:
        return False
    return noOverlap(applyautgroup(G, E))
    
    
    
    
    
    
