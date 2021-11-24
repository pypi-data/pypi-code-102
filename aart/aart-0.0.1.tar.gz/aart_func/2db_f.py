#red shift factor for orbiting material
def gDisk(r,a,lamb):
    return sqrt(r**3 - 3*r**2 + 2*a*r**(3/2))/(r**(3/2) - (lamb- a))

#defined just for convenience
def Rint(r,a,lamb,eta):
    return (r**2 + a**2 - a*lamb)**2 - (r**2 - 2*r + a**2)*(eta + (lamb - a)**2)

#red shift factor for infalling material
def gGas(r,b,a,lamb,eta):
    isco=rms(a) # This should be done once
    Delta=r**2 - 2*r + a**2
    lambe=((isco**2 - 2*a*sqrt(isco) + a**2))/(isco**(3/2) - 2*sqrt(isco) + a)
    H=(2*r - a*lambe)/Delta
    gamma=sqrt(1 - 2/3 *1/isco)
    ut=gamma*(1 + (2)/r *(1 + H))
    uphi=gamma/r**2*(lambe + a*H)
    ur=-np.sqrt(2/3/isco)*(isco/r - 1)**(3/2)
    return 1/(ut - uphi*lamb - ur*Delta**(-1)*b*sqrt(Rint(r,a,lamb,eta)))

#calculate the observed brightness for a purely radial profile
def bright2(grid,mask,redshift_sign,mbar,a,rs,isco,thetao):
    alpha = grid[:,0][mask]
    beta = grid[:,1][mask]
    rs = rs[mask]
    lamb,eta = conserved_quantities(alpha,beta,thetao,a)
    brightness = np.zeros(rs.shape[0])
    redshift_sign = redshift_sign[mask]
    brightness[rs>=isco]= gDisk(rs[rs>=isco],a,lamb[rs>=isco])**4*profile(rs[rs>=isco],a)
    brightness[rs<isco]= gGas(rs[rs<isco],redshift_sign[rs<isco],a,lamb[rs<isco],eta[rs<isco])**4*profile(rs[rs<isco],a)
    
    r_p = 1+np.sqrt(1-a**2)
    brightness[rs<=r_p] = 0
    
    I = np.zeros(mask.shape)
    I[mask] = brightness
    return(I)