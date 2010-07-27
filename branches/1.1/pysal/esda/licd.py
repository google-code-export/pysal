from scipy.stats import binom
from scipy.misc import factorial as fact
import numpy as np
import pysal

def _window(i,nrows,ncols,window_size):
    """
    Find cells in a window of size window_size center on cell i from a lattice
    with nrows and ncols

    Parameters
    ----------

    i            : int
                   id of center cell in the window

 
    nrows        : int
                   number of rows in the lattice

    ncols        : int
                   number of columns in the lattice

    window_size  : int
                   size of moving window to be centered on each
                   observation. Required to be an odd integer

    Returns
    -------

    neighbors    : list
                   ids of cells in the window centered on i

    """
    wsize=range(1,window_size+2,2)
    k=wsize.index(window_size)
    neighbors=[]
    inc=i/ncols
    i_row=inc
    top=max(0,inc-k)
    bottom=min(nrows,inc+k+1)
    left=max(0,i%ncols-k)
    right=min(ncols-1,i%ncols+k)
    neighbors=[]
    for row in range(top,bottom):
        pivot=row*ncols
        neighbors.extend(range(pivot+left,pivot+right+1))
    return neighbors 
    


def _example():
    """
    Builds data example from Upton and Fingleton 1985 Figure 3.3

    This is a 16x16 lattice of presence (1)/absence (0) data. Observations
    are row ordered.
    """
    l={}
    l[0]=[4]
    l[1]=[6,9]
    l[2]=[2,5,7]
    l[3]=[0,1,7,8,9,10]
    l[4]=[5,7,13]
    l[5]=[0,3,4,5,6,9]
    l[6]=[1,2,4,5,6,8,9,10]
    l[7]=[2,4,5,6,11,13]
    l[8]=[1,3]
    l[9]=[3,4,6,9,11,14,15]
    l[10]=[1,3,4,11]
    l[11]=[2,10]
    l[12]=[2,5,8,9,11,12]
    l[13]=[5,8]
    l[14]=[3,5,8]
    l[15]=[5,6,8,11,13]
    y=np.zeros((16*16,1))
    for i in range(16):
        for j in l[i]:
            p=i*16+j
            y[p]=1
    return y

