def OverRint(r,a,lamb,eta):
    return 1/sqrt((r**2 + a**2 - a*lamb)**2 - (r**2 - 2*r + a**2)*(eta + (lamb - a)**2))
    
def ApparentBH(s,a,thetao,alpha,beta,m,sign):

    alpha= s*alpha
    beta= s*beta
    
    # Photon conserved quantities
    # Eqs. (55 P1)
    lamb = -alpha*np.sin(thetao) 
    eta = (alpha**2 - a**2)*np.cos(thetao)**2+beta**2
    
    DeltaTheta = 1/2 *(1 - (eta + lamb**2)/a**2) # Eq. (19 P2)
    
    # Roots of angular potentail
    # Eqs. (B9 P2)
    uP = DeltaTheta + sqrt(DeltaTheta**2 + eta/a**2) # Eq. (19 P2)
    uM = DeltaTheta - sqrt(DeltaTheta**2 + eta/a**2) # Eq. (19 P2)
    
    rP = 1 + np.sqrt(1 - a**2)
    
    #Change this 1000
    return (sqrt(-uM)*a)*quad(OverRint, rP,1000,args=(a,lamb,eta))[0] +sign*ellipf(np.arcsin(np.cos(thetao)/np.sqrt(uP)), uP/uM) -2*m*ellipk(uP/uM) 

def nlayers(s,a,thetao,thetad,alpha,betai,mbar):
    '''
    Computes the boundary of the nth lensing band
    :param s: Type of ray. s>1 (Rays arrive outside) and s<1 (Rays arrive inside)
              the critical curve. We have to solve for this parameter. 
    :param a: BH's spin (-1<0<1)
    :param thetao: Observers angle [degrees]
    :param thetad: Angle of the disk [degrees]
    :param alpha: Bardeen's coordinate alpha
    :param betai: Bardeen's coordinate beta
    :param mbar: Label of the observed rings 

    :return: 
    '''
    alpha= s*alpha
    beta= s*betai

    #Angular Turning points encountered along the trajectory
    m= mbar + np.heaviside(betai,0) # Eq. (82 P1)

    # Photon conserved quantities
    # Eqs. (55 P1)
    lamb = -alpha*np.sin(thetao) 
    eta = (alpha**2 - a**2)*np.cos(thetao)**2+beta**2
    
    nutheta=np.sign(betai)
    
    # Radial Roots and Integrals 
    AAA = a**2 - eta - lamb**2 # Eq. (79 P2)
    BBB = 2*(eta + (lamb - a)**2) # Eq. (80 P2)
    CCC = -a**2 *eta # Eq. (81 P2)
    
    P = -(AAA**2/12) - CCC # Eq. (85 P2)
    Q = -(AAA/3) *((AAA/6)**2 - CCC) - BBB**2/8  # Eq. (86 P2)

    Delta3 = -4 *P**3 - 27*Q**2 # Eq. (92 P2)
    
    xi0 = np.real(cbrt(-(Q/2) + sqrt(-(Delta3/108))) + cbrt(-(Q/2) - sqrt(-(Delta3/108))) - AAA/3) # Eq. (87 P2)
    z = sqrt(xi0/2) # Eq. (94 P2)
   
    r1 = -z - sqrt(-(AAA/2) - z**2 + BBB/(4*z)) # Eq. (95a P2)
    r2 = -z + sqrt(-(AAA/2) - z**2 + BBB/(4*z)) # Eq. (95b P2)
    r3 = z - sqrt(-(AAA/2) - z**2 - BBB/(4*z))  # Eq. (95c P2)
    r4 = z + sqrt(-(AAA/2) - z**2 - BBB/(4*z))  # Eq. (95d P2)
    
    DeltaTheta = 1/2 *(1 - (eta + lamb**2)/a**2) # Eq. (19 P2)
    
    # Roots of angular potentail
    # Eqs. (B9 P2)
    uP = DeltaTheta + sqrt(DeltaTheta**2 + eta/a**2) # Eq. (19 P2)
    uM = DeltaTheta - sqrt(DeltaTheta**2 + eta/a**2) # Eq. (19 P2)
    
    # Eqs. (B9 P2)
    r21 = r2 - r1 
    r31 = r3 - r1
    r32 = r3 - r2
    r41 = r4 - r1
    r42 = r4 - r2
    r43 = r4 - r3
    
    # Outer and inner horizons
    # Eqs. (2 P2)
    rP = 1 + np.sqrt(1 - a**2)
    rM = 1 - np.sqrt(1 - a**2)
    
    # Eqs. (B10 P2)
    a1=sqrt(-(r43**2/4))
    # Eqs. (B10 P2)
    b1=(r3 + r4)/2
    
    #Elliptic Parameter
    # Eqs. (B13 P2)
    k = (r32*r41)/(r31*r42)

    AA = np.real(sqrt(a1**2 + (b1 - r2)**2)) # Eqs. (B56 P2)
    BB = np.real(sqrt(a1**2 + (b1 - r1)**2)) # Eqs. (B56 P2)

    # This parameter is real and less the unity
    k3 = np.real(((AA + BB)**2 - r21**2)/(4*AA*BB)) # Eqs. (B59 P2)
    
    # Eqs. (20 P1)
    Gtheta = 1/(sqrt(-uM)*a)*(2*m*ellipk(uP/uM) -nutheta*ellipf(np.arcsin(np.cos(thetao)/np.sqrt(uP)), uP/uM) + nutheta*(-1)**m*ellipf(np.arcsin(np.cos(thetad)/np.sqrt(uP)), uP/uM))
    
    if s>1:
        # Eqs.  (A10 P1)
        Q1= 4/sqrt(r31*r42)*ellipf(np.arcsin(sqrt(r31/r41)), k)
        return Q1-Gtheta
    else:
        if k3<1:
            # Eqs. (A11 P1)
            Q2=1/sqrt(AA*BB)*(ellipf(np.arccos((AA - BB)/(AA + BB)), k3) - ellipf(np.arccos((AA *(rP - r1) - BB*(rP - r2))/(AA*(rP - r1) + BB*(rP - r2))), k3))
        else:
            Q2=np.nan
    
        return Q2-Gtheta

