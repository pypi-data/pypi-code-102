#Angular momentum and carter constant
def conserved_quantities(alpha,beta,theta_o,a):
    lam = -alpha*np.sin(theta_o)
    eta = (alpha**2-a**2)*np.cos(theta_o)**2+beta**2
    return(lam,eta)

#Calculate cube root for real number or the principle root for complex number
def cuberoot(a):
    a_real_ind = np.ones(a.shape)
    a_real_ind[np.abs(a.imag)>1e-12] = 0
    croa1 = np.cbrt((a*a_real_ind).real)
    croa2 = (a-a*a_real_ind)**(1/3)
    return(croa1+croa2)

#calculate radial turning points
def radial_turning_points(alpha,beta,lam,eta,a,M):

    A = a**2-eta-lam**2
    B = 2*M*(eta+(lam-a)**2)
    C = -a**2*eta
    
    P = -A**2/12-C
    Q = -A/3*((A/6)**2-C)-B**2/8
    
    #Distinguish real and complex numbers in the cube root
    pp = -Q/2+np.sqrt((P/3)**3+(Q/2)**2+0*1j)
    mm = -Q/2-np.sqrt((P/3)**3+(Q/2)**2+0*1j)
    w_p = cuberoot(pp)
    w_m = cuberoot(mm)
    
    z = np.sqrt((w_p+w_m)/2 - A/6)
    r1 = - z - np.sqrt(-A/2-z**2+B/4/z)
    r2 = - z + np.sqrt(-A/2-z**2+B/4/z)
    r3 = + z - np.sqrt(-A/2-z**2-B/4/z)
    r4 = + z + np.sqrt(-A/2-z**2-B/4/z)
    return(r1,r2,r3,r4)

#we can now calculate the angular turning points
def angular_turning_points(alpha,beta,lam,eta,a,M):
    
    Delta_theta = (1-(eta+lam**2)/a**2)/2
    u_p = Delta_theta+np.sqrt(Delta_theta**2+eta/a**2)
    u_m = Delta_theta-np.sqrt(Delta_theta**2+eta/a**2)
    
    theta_p = np.arccos(-np.sqrt(u_p))
    theta_m = np.arccos(+np.sqrt(u_p))
    
    return(u_p,u_m,theta_p,theta_m)


def angular_integrals(mbar,beta,u_p,u_m,theta_p,theta_m,pm_o,theta_o,a):
    k = u_p/u_m
    
    #complete elliptic integrals
    K = ellipk(k)
    E_prime = (ellipe(k)-K)/2/k
    PI = ellippi(u_p,np.pi/2,k)
    
    arg = (np.arcsin(np.cos(theta_o)/np.sqrt(u_p)))
    #incomplete elliptic integrals, for the observer
    F_o = ellipf(arg,k)
    E_prime_o = (ellipeinc(arg,k)-F_o)/2/k
    PI_o = ellippi(u_p,arg,k)
    #source terms are zero as we are assuming emission only from the equitorial plane 
    
    #m = m+1 for the disk on the back side of the black hole
    H_beta = np.zeros(beta.shape)
    H_beta[beta>=0] = 1
    m = mbar+H_beta
    G_theta = (2*m*K-pm_o*F_o)/a/np.sqrt(-u_m)
    G_phi = (2*m*PI-pm_o*PI_o)/a/np.sqrt(-u_m)
    G_t = -2*u_p*(2*m*E_prime-pm_o*E_prime_o)/a/np.sqrt(-u_m)
    
    return(G_theta,G_phi,G_t)

#source radius in radial case (2), one turning point at r4, scattering; Outside critical curve
def source_radius2(r1,r2,r3,r4,G_theta,alpha):
    r31 = (r3-r1)
    r32 = (r3-r2)
    r41 = (r4-r1)
    r42 = (r4-r2)
    r21 = (r2-r1)

    k2 = r32*r41/r31/r42
    F2 = ellipf(np.arcsin(np.sqrt(r31/r41).real),(k2).real)
    sn_square = np.square(ellipj(1/2*np.sqrt(r31*r42).real*G_theta-F2, (k2).real)[0])
    rs2 = np.nan_to_num((r4*r31-r3*r41*sn_square)/(r31-r41*sn_square))
    return(rs2)