class LICD_R:
    """
    Local Indicators for Categorical Data on a Regular Lattice

    Parameters
    ----------

    y            : array shape=(nrows*ncols,1)
                   binary variable

    nrows        : int
                   number of rows in the lattice

    ncols        : int
                   number of columns in the lattice

    window_size  : int
                   size of moving window to be centered on each
                   observation. Required to be an odd integer

    permutations : int
                   the number of permutations of values of y within each
                   window to determine signficance of local configuration

 
    Attributes
    ----------

    comp         : array (nx1)
                   number of black cells in the window centered on i

    joins        : array (nx1)
                   number of joins in the window centered on i

    l_bb         : array (nx1)
                   local black-black joins in the window centered on i

    l_bw         : array (nx1)
                   local black-white joins in the window centered on i

    l_ww         : array (nx1)
                   local white-white joins in the window centered on i

    p            : scalar
                   global binomial probability of success  (black cell)

    p_comp       : array(nx1)
                   binomial probabilities of having comp[i] black cells in r[i]
                   cells given success probability of p

    p_l_bb       : array (nx1)
                   p-value for local bb joins in the window centered on i

    p_l_bw       : array (nx1)
                   p-value for local bw joins in the window centered on i

    p_l_ww       : array (nx1)
                   p-value for local ww joins in the window centered on i

    r            : array (nx1)
                   number of cells in the window centered on i

    realizations : array (nx1)
                   number of permutations or combinations used for pseudo
                   signficance tests

    w            : weights instance
                   instance of weights for the regular lattice

    y            : array (nx1)
                   binary variable


    Notes
    -----

    Based on tests suggested by Boots [1]_

    The class implements two tests, one focusing on composition and one
    on configuration, both are local in form.  The composition test is
    is an exact test being based on the binomial distribution using the
    overall/global p as the success probability to determine the
    probability of realizing comp_i black cells in the window centered on
    i. The configuration test is a local join counts test centered on i.
    Depending on the number of black cells in window i, and the size of
    window i, the p-values for the local join counts are based on either a
    complete enumeration of the combinations of assigning the black cells
    to the window cells, or a sampling of this space if the number of
    combinations exceeds the specified number of permutations.

    Both tests as currently implemented assume that the global pattern of
    BB joins is spatially random.

    Example
    -------

   
    References
    ----------
    .. [1] Boots B. 2003. Developing local measures of spatial association for
    categorical data, Journal of Geographical Systems, 5: 139-160.
    """
    def __init__(self,y,nrows,ncols,window_size=3,permutations=99):
        self.y=y
        n=len(y)
        p=y.sum()*1./n
        self.p=p

        #pv=binom.pmf(comp,r,p)
        comp=np.zeros((n,1))
        r=np.zeros((n,1))
        self.w=pysal.lat2W(nrows,ncols)
        l_bb=np.zeros((n,1))
        l_ww=np.zeros((n,1))
        l_bw=np.zeros((n,1))
        conf_p_bb=np.zeros((n,1))
        conf_p_ww=np.zeros((n,1))
        conf_p_bw=np.zeros((n,1))
        joins=np.zeros((n,1))
        realizations=np.ones((n,1))*permutations
        for i in xrange(n):
            js=_window(i,nrows,ncols,window_size)
            r[i]=len(js)
            comp[i]=y[js].sum()
            # configuration info
            yi=y[js]
            #build local W
            w=np.zeros((r[i],r[i]))
            for pair in pysal.comb(js,2):
                left,right=pair
                li=js.index(left)
                ri=js.index(right)
                if right in self.w.neighbors[left]:
                    w[li,ri]=1
                    w[ri,li]=1
            joins[i]=w.sum()/2.
            yi.shape=(r[i],1)
            #local join count
            l_bb[i]=(w*(yi*yi.transpose())).sum()/2.
            yd=1-yi
            l_ww[i]=(w*(yd*yd.transpose())).sum()/2.
            l_bw[i]=joins[i]-l_bb[i]-l_ww[i]
            # permutations

            yb=yi.sum()
            nc=fact(r[i])/(fact(r[i]-yb)*fact(yb))
            if nc > permutations:
                # sample the combination space
                for perm in xrange(permutations): 
                    np.random.shuffle(yi)
                    yd=1-yi
                    l_bb_perm=(w*(yi*yi.transpose())).sum()/2.
                    l_ww_perm=(w*(yd*yd.transpose())).sum()/2.
                    if l_bb_perm>=l_bb[i]:
                        conf_p_bb[i]+=1
                    if l_ww_perm>=l_ww[i]:
                        conf_p_ww[i]+=1
                    if (joins[i]-l_bb_perm-l_ww_perm)>l_bw[i]:
                        conf_p_bw[i]+=1

            else:
                # exhaust the combinations
                real=0
                for comb in pysal.comb(range(r[i]),yb):
                    yi=np.zeros((r[i],1))
                    yi[comb]=1.0
                    yd=1-yi
                    l_bb_perm=(w*(yi*yi.transpose())).sum()/2.
                    l_ww_perm=(w*(yd*yd.transpose())).sum()/2.

                    if l_bb_perm>=l_bb[i]:
                        conf_p_bb[i]+=1
                    if l_ww_perm>=l_ww[i]:
                        conf_p_ww[i]+=1
                    if (joins[i]-l_bb_perm-l_ww_perm)>l_bw[i]:
                        conf_p_bw[i]+=1
                    real+=1
                if yb==0:
                    # no blacks in window
                    conf_p_ww[i]+=1
                    real=1

                realizations[i]=real
        self.comp=comp
        self.r=r
        self.p_comp=binom.pmf(comp,r,p)
        self.p_l_bb=conf_p_bb*1./realizations
        self.p_l_ww=conf_p_ww*1./realizations
        self.p_l_bw=conf_p_bw*1./realizations
        self.joins=joins
        self.l_bw=l_bw
        self.l_bb=l_bb
        self.l_ww=l_ww
        self.realizations=realizations
        

class LICD:
    """
    Local Indicators for Categorical Data
    
    Irregular lattice. Only compositional effects are measured, not
    configurational as in LICD_R

    """
    def __init__(self,y,w,pv=0.05):
        self.y=y
        n=len(y)
        ni=np.array(w.cardinalities.values())
        ni.shape=(n,1)
        ni=ni+y
        k=pysal.lag_array(w,y)+1
        p=y.sum()/(n*1.)
        self.k=k
        self.ni=ni
        p_comp=binom.pmf(k,ni,p)
        self.p=p
        self.p_comp=p_comp
        h=p_comp<=pv
        self.core=h*y
        self.hole=h*(1-y)
        
if __name__ == '__main__':
    y=_example()
    lr=LICD(y,pysal.lat2W(16,16))
    lq=LICD(y,pysal.lat2W(16,16,rook=False))
    l3=LICD_R(y,16,16)
    """
    l5=LICD_R(y,16,16,5)
    l7=LICD_R(y,16,16,7)
    """