def spacedmarks(x, y, Nmarks):

    """
    Computes the arch-length
    :param x: x point
    :param y: y point
    :param Nmarks: Number of marks 

    :returns: position of the x and y markers
    """
    dydx = np.gradient(y, x[0],edge_order=2)
    dxdx = np.gradient(x, x[0],edge_order=2)
    arclength = cumtrapz(sqrt(dydx**2 + dxdx**2), initial=0)
    marks = np.linspace(0, max(arclength), Nmarks)
    markx = np.interp(marks, arclength, x)
    marky = np.interp(markx, x, y)
    return markx, marky
    

def Shadow(a,angle):
    """
    Computes the critical curve (black hole shadow)
    :param a: spin of black hole
    :param angle: angle of the observer
    :param Nmarks: Number of marks 

    :returns: contour of the shadow on the observer plane
    """
    thetao = angle * np.pi/180
    
    rM = 2*(1 + np.cos(2/3 *np.arccos(-(a))))
    rP = 2*(1 + np.cos(2/3 *np.arccos(a)))
    
    
    r=np.linspace(rM,rP,int(1e7))
    
    lam = a + r/a *(r - (2 *(r**2 - 2*r + a**2))/(r - 1))
    eta = r**3/a**2 *((4*(r**2 - 2*r + a**2))/(r - 1)**2 - r)

    alpha=-lam/np.sin(thetao)
    beta=eta + a**2 *np.cos(thetao)**2 - lam**2*np.tan(thetao)**(-2)
    
    mask=np.where(beta>0)
    r=r[mask]
    
    rmin=min(r)+1e-12
    rmax=max(r)-1e-12
    
    r=np.linspace(rmin,rmax,int(1e6))
        
    lam = a + r/a *(r - (2 *(r**2 - 2*r + a**2))/(r - 1))
    eta = r**3/a**2 *((4*(r**2 - 2*r + a**2))/(r - 1)**2 - r)

    alpha=-lam/np.sin(thetao)
    beta=eta + a**2 *np.cos(thetao)**2 - lam**2*np.tan(thetao)**(-2)

    return alpha, sqrt(beta)

