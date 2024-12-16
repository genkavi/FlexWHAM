import numpy as np

# This does weighted histogram and then converst to log for free energy
def do_pmf_1D(data, weights, bins, Temperature=310, kB=0.0083144621):
    hist, bin_edges = np.histogram(data, bins=bins, weights=weights, density=True)

    kBT=kB * Temperature #kJ/mol
    DG=-kBT*np.log(hist)

    bin_centers=0.5*(bin_edges[1:]+bin_edges[:-1])

    return(DG, bin_centers)

# This does weighted histogram and then converst to log for free energy
def do_pmf_1D_bs(data, weights, bins, Temperature=310, kB=0.0083144621):
    Nboots = weights.shape[1]
    kBT=kB * Temperature #kJ/mol
    
    bs=0
    hist, bin_edges = np.histogram(data, bins=bins, weights=weights[:,bs], density=True)
    DG=-kBT*np.log(hist)

    mean = DG
    std  = DG**2.0
        
    for bs in range(1, Nboots):
        hist, bin_edges = np.histogram(data, bins=bins, weights=weights[:,bs], density=True)
        DG=-kBT*np.log(hist)
        
        mean += DG
        std  += DG**2.0

    mean /= Nboots
    std   = ( std/Nboots - mean**2.0)**0.5
    
    DG={}
    DG["mean"] = mean
    DG["std"]  = std

    bin_centers=0.5*(bin_edges[1:]+bin_edges[:-1])

    return(DG, bin_centers)

# calculate the 2d pmf using weighted histogram
def do_pmf_2D(x, y, weights, bins, Temperature=310, kB=0.0083144621):
    H, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=weights, density=True)
    
    kBT=kB * Temperature #kJ/mol
    DG=-kBT*np.log(H)

    x_centers=0.5*(xedges[1:]+xedges[:-1])
    y_centers=0.5*(yedges[1:]+yedges[:-1])

    return(DG, x_centers, y_centers)

# calculate the 2d pmf using weighted histogram
def do_pmf_2D_bs(x, y, weights, bins, Temperature=310, kB=0.0083144621):
    Nboots = weights.shape[1]
    kBT=kB * Temperature #kJ/mol

    bs=0
    H, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=weights[:,bs], density=True)
    DG=-kBT*np.log(H)

    mean = DG
    std  = DG**2.0
        
    for bs in range(1, Nboots):
        H, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=weights[:,bs], density=True)
        DG=-kBT*np.log(H)
        
        mean += DG
        std  += DG**2.0

    mean /= Nboots
    std   = ( std/Nboots - mean**2.0)**0.5
    
    DG={}
    DG["mean"] = mean
    DG["std"]  = std
    
    x_centers=0.5*(xedges[1:]+xedges[:-1])
    y_centers=0.5*(yedges[1:]+yedges[:-1])

    return(DG, x_centers, y_centers)

# calculate the 1d pmf using weighted histogram
def do_pmf_1D_kde(x, weights, bins, Temperature=310, kB=0.0083144621, bw_method="scott"):
    from scipy.stats import gaussian_kde
    
    values = x
    positions = bins
     
    kernel = gaussian_kde(values, weights=weights, bw_method=bw_method)
    H = np.reshape(kernel(positions).T, positions.shape)
        
    kBT=kB * Temperature #kJ/mol
    DG=-kBT*np.log(H)
    x_centers=bins

    return(DG, x_centers)

# calculate the 1d pmf using weighted histogram
def do_pmf_1D_kde_bs(x, weights, bins, Temperature=310, kB=0.0083144621, bw_method="scott"):
    from scipy.stats import gaussian_kde
    Nboots = weights.shape[1]
    kBT=kB * Temperature #kJ/mol
    
    values = x
    positions = bins
    
    bs = 0
    kernel = gaussian_kde(values, weights=weights[:,bs], bw_method=bw_method)
    H = np.reshape(kernel(positions).T, positions.shape)
        
    DG=-kBT*np.log(H)
    x_centers=bins

    mean = DG
    std  = DG**2.0
        
    for bs in range(1, Nboots):
            kernel = gaussian_kde(values, weights=weights[:,bs], bw_method=bw_method)
            H = np.reshape(kernel(positions).T, positions.shape)
            DG=-kBT*np.log(H)
            mean += DG
            std  += DG**2.0

    mean /= Nboots
    std   = ( std/Nboots - mean**2.0)**0.5
    
    DG={}
    DG["mean"] = mean
    DG["std"]  = std
    
    return(DG, x_centers)


# calculate the 2d pmf using weighted KDE
def do_pmf_2D_kde(x, y, weights, bins, Temperature=310, kB=0.0083144621, bw_method="scott"):
    from scipy.stats import gaussian_kde

    values=np.vstack([x,y])
    
    xv, yv = np.meshgrid(bins[0], bins[1], sparse=False, indexing='ij')
    positions = np.vstack([xv.ravel(), yv.ravel()])
        
    kernel = gaussian_kde(values, weights=weights, bw_method=bw_method)

    H = np.reshape(kernel(positions).T, xv.shape)
        
    kBT=kB * Temperature #kJ/mol
    DG=-kBT*np.log(H)

    x_centers=bins[0]
    y_centers=bins[1]

    return(DG, x_centers, y_centers)