#source radius in radial case (3), no turning point; generated at the white hole horizon and ended at infinity; inside critical curve
def source_radius3(r1,r2,r3,r4,G_theta,alpha):
    r31 = (r3-r1)
    r32 = (r3-r2)
    r41 = (r4-r1)
    r42 = (r4-r2)
    r21 = (r2-r1)

    A = np.sqrt(r32*r42).real
    B = np.sqrt(r31*r41).real
    k3 = ((A+B)**2 - r21**2)/(4*A*B)
    F3 = ellipf(np.arccos((A-B)/(A+B)),(k3).real)

    cn = ellipj(np.sqrt(A*B)*G_theta-F3,(k3).real)[1]
    rs3 = np.nan_to_num(((B*r2-A*r1)+(B*r2+A*r1)*cn)/((B-A)+(B+A)*cn))
    return(rs3)

#Radial effective potential, roots of which are the turing points:
def radial_potential(r,a,lam,eta):
    M=1
    Delta = r**2-2*M*r+a**2
    R = (r**2+a**2-a*lam)**2-Delta*(eta+(lam-a)**2)
    return(R)

#(indefinite) antiderivatives of the three radial integral in radial case 2.
def radial_case2_antiderivative(r,r1,r2,r3,r4,M,a,lam,eta):
    r_m = M-np.sqrt(M**2-a**2)
    r_p = M+np.sqrt(M**2-a**2)
    
    r31 = (r3-r1)
    r32 = (r3-r2)
    r41 = (r4-r1)
    r42 = (r4-r2)
    r43 = (r4-r3)
    r21 = (r2-r1)
    rp3 = (r_p-r3)
    rm3 = (r_m-r3)
    rp4 = (r_p-r4)
    rm4 = (r_m-r4)
    
    k = r32*r41/r31/r42
    
    x2 = np.sqrt((r-r4)*r31/(r-r3)/r41)
    arg = np.arcsin(x2)
    
    F2 = 2/np.sqrt(r31*r42)*ellipf(arg.real,k.real)

    E2 = np.sqrt(r31*r42)*ellipeinc(arg.real,k.real)
    PI21 = 2/np.sqrt(r31*r42)*ellippi((r41/r31).real,arg.real,k.real)
    PI2p = 2/np.sqrt(r31*r42)*r43/rp3/rp4*ellippi((rp3*r41/rp4/r31).real,arg.real,k.real)
    PI2m = 2/np.sqrt(r31*r42)*r43/rm3/rm4*ellippi((rm3*r41/rm4/r31).real,arg.real,k.real)
    
    I0 = F2
    I1 = r3*F2 + r43*PI21
    I2 = np.sqrt(radial_potential(r,a,lam,eta))/(r-r3)-(r1*r4+r2*r3)/2*F2-E2
    Ip = - PI2p - F2/rp3
    Im = - PI2m - F2/rm3
    return(I0,I1,I2,Ip,Im)

#radial integrals in case 2.
def radial_case2(rs,ro,r1,r2,r3,r4,M,a,beta,lam,eta,redshift_sign):
    #source terms
    w = redshift_sign
    w[w==1] = 0
    w[w==-1] = 1
    I0s,I1s,I2s,Ips,Ims = radial_case2_antiderivative(rs,r1,r2,r3,r4,M,a,lam,eta)
    
    #turning points terms
    I0t,I1t,I2t,Ipt,Imt = radial_case2_antiderivative(r4,r1,r2,r3,r4,M,a,lam,eta)
    
    #observer terms
    I0o,I1o,I2o,Ipo,Imo = radial_case2_antiderivative(ro,r1,r2,r3,r4,M,a,lam,eta)

    I0 = I0o-I0s + 2*w*(I0s-I0t)
    I1 = I1o-I1s + 2*w*(I1s-I1t)
    I2 = I2o-I2s + 2*w*(I2s-I2t)
    Ip = Ipo-Ips + 2*w*(Ips-Ipt)
    Im = Imo-Ims + 2*w*(Ims-Imt)
    
    return(I0,I1,I2,Ip,Im)