def round_up_to_even(f):
    return int(np.ceil(f / 2.) * 2)

def in_hull(p, hull):
    """
    Test if points in p are inside the hull
    """
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def grid_mask(hull,hull2,dx,limits,force_lims = False):
    """
    create cartesian grid on the observer plane
    :param hull: marks outer edge of the lensing band
    :param hull2: marks inner edge of the lensing band
    :param dx: grid resolution
    :param limits: specify limits for the both axis on the observer plane, only works if force_lims = True
    :param force_lims: specify a limit or find the optimal limit for the grid

    :returns: a cartesian grid and a mask indicating lensing band, along with other parameters
    """
    
    if force_lims == False:
        xlim_min = hull2.points[:,0].min()-5*dx
        xlim_max = hull2.points[:,0].max()+5*dx
        ylim_min = hull2.points[:,1].min()-5*dx
        ylim_max = hull2.points[:,1].max()+5*dx
        lims = np.ceil(max(np.abs(xlim_min),np.abs(xlim_max),np.abs(ylim_min),np.abs(ylim_max)))
        if lims>=limits:
            lims = limits
        x = np.linspace(-lims, lims, round_up_to_even(2*lims/dx))
        y = np.linspace(-lims, lims, round_up_to_even(2*lims/dx))
        N = int(round_up_to_even(2*lims/dx))
    else:
        lims = limits
        x = np.linspace(-lims, lims, round_up_to_even(2*lims/dx))
        y = np.linspace(-lims, lims, round_up_to_even(2*lims/dx))
        N = int(round_up_to_even(2*lims/dx))
    mesh = np.array(np.meshgrid(x , y))
    grid=mesh.T.reshape(-1, 2)
    
    # We check the points belong to the lensing bands
    mask1=np.invert(in_hull(grid,hull))
    mask2=in_hull(grid,hull2)
    
    indexes=mask2*mask1

    return grid, N , indexes, lims

def hulls(alpha, beta, smin=0.2, smax=600,limi0=0.99,lime0=1.01,limi1=0.999,lime1=1.001,limi2=0.9999,lime2=1.001):

    #Points around the BH's Shadows. The larger the smoother the Hull convex. Fifty is okay
    # How far inside we allow the region to be.  
    # How far outside we allow the region to be.

    data=(np.append(alpha,alpha), np.append(beta,-beta))

    points_0i=np.zeros([data[0].size,2])
    points_0e=np.array([[-limits,-limits],[limits,-limits],[limits,limits],[-limits, limits]])

    points_1i=np.zeros([data[0].size,2])
    points_1e=np.zeros([data[0].size,2])

    points_2i=np.zeros([data[0].size,2])
    points_2e=np.zeros([data[0].size,2])

    for i in range(data[0].size):
        if data[1][i]>=0:
            m1=optimize.root(ApparentBH, lim0, args=(spin_case,thetao,data[0][i],data[1][i],1,1))
        else:
            m1=optimize.root(ApparentBH, lim0, args=(spin_case,thetao,data[0][i],data[1][i],0,-1))

        points_0i[i]=m1.x[0]*np.array([data[0][i],data[1][i]])
        
        m1=optimize.root(nlayers, lim0, args=(spin_case,thetao,thetad,data[0][i],data[1][i],1))
        m2=optimize.root(nlayers, lime0, args=(spin_case,thetao,thetad,data[0][i],data[1][i],1))

        points_1i[i]=limi1*m1.x[0]*np.array([data[0][i],data[1][i]])
        points_1e[i]=lime1*m2.x[0]*np.array([data[0][i],data[1][i]])

        if m1.x[0]<smin:
            points_1i[i]=limi1*smin*np.array([data[0][i],data[1][i]])
        else:
            points_1i[i]=limi1*m1.x[0]*np.array([data[0][i],data[1][i]]) 

        if m2.x[0]>smax:
            points_1e[i]=lime1*smax*np.array([data[0][i],data[1][i]])
        else:
            points_1e[i]=lime1*m2.x[0]*np.array([data[0][i],data[1][i]])

        m1=optimize.root(nlayers, limi2, args=(spin_case,thetao,thetad,data[0][i],data[1][i],2))
        m2=optimize.root(nlayers, lime2, args=(spin_case,thetao,thetad,data[0][i],data[1][i],2))

        points_2i[i]=limi2*m1.x[0]*np.array([data[0][i],data[1][i]])
        points_2e[i]=lime2*m2.x[0]*np.array([data[0][i],data[1][i]])

    return Delaunay(points_0i), Delaunay(points_0e), Delaunay(points_1i), Delaunay(points_1e), Delaunay(points_2i),  Delaunay(points_2e)


