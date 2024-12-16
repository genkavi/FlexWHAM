import sys
outname = sys.argv[1]

from wham import *

print(outname)


U   = np.load('U.npy')
print("U loaded")

w_i = np.load('w_i.npy')
print("w_i loaded")

Pm  = np.load('Pm.npy')
print("Pm_loaded")

weights = WHAM(bias_matrix    = U, 
               window_indices = w_i,
               Temperature    = 310,
               Tolerance      = 10**0,
               Pm             = Pm,
               Units          = "kJoul",
               Bootstrap      = 5,
               Blocks         = None
              )


np.save(outname, weights)
