import numpy as np
import numpy.linalg as LA
import math



def readData():
    """
    read data into two dictionaries: movie_dict and user_dict 
    movie_dict: key is the movie_id, and value is the user_id
    user_dict: key is the user_id, and value is the movie id
    """
    infile = open("ml-100k/u.data","r")
    user_dict = {}
    movie_dict = {}
    user_list = []
    movie_list = []
    for line in infile:
        fields = line.strip().split()
        print fields[0],fields[1],fields[2],fields[3]
        user = int(fields[0])
        movie = int(fields[1])
        rating = float(fields[2])
        time_stamp = int(fields[3])

        if user not in user_dict:
            user_dict[user] = {}
            user_dict[user][movie] = rating
            user_list.append(user)
        else:
            user_dict[user][movie] = rating

        if movie not in movie_dict:
            movie_dict[movie] = {}
            movie_dict[movie][user] = rating
            movie_list.append(movie)
        else:
            movie_dict[movie][user] = rating
    infile.close() 
    l = len(user_dict)
    n = len(movie_dict)
    user_list.sort()
    movie_list.sort()
    print user_list[-1], l
    print movie_list[-1], n
    return  movie_dict, user_dict, n, l


def initialization(n,l,r):
    """
    initialize F and G as matrix with 0s as all entries 
    the reason to initialize F and G as matrix rather than dictionary is because they are not sparse
    """
    F = np.zeros((n,r))   # input of np.zeros is a tuple if you want to initialize a matrix
    G = np.zeros((r,l))
    #print "F",F[:,r-1]
    #f = np.ones(n)
    #F[:,r-1] = f
    return F,G



def AltQPInc(movie_dict,user_dict, F,G,n,l,r):
    """
    input: original n*l matrix A (here we use A_dict to represent matrix), and rank size r
    output: n*r matrix F, r*l matrix G, and an n*l matrix R
    """ 
    R_dict =  movie_dict #residual matrix initialized as a dict due to sparsity
    for k in range(r):
        f, g = RankOneApproximation(R_dict, user_dict,n,l,r)
        F[:,k] = f
        G[k,:] = g
        for movie in movie_dict:
            for user in movie_dict[movie]:
                R_dict[movie][user] = R_dict[movie][user] - f[movie-1]*g[user-1]
    return F, G, R_dict
   

def RankOneApproximation(movie_dict,user_dict,n,l,r):
    """
    input: A_dict, the matrix needs to be factorized
    output: a colunmn vector f (movie feature), and a row vector g (user feature)
    """
    convergent = False
    f = np.array([0.1]*n)
    f = f.T
    g = np.array([0.1]*l) 
    print "f",f
    print "g",g
    product = np.outer(f,g)
    print "product",product
    while convergent == False:
        g = Update_g(movie_dict,f,g,n,l,r)
        print "g",g
        f_hat = Update_g(user_dict,g.T,f.T,l,n,r)  #note the order of parameters n and l
        f = f_hat.T
        print "f",f
        product_next = np.outer(f,g)
        error = LA.norm(product_next - product)
        print "error",error
        print "product_next",product_next
        if error > 10.0:
            product = product_next
        else:
            convergent = True
            print "convergent------------------------------------------------------------"
    return f, g


def Update_g(A_dict,f,g,n,l,r):
    """
    input: the origin matrix (movie_dict) needs to be factorized, and a column vector
    output: a row vector
    """
    for j in range(l):
        low = float("-inf")
        up = float("inf")
        t = 0
        q = 0
        for movie in A_dict:
            user = j+1
            if user in A_dict[movie]:
                q = q + f[movie-1] * A_dict[movie][user]
                t = t + math.pow(f[movie-1],2)
                if f[movie-1] > 0:
                    up = min(up, A_dict[movie][user]/f[movie-1]) 
                elif f[movie-1] < 0:
                    low = max(low, A_dict[movie][user]/f[movie-1])
                else:
                    continue
        if t == 0:
            g[j] = 0 
            continue
        q = q /t
        if q <= up and q >= low:
            g[j] = q
        elif q > up:
            g[j] = up
        else:
            g[j] = low  
    return g    



if __name__ == "__main__": 
    movie_dict, user_dict, n, l = readData() 
    r = 3
    F, G = initialization(n,l,r)
    F, G, R_dict = AltQPInc(movie_dict, user_dict, F,G, n, l, r)
    print "F",F
    print "G",G
    print "R_dict", R_dict    


