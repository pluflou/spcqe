import cvxpy as cp
from spcqe.functions import basis, make_regularization_matrix


def solve_cvx(data, num_harmonics, periods, weight, percentiles, solver, verbose):
    problem, basis = make_cvx_problem(num_harmonics, periods, weight, percentiles)
    problem.solve(solver=solver, verbose=verbose)
    theta = problem.variables()[0]
    quantiles = basis @ theta.value
    return quantiles, basis


def make_cvx_problem(data, num_harmonics, periods, weight, percentiles):
    length = len(data)
    B = basis(num_harmonics, length, periods)
    D = make_regularization_matrix(num_harmonics, weight, periods)
    a, b = pinball_slopes(percentiles)
    num_quantiles = len(a)
    Theta = cp.Variable((B.shape[1], num_quantiles))
    BT = B @ Theta
    nonnanindex = ~np.isnan(y1)
    Var = y1[nonnanindex].reshape(-1, 1) - BT[nonnanindex]
    obj = cp.sum(Var @ np.diag(a) + cp.abs(Var) @ np.diag(b))
    # ensures quantiles are in order and prevents point masses ie minimum distance.
    cons = [cp.diff(BT, axis=1) >= 0.01]
    # cons+=[BT[:,0]>=0] #ensures quantiles are nonnegative
    Z = D @ Theta
    regularization = cp.sum_squares(Z)
    obj += regularization
    prob = cp.Problem(cp.Minimize(obj), cons)
    return prob, B
