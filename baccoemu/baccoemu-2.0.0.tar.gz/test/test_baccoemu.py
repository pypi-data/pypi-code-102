#run with python -m unittest test.test_baccoemu
import unittest
import baccoemu
import numpy as np

emu = baccoemu.Matter_powerspectrum()
kk = np.logspace(-2,0.6,10)
params = {
    'omega_matter'  :  0.315,
    'A_s'           :  2e-9,
    'omega_baryon'  :  0.05,
    'ns'            :  0.96,
    'hubble'        :  0.67,
    'neutrino_mass' :  0.1,
    'w0'            : -1.1,
    'wa'            :  0.2,
    'expfactor'     :  0.8,

    'M_c'           :  14,
    'eta'           : -0.3,
    'beta'          : -0.22,
    'M1_z0_cen'     : 10.5,
    'theta_out'     : 0.25,
    'theta_inn'     : -0.86,
    'M_inn'         : 13.4
}

dec_prec = 5

class test_baccoemu(unittest.TestCase):
    def test_get_nonlinear_boost(self):
        k, Q = emu.get_nonlinear_boost(**params, k=kk)
        Q_tab = np.array([ 1.0007161 ,  0.99524166,  0.99200782,  0.98202384,  1.03256175,
        1.32575333,  2.27006381,  5.03370763, 11.27070351, 20.31441056])
        for i,j in zip(Q,Q_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

    def test_get_baryonic_boost(self):
        k, S = emu.get_baryonic_boost(**params, k=kk)
        S_tab = np.array([1.00061651, 0.99987419, 0.99823298, 0.99842931, 0.99661765,
       0.99049649, 0.97010919, 0.93417986, 0.88753197, 0.83361164])
        for i,j in zip(S,S_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

    def test_get_linear_pk(self):
        k, pk_lin_cold = emu.get_linear_pk(**params, k=kk, cold=True)
        pk_lin_cold_tab = np.array([1.62854183e+04, 1.77584261e+04, 1.16049004e+04, 6.59140251e+03,
       2.49394757e+03, 7.38743986e+02, 1.88090425e+02, 4.23532059e+01,
       8.68574722e+00, 1.66160033e+00])
        for i,j in zip(pk_lin_cold,pk_lin_cold_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

        k, pk_lin_tot = emu.get_linear_pk(**params, k=kk, cold=False)
        pk_lin_tot_tab = np.array([1.61550147e+04, 1.75643833e+04, 1.14536942e+04, 6.48820975e+03,
       2.45236517e+03, 7.26781358e+02, 1.85054606e+02, 4.16805881e+01,
       8.54843339e+00, 1.63535958e+00])
        for i,j in zip(pk_lin_tot,pk_lin_tot_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

    def test_get_smeared_bao_pk(self):
        k, pk = emu.get_smeared_bao_pk(**params, k=kk)
        pk_tab = np.array([1.62870070e+04, 1.77438867e+04, 1.16350610e+04, 6.52558247e+03,
       2.45416259e+03, 7.34044484e+02, 1.87901947e+02, 4.23275559e+01,
       8.67997917e+00, 1.66034432e+00])
        for i,j in zip(pk,pk_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

    def test_get_nonlinear_pk(self):
        k, pk = emu.get_nonlinear_pk(**params, k=kk, baryonic_boost=True)
        pk_tab = np.array([16307.12755312, 17671.70187069, 11491.80970052,  6462.74744049,
        2566.44477746,   970.08463921,   414.21457043,   199.16121891,
          86.88448184,    28.13808688])
        for i,j in zip(pk,pk_tab):
            self.assertAlmostEqual(np.round(i / j, dec_prec), 1)

    def test_get_sigma8(self):
        sigma8 = emu.get_sigma8(**params)
        self.assertAlmostEqual(np.round(sigma8 / 0.7861695, dec_prec), 1)


if __name__ == '__main__':
    unittest.main()
