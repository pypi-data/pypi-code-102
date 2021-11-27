from phi import math
from phi import field
from phi.field import Grid, SampledField, center_of_mass, Field, StaggeredGrid, Grid

from . import diffuse, advect, Domain, fluid


# def unidirectional_advection_loss(velocity, source_dist, target_dist, diffusion=2.):
#     diffused_source = diffuse.fourier(source_dist, diffusion, 1)
#     m12 = advect.semi_lagrangian(diffused_source, velocity, 1)
#     norm = math.stop_gradient(field.mean(source_dist))
#     return field.frequency_loss((m12 - target_dist) / norm, n=1, frequency_falloff=80, ignore_mean=True, batch_norm=False)
#
#
# def bidirectional_advection_loss(velocity, dist1, dist2, diffusion=2.):
#     l1 = unidirectional_advection_loss(velocity, dist1, dist2, diffusion=diffusion)
#     l2 = unidirectional_advection_loss(-velocity, dist2, dist1, diffusion=diffusion)
#     return 0.5 * (l1 + l2)
#
#
# unidirectional_advection_delta = field.functional_gradient(unidirectional_advection_loss)
# bidirectional_advection_delta = field.functional_gradient(bidirectional_advection_loss, get_output=True)
#
#
# def divergence_free_optimal_transport(dist1: AbstractGrid,
#                                       dist2: AbstractGrid,
#                                       domain: Domain,
#                                       vtype: type = Grid,
#                                       lr=100.,
#                                       smooth=1.,
#                                       iterations=10) -> AbstractGrid:
#     mean_shift = field.center_of_mass(dist2) - field.center_of_mass(dist1)
#     velocity = domain.vector_grid(mean_shift, type=vtype)  # initial guess
#     for step in range(iterations):
#         gradient = 0
#         loss = None
#         for _ in range(2):
#             loss_n, gradient_n = bidirectional_advection_delta(velocity - lr * gradient / 2, dist1, dist2)
#             loss = loss if loss is not None else loss_n
#             gradient += gradient_n
#         gradient = diffuse.explicit(gradient, smooth, 1, substeps=10)
#         gradient, *_ = fluid.make_incompressible(gradient, domain)
#         field.mean(field.vec_squared(gradient))
#         velocity -= lr * gradient
#     return velocity

# def divergence_free_optimal_transport(dist1: AbstractGrid,
#                                       dist2: AbstractGrid,
#                                       vtype: type = Grid,
#                                       smoothness=1.,
#                                       solve_linear=math.Solve('L-BFGS-B', 0, 1e-10)) -> AbstractGrid:
#     linear_velocity = center_of_mass(dist2) - center_of_mass(dist1)
#     potential_fft = Domain(resolution=dist1.resolution, bounds=dist1.bounds).vector_potential(0j, curl_type=vtype, extrapolation=dist1.extrapolation)
#
#     def pot_to_vel(pot_freq):
#         vec_pot = pot_freq.with_(values=math.real(math.ifft(pot_freq.values)))  # grad(abs)=0 at 0.
#         curl_vel = field.curl(vec_pot, type=vtype)
#         return curl_vel + linear_velocity
#
#     def loss(vec_pot_freq: AbstractGrid):
#         k = math.vec_abs(math.fftfreq(vec_pot_freq.shape.spatial))
#         mask = k < 0.01
#         vec_pot_freq *= mask
#         vel = pot_to_vel(vec_pot_freq)
#         adv_loss = bidirectional_advection_loss(vel, dist1, dist2)
#         # smooth_loss = math.l2_loss(vec_pot_freq.values) * smoothness
#         return adv_loss + 1 * field.l2_loss(vel)
#
#     try:
#         potential_fft = field.minimize(loss, x0=potential_fft, solve=solve_linear)
#         return pot_to_vel(potential_fft)
#     except math.ConvergenceException as exc:
#         raise type(exc)(solve_linear, None, pot_to_vel(exc.x), exc.msg)
