import numpy as np
import numpy.linalg as LA


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
    n = len(user_dict)
    l = len(movie_dict)
    user_list.sort()
    movie_list.sort()
    print user_list[-1], n
    print movie_list[-1], l
    return user_dict, movie_dict, n, l


def initialization(n,l,r):
    F = np.zeros((n,r))   # input of np.zeros is a tuple if you want to initialize a matrix
    G = np.zeros((r,l))
    #print "F",F[:,r-1]
    #f = np.ones(n)
    #F[:,r-1] = f
    return F,G


def AltQPInc(A,F,G,n,l,r):
    """
    input: original n*l matrix A, and rank size r
    output: n*r matrix F, r*l matrix G, and an n*l matrix R
    """ 
    RMat = {} #residual matrix initialized as a dict due to sparsity
    for k in range(r):
        f, g = RankOneApproximation(RMat)

    

if __name__ == "__main__": 
    user_dict, movie_dict, n, l = readData() 
    r = 3
    F, G = initialization(n,l,r)
        



