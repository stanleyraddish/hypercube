README
	fundamental.py is a Python file that contains certain functions that facilitate the process of checking 	hypercube decompositions in smaller dimensional hypercubes. 

FUNCTIONS/USAGE
        ◦ findCyclic(n, E)
            ▪ n : dimension of hypercube
            ▪ E : set of edges where edges are binary strings with a * in the edge direction
            ▪ returns generator automorphism of cyclic subgroup that decomposes E by Q_n, otherwise returns None if E is not cyclically fundamental
        ◦ dircyc(n, dirseq)
            ▪ n : dimension of hypercube
            ▪ dirseq: a string of numbers from 1 to n that represents a path starting at the all 0 vertex and taking edges in the input sequence
            ▪ returns findCyclic of the corresponding edge set
        ◦ smallestSubgroup(S)
            ▪ S : a set of automorphisms of the hypercube
                • elements are in the form (s, p) where s represents a binary string addition and p is a string corresponding to a permutation where p[i] is the coordinate i maps to
                • returns the smallest subgroup that contains all the elements in S
        ◦ applyautgroup(G, E)
            ▪ G : a subgroup of some automorphism group on a hypercube
            ▪ E : set of edges where edges are binary strings with a * in the edge direction
            ▪ returns a set of edge sets, each corresponding to applying some automorphism in G to E
        ◦ validautgroup(n, G, E)
            ▪ n : dimension of hypercube
            ▪ G : a subgroup of some automorphism group on a hypercube
            ▪ E : set of edges where edges are binary strings with a * in the edge direction
            ▪ return True of E fundamentally decomposes Q_n by subgroup G and False otherwise
	