def lb():

    critc=Shadow(spin_case,i_case)

    alpha_critc, beta_critc = spacedmarks(critcur[0], critcur[1], npointsS)

    hull_0i, hull_0e, hull_1i, hull_1e, hull_2i, hull_2e = lb.hulls(alpha_critc,beta_critc)

    if p_image==1:
        supergrid0, N0, mask0, lim0 =grid_mask(hull_0i,hull_0e,dx0,limits,True)
        print("Number of points in the n=0 grid ", supergrid0.shape[0])

        supergrid1, N1, mask1, lim1 =grid_mask(hull_1i,hull_1e,dx1,limits,True)
        print("Number of points in the n=1 grid ", supergrid1.shape[0])

        supergrid2, N2, mask2, lim2 =grid_mask(hull_2i,hull_2e,dx2,limits,True)
        print("Number of points in the n=2 grid ", supergrid2.shape[0])
    else:
        supergrid0, N0, mask0, lim0 =grid_mask(hull_0i,hull_0e,dx0,limits)
        print("Number of points in the n=0 grid ", supergrid0.shape[0])

        supergrid1, N1, mask1, lim1 =grid_mask(hull_1i,hull_1e,dx1,limits)
        print("Number of points in the n=1 grid ", supergrid1.shape[0])

        supergrid2, N2, mask2, lim2 =grid_mask(hull_2i,hull_2e,dx2,limits)
        print("Number of points in the n=2 grid ", supergrid2.shape[0])

    if save==1:

        filename="LensingBands_a_%s_i_%s.h5"%(spin_case,i_case)
        h5f = h5py.File(filename, 'w')

        h5f.create_dataset('alpha', data=alpha_critc)
        h5f.create_dataset('beta', data=beta_critc)

        h5f.create_dataset('hull_0i', data=hull_0i)
        h5f.create_dataset('hull_0e', data=hull_0e)
        h5f.create_dataset('grid0', data=supergrid0)
        h5f.create_dataset('grid0', data=supergrid0)
        h5f.create_dataset('N0', data=N0)
        h5f.create_dataset('mask0', data=mask0)
        h5f.create_dataset('lim0', data=lim0)

        h5f.create_dataset('hull_1i', data=hull_1i)
        h5f.create_dataset('hull_1e', data=hull_1e)
        h5f.create_dataset('grid1', data=supergrid1)
        h5f.create_dataset('N1', data=N1)
        h5f.create_dataset('mask1', data=mask1)
        h5f.create_dataset('lim1', data=lim1)

        h5f.create_dataset('hull_2i', data=hull_2i)
        h5f.create_dataset('hull_2e', data=hull_2e)
        h5f.create_dataset('grid2', data=supergrid2)
        h5f.create_dataset('N2', data=N2)
        h5f.create_dataset('mask2', data=mask2)
        h5f.create_dataset('lim2', data=lim2)

        h5f.close()

        print("File ",filename," created.")

        if live==1:
            return alpha_critc, beta_critc, hull_0i, hull_0e, hull_1i, hull_1e, hull_2i, hull_2e, supergrid0, N0, mask0, lim0, supergrid1, N1, mask1, lim1, supergrid2, N2, mask2, lim2 

    elif live==1:
        return alpha_critc, beta_critc, hull_0i, hull_0e, hull_1i, hull_1e, hull_2i, hull_2e, supergrid0, N0, mask0, lim0, supergrid1, N1, mask1, lim1, supergrid2, N2, mask2, lim2