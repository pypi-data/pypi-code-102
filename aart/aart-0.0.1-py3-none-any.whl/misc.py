def cbrt(x):
    '''
    Cubic root
    :param x: number to compute cbrt
    '''
    if x.imag==0:
        return np.cbrt(x)
    else:
        return x**(1/3)

def rms(a):
    Z1=1 + (1 - a**2)**(1/3) *((1 + a)**(1/3) + (1 - a)**(1/3))
    Z2=sqrt(3*a**2 + Z1**2)
    return (3 + Z2 - sqrt((3 - Z1)*(3 + Z1 + 2*Z2)))

# For the radon interpolation
def poly_fit(x,a,b,c):
    return(a*x**-2+b*x**-3+c*x**-4)

def imagetreat(image,lims,lims0,dx1,dx2):
    fov1=fov*(lims/lims0)
    fov_rad1=fov1*1e-6*1./3600.*np.pi/180.
    angle1=0.5*fov_rad1
    Omega1=np.pi*angle1**2
    NN = image.shape[0]
    dfovreal1=2*angle1/NN
    flux = (dx1/dx2)*np.trapz(np.trapz(image, dx=dfovreal1, axis=0), dx=dfovreal1, axis=0) # Total flux 
    sino = (dx1/dx2)*radon(image, theta=radonangle, circle=True)
    xaxis=np.linspace(-lims,lims,num=NN) # in muas
    return sino, xaxis,flux 
