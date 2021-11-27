from phi import math


def sin_loss(x: math.Tensor, a: math.Tensor):
    return math.l1_loss(math.sin(a/x) + 1, batch_norm=False)


def closest_min(x, a):
    # n=0 is the furthest positive minimum
    # n=-1 is the furthest negative minimum
    closest_n = math.round(a / x / 2 / math.PI - 0.75)
    closest_n_pos = math.maximum(closest_n, math.wrap(0))
    closest_n_neg = math.minimum(closest_n, math.wrap(-1))
    closest_n = math.where(x * a >= 0, closest_n_pos, closest_n_neg)
    result = a / (1.5 * math.PI + closest_n * 2 * math.PI)
    return result


sin_loss_grad = math.functional_gradient(sin_loss, get_output=True)


def eval_delta(a, x, method):
    if method == 'GD':  # GD clipped
        _, grad = sin_loss_grad(x, a)
        return - math.clip(grad / grad.shape.volume, -1, 1)
    elif method == 'IG':  # IG clipped
        _, grad = sin_loss_grad(x, a)
        height = math.sin(a / x) + 1  # This is domain knowledge
        result = - math.where(abs(height) == 0, 0, math.clip(height / grad, -1, 1))
        return result
    elif method.startswith('Supervised'):  # Supervised
        x0 = math.random_uniform(a.shape) if method.endswith('random') else float(method[len('Supervised_'):])
        return closest_min(x0, a) - x
    elif method == 'PG':  # Physical Gradient
        return closest_min(x, a) - x
    elif method == 'Newton':  # Newton's method clipped
        grad_hess = math.clip(x ** 2 / (a * math.tan(a / x) - 2 * x), -1, 1)
        # delta = -(d/dx sin(a/x)) / (d^2/dx^2 sin(a/x))  plot sin(a/x) and (x^2 cos(a/x))/(2 x cos(a/x) - a sin(a/x)) from x=0.01 to 1
        return abs(grad_hess) * -math.sign(sin_loss_grad(x, a)[1])  # move away from maxima
    else:
        raise ValueError(method)