# calculate the 2d pmf using weighted KDE
def do_pmf_2D_kde_bs(x, y, weights, bins, Temperature=310, kB=0.0083144621, bw_method="scott"):
    from scipy.stats import gaussian_kde
    Nboots = weights.shape[1]
    kBT=kB * Temperature #kJ/mol

    values=np.vstack([x,y])
    
    xv, yv = np.meshgrid(bins[0], bins[1], sparse=False, indexing='ij')
    positions = np.vstack([xv.ravel(), yv.ravel()])
    
    bs = 0 
    kernel = gaussian_kde(values, weights=weights[:,bs], bw_method=bw_method)
    H = np.reshape(kernel(positions).T, xv.shape)
    DG=-kBT*np.log(H)

    x_centers=bins[0]
    y_centers=bins[1]

    mean = DG
    std  = DG**2.0
    
    for bs in range(1, Nboots):
        print(bs, end=" ")
        kernel = gaussian_kde(values, weights=weights[:,bs], bw_method=bw_method)
        H = np.reshape(kernel(positions).T, xv.shape)
        DG=-kBT*np.log(H)
        
        mean += DG
        std  += DG**2.0
        
    mean /= Nboots
    std   = ( std/Nboots - mean**2.0)**0.5
    
    DG={}
    DG["mean"] = mean
    DG["std"]  = std    
    
    return(DG, x_centers, y_centers)

def do_average(y, x, weights, bins):
    nu, bin_edges = np.histogram(x, bins=bins, weights=weights  , density=False)
    su,    bin_edges = np.histogram(x, bins=bins, weights=weights*y, density=False)
    ave = su/nu
    
    bin_centers=0.5*(bin_edges[1:]+bin_edges[:-1])
    
    return(ave, bin_centers)
  
def do_average_bs(y, x, weights, bins):
    Nboots = weights.shape[1]

    bs = 0
    nu, bin_edges = np.histogram(x, bins=bins, weights=weights[:,bs]  , density=False)
    su,    bin_edges = np.histogram(x, bins=bins, weights=weights[:,bs]*y, density=False)
    ave = su/nu
    
    mean = ave
    std  = ave**2.0
    
    bin_centers=0.5*(bin_edges[1:]+bin_edges[:-1])

    for bs in range(1, Nboots):
        nu, bin_edges = np.histogram(x, bins=bins, weights=weights[:,bs]  , density=False)
        su,    bin_edges = np.histogram(x, bins=bins, weights=weights[:,bs]*y, density=False)
        ave = su/nu
        
        mean += ave
        std  += ave**2.0
        
    mean /= Nboots
    std   = ( std/Nboots - mean**2.0)**0.5
    
    ave={}
    ave["mean"] = mean
    ave["std"]  = std  
    
    return(ave, bin_centers)
    
def do_mean_std(x, weights):
    mean = np.average(x, weights=weights)
    var  = np.average((x-mean)**2.0, weights=weights)
    return (mean, var**0.5)

def do_mean_std_bs(x, weights):
    Nboots = weights.shape[1]

    bs = 0
    a = np.average(x, weights=weights[:,bs])
    mean_s     = a
    mean_s_std = a**2.0
    
    b  = np.average((x-mean_s)**2.0, weights=weights[:,bs])*0.5
    std_s     = b
    std_s_std = b**2.0
    
    for bs in range(1, Nboots):
        a = np.average(x, weights=weights[:,bs])
        mean_s     += a
        mean_s_std += a**2.0

        b  = np.average((x-mean_s)**2.0, weights=weights[:,bs])*0.5
        std_s     += b
        std_s_std += b**2.0
        
    mean_s      /= Nboots
    mean_s_std   = ( mean_s_std/Nboots - mean_s**2.0)**0.5

    std_s /= Nboots
    std_s_std   = ( std_s_std/Nboots - std_s**2.0)**0.5
    
    mean={}
    mean["mean"] = mean_s
    mean["std"]  = mean_s_std  
    
    std={}
    std["mean"] = std_s
    std["std"]  = std_s_std  
    
    return (mean, std)

def do_mean_std_angle(x, weights):
    sinx = np.sin(x)
    cosx = np.cos(x)
    
    mean_sinx = np.average(sinx, weights=weights)
    mean_cosx = np.average(cosx, weights=weights)
    mean = np.arctan2(mean_sinx, mean_cosx)
    
    #https://en.wikipedia.org/wiki/Directional_statistics
    R = (mean_sinx**2.0 + mean_cosx**2.0)**0.5 
    varz = 1 - R
    
    std = ( -2*np.log(R) )**0.5
    return (mean, std )

def do_mean_std_angle_bs(x, weights):
    Nboots = weights.shape[1]

    sinx = np.sin(x)
    cosx = np.cos(x)

    bs = 0
    
    mean_sinx = np.average(sinx, weights=weights[:,bs])
    mean_cosx = np.average(cosx, weights=weights[:,bs])
    
    mean_sinx_s = mean_sinx
    mean_cosx_s = mean_cosx
    R = (mean_sinx**2.0 + mean_cosx**2.0)**0.5 
        
    for bs in range(1, Nboots):
        mean_sinx = np.average(sinx, weights=weights[:,bs])
        mean_cosx = np.average(cosx, weights=weights[:,bs])

        mean_sinx_s += mean_sinx
        mean_cosx_s += mean_cosx
        R += (mean_sinx**2.0 + mean_cosx**2.0)**0.5 
    
    mean_sinx_s /= Nboots
    mean_cosx_s /= Nboots
    R /= Nboots
       
    mean_s = np.arctan2(mean_sinx_s, mean_cosx_s)
    std_s = ( -2*np.log(R) )**0.5

    
    mean={}
    mean["mean"] = mean_s
    mean["std"]  = std_s  
    
    
    return (mean)