#(indefinite) antiderivatives of the three radial integral in radial case 3.
def radial_case3_antiderivative(r,r1,r2,r3,r4,M,a):
    r_m = M-np.sqrt(M**2-a**2)
    r_p = M+np.sqrt(M**2-a**2)
    
    r31 = (r3-r1)
    r32 = (r3-r2)
    r41 = (r4-r1)
    r42 = (r4-r2)
    r43 = (r4-r3)
    r21 = (r2-r1)
    rp3 = (r_p-r3)
    rm3 = (r_m-r3)
    rp4 = (r_p-r4)
    rm4 = (r_m-r4)
    rp2 = (r_p-r2)
    rm2 = (r_m-r2)
    rp1 = (r_p-r1)
    rm1 = (r_m-r1)
    
    A = np.sqrt(r32*r42)
    B = np.sqrt(r31*r41)
    k = ((A+B)**2-r21**2)/(4*A*B)
    alphap = (B*rp2+A*rp1)/(B*rp2-A*rp1)
    alpham = (B*rm2+A*rm1)/(B*rm2-A*rm1)
    alpha0 = (B+A)/(B-A)

    x3 = (A*(r-r1)-B*(r-r2))/(A*(r-r1)+B*(r-r2))
    arg = np.arccos(x3)
        
    def R1(alpha):
        p1 = np.sqrt((alpha**2-1)/(k+(1-k)*alpha**2))
        f1 = p1/2*np.log(np.abs(
            (p1*np.sqrt(1-k*np.sin(arg)**2)+np.sin(arg))/
            (p1*np.sqrt(1-k*np.sin(arg)**2)-np.sin(arg))))#natural log
        R1 = 1/(1-alpha**2)*(ellippi((alpha**2/(alpha**2-1)).real,arg.real,k.real)-alpha*f1)
        return(R1)
    
    F = ellipf(arg.real,k.real)
    E = ellipeinc(arg.real,k.real)
    
    def R2(alpha):
        R2 = 1/(alpha**2-1)*(F-alpha**2/(k+(1-k)*alpha**2)*(E-alpha*np.sin(arg)* \
                np.sqrt(1-k*np.sin(arg)**2)/(1+alpha*np.cos(arg)))) + \
                1/(k+(1-k)*alpha**2)*(2*k-alpha**2/(alpha**2-1))*R1(alpha)
        return(R2)

    
    F3 = 1/np.sqrt(A*B)*F

    PI31 = ((2*r21*np.sqrt(A*B)/(B**2-A**2))*R1(alpha0)).real


    PI32 = ((2*r21*np.sqrt(A*B)/(B**2-A**2))**2*R2(alpha0)).real
    

    I0 = F3
    I1 = ((B*r2+A*r1)/(B+A))*F3 + PI31
    I2 = ((B*r2+A*r1)/(B+A))**2*F3 + 2*((B*r2+A*r1)/(B+A))*PI31 + np.sqrt(A*B)*PI32
    Ip = -1/(B*rp2+A*rp1)*((B+A)*F3+2*r21*np.sqrt(A*B)/(B*rp2-A*rp1)*R1(alphap))
    Im = -1/(B*rm2+A*rm1)*((B+A)*F3+2*r21*np.sqrt(A*B)/(B*rm2-A*rm1)*R1(alpham))
    return(I0,I1,I2,Ip,Im,PI31)

#radial integrals in case 3.
def radial_case3(rs,ro,r1,r2,r3,r4,M,a):
    #source terms
    I0s,I1s,I2s,Ips,Ims, PI31s = radial_case3_antiderivative(rs,r1,r2,r3,r4,M,a)

    #observer terms
    I0o,I1o,I2o,Ipo,Imo, PI31o = radial_case3_antiderivative(ro,r1,r2,r3,r4,M,a)

    I0 = I0o-I0s
    I1 = I1o-I1s
    I2 = I2o-I2s
    Ip = Ipo-Ips
    Im = Imo-Ims
    PI31 = PI31o-PI31s

    return(I0,I1,I2,Ip,Im,PI31)

#radial integrals in both cases for every point on the observer plane.
def radial_integrals(rs,ro,r1,r2,r3,r4,M,a,beta, mask2, mask3, lam,eta,redshift_sign):
    
    I03,I13,I23,Ip3,Im3, PI31 = radial_case3(rs[mask3],ro,r1[mask3],r2[mask3],r3[mask3],r4[mask3],M,a)
    
    I02,I12,I22,Ip2,Im2 = radial_case2(rs[mask2],ro,r1[mask2],r2[mask2],r3[mask2],r4[mask2],M,a,beta[mask2],lam[mask2],eta[mask2],redshift_sign[mask2])
    
    I0 = np.zeros(mask2.shape)
    I1 = np.zeros(mask2.shape)
    I2 = np.zeros(mask2.shape)
    Ip = np.zeros(mask2.shape)
    Im = np.zeros(mask2.shape)
    PI1 = np.zeros(mask2.shape)

    I0[mask2] = I02.real
    I0[mask3] = I03.real
    I1[mask2] = I12.real
    I1[mask3] = I13.real
    I2[mask2] = I22.real
    I2[mask3] = I23.real
    Ip[mask2] = Ip2.real
    Ip[mask3] = Ip3.real
    Im[mask2] = Im2.real
    Im[mask3] = Im3.real
    PI1[mask3] = PI31
    r_m = M-np.sqrt(M**2-a**2)
    r_p = M+np.sqrt(M**2-a**2)
    
    I_r = I0
    I_phi = 2*M*a/(r_p-r_m)*((r_p-a*lam/2/M)*Ip-(r_m-a*lam/2/M)*Im)
    I_t = (2*M)**2/(r_p-r_m)*(r_p*(r_p-a*lam/2/M)*Ip-r_m*(r_m-a*lam/2/M)*Im) + (2*M)**2*I0 + (2*M)*I1 + I2
    return(I_r,I_phi,I_t)

