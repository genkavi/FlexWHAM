import numpy as np

def WHAM(bias_matrix, window_indices, Temperature, Tolerance=10**-5, Pm=None, Units="kJoul", Bootstrap=0, Blocks=None):
    print ("Inputs:")
    print ("Initial Probability:", Pm)
    print ("Units:", Units)
    print ("Temperature:", str(Temperature)+"K")
    print ("Tolerance:",Tolerance)
    print ("Bootstrap", Bootstrap)

    Nconf, Nw = bias_matrix.shape
    
    print ("Number of windows: ", Nw)
    print ("Total number of configurations: ", Nconf)
        
    T = np.float(Temperature)
    if (Units=='kJoul'):
        # Boltzmann constant in kJ/(mol.K)
        kB=0.0083144621
        beta=1.0/(kB*T)
    elif (Units=='kCal'):
        # Boltzmann constant in kcal/(mol.K)
        kB=0.0019872041
        beta=1.0/(kB*T)
    elif (Units=='kT'):
        beta=1.0
    else:
        print ("# Units has to be kJoul, kCal, or kT")
        sys.exit(2)
    
    print ("Thermodynamic beta = ", beta)
    
    # Bias function exponential
    bf = np.exp(-beta*bias_matrix)
    
    if ( Pm is None):
        pm=np.ones(Nconf)
        print ("No initial configuration weights.")
    else:
        pm = Pm
        print ("Initial configuration weights are set to ", pm)
    
    Nboots=np.int(Bootstrap)
    if (Nboots>0):
        print ("Number of bootstrap iterations= ", Nboots)
        if Blocks is None:
            blocks=window_indices
            print("Each simulation is taken as a single block.")
        else:
            blocks=Blocks
            print ("Blocks are set to ", blocks)

        Nblocks=np.unique(blocks).size
        print ("Total number of blocks= ", Nblocks)
    
    pboots = np.ones(Nconf)
    
    #inititalize c's
    cini = np.ones(Nw)
    
    #iterate until tolerance (in kT)
    tol = np.float(Tolerance)
    
    # bootstrapping
    for bs in range(0,Nboots+1):
        print (bs, " Bootstrap iteration")
        # in bs 0 we do not do any bootstrap but regular wham
        #
        # total prior weights (e.g., weigths from metadynamics)
        # N[i] is equal to number of samples in window i when there are no prior weights
        pp = pboots*pm
    
        N = np.empty(Nw)
        for i in range(0,Nw):
           wni = np.unique(window_indices)[i]
           N[i] = sum(pp[window_indices==wni])
        #
        c = cini
        it = 0
        lndc = 10**100
        while lndc >= tol:
            #save the previous values to check convergence
            cpre = c
            # The following sum is over all columns (i)
            multi=np.sum(N*c*bf,axis=1)
            #print (N,c,bf,N*c*bf,multi)
            p = pp/multi
       
            # The following sum is over all rows (t)          
            c = 1.0/np.sum(p[np.newaxis].T*bf,axis=0)
            lndc=np.log(np.max(c/cpre))
            
            if it%50==0:
                print(it, end=" ")
            
            it += 1
        print ("")
        print (bs, " Final estimate of c")
        print (c)

        #
        # finalize p -- calculate it again once the convergence is reached
        p  = pp/np.sum(N*c*bf,axis=1)
        # no normalize
        #p /= np.sum(p)
        #
        if bs == 0:
            cini = c
        
        if bs==0:
            ps=p
        else:
            ps=np.vstack([ps,p])
    

        if (Nboots>0):
            #bayesian weights
            u = np.empty(Nblocks+1)
            u[0] = 0.0
            u[-1] = 1.0
            u[1:-1] = np.sort(np.random.uniform(0,1,Nblocks-1))
            g = u[1:]-u[:-1]
            pboots = np.zeros(Nconf)
            for i in range(0,Nblocks):
                blocki = np.unique(blocks)[i]
                pboots[blocks == blocki] = g[i]/blocks[blocks == blocki].size

    print ("Done.")
    
    return ps.T
    