#net change of angle due to gravitational lensing
def delta_phi(I_phi,G_phi,lam):
    return(I_phi+lam*G_phi)

#net change of time due to gravitational lensing
def delta_t(I_t,G_t,a):
    return(I_t+a**2*G_t)

#def mask_horizon(rs,r_p,N):
#    ind = np.arange(0,N,1)
#    for i in range(N):
#        try:
#            ind_min = ind[rs[ind[i]]<=r_p][0]
#            ind_max = ind[rs[ind[i]]<=r_p][-1]
#            rs[ind[i],ind_min:ind_max] = r_p
#        except:
#            pass
#    return(np.ravel(rs))


#calculate the source radius, angular, and time change for the rays associated with each grid. 
def calculate_observables(grid,mask,theta_o,a,mbar,M=1):
    alpha = grid[:,0][mask]
    beta = grid[:,1][mask]

    lam,eta = conserved_quantities(alpha,beta,theta_o,a)
    pm_o = np.sign(beta)
    r1,r2,r3,r4 = radial_turning_points(alpha,beta,lam,eta,a,M)
    mask2 = np.ones(r1.shape,dtype=bool)
    mask2[np.abs(r4.imag)>1e-13] = False
    mask3 = np.invert(mask2)
    u_p,u_m,theta_p,theta_m = angular_turning_points(alpha,beta,lam,eta,a,M)
    G_theta,G_phi,G_t = angular_integrals(mbar,beta,u_p,u_m,theta_p,theta_m,pm_o,theta_o,a)

    r31 = (r3-r1)
    r32 = (r3-r2)
    r41 = (r4-r1)
    r42 = (r4-r2)
    k = r32*r41/r31/r42
    taumax = np.zeros(alpha.shape)
    Jmax = 2/sqrt(r31[mask2]*r42[mask2])*ellipf(np.arcsin(np.sqrt(r31[mask2]/r41[mask2])).real, k[mask2].real)
    taumax[mask2]=2*Jmax.real
    
    r_sign0 = np.ones(taumax[mask2].shape)
    r_sign0[G_theta[mask2]>taumax[mask2]/2] = -1
    
    r_sign = np.ones(r1.shape)
    r_sign[mask2] = r_sign0
    redshift_sign = np.ones(mask.shape)
    redshift_sign[mask] = r_sign
    
    rs2 = source_radius2(r1[mask2],r2[mask2],r3[mask2],r4[mask2],G_theta[mask2],eta[mask2])
    rs3 = source_radius3(r1[mask3],r2[mask3],r3[mask3],r4[mask3],G_theta[mask3],eta[mask3])
    rs = np.zeros(mask.shape)
    r_mask = np.zeros(rs[mask].shape)
    r_mask[mask2] = rs2.real
    r_mask[mask3] = rs3.real
    rs[mask] = r_mask
    rs=np.nan_to_num(rs)
    r_p = 1+np.sqrt(1-a**2)
    rs[rs<=r_p] = r_p

    #if mbar ==0: 
    #    N = int(np.sqrt(grid.shape[0]))
    #    rs = mask_horizon(rs.reshape(N,N),r_p,N)
    I_r,I_phi,I_t = radial_integrals(r_mask,1000,r1,r2,r3,r4,M,a,beta, mask2, mask3, lam,eta,r_sign)
    deltat = np.zeros(mask.shape)
    deltaphi = np.zeros(mask.shape)
    
    deltat[mask] = delta_t(I_t,G_t,a)
    deltaphi[mask] = delta_phi(I_phi,G_phi,lam)
    
    maskkk = np.ones(rs.shape)
    maskkk[rs<=r_p] = 0
    return(rs,redshift_sign,deltat*maskkk,deltaphi*maskkk)