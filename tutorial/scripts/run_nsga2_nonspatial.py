#problem

import numpy as np
from pymoo.model.problem import Problem

class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_constr=2,
                         xl=np.array([-2,-2]),
                         xu=np.array([2,2]))

    def _evaluate(self, X, out, *args, **kwargs):
       f1 = (X[:, 0]**2 + X[:, 1]**2)
       f2 = -(X[:, 0] - 1)**2 - X[:, 1]**2
       f2 = f2 * -1
       g1 = 2*(X[:, 0]-0.1) * (X[:, 0]-0.9) / 0.18
       g2 = - 20*(X[:, 0]-0.4) * (X[:, 0]-0.6) / 4.8
       out["F"] = np.column_stack([f1, f2])
       out["G"] = np.column_stack([g1, g2])

problem = MyProblem()
print(problem)

#algorithm

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm = NSGA2(
    pop_size= 40,
    n_offsprings= 10,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True
)

#termination

from pymoo.factory import get_termination

termination = get_termination("n_gen", 1000)

#optimization

from pymoo.optimize import minimize
res = minimize(problem,
    algorithm,
    termination,
    seed=1,
    save_history=True,
    verbose=True)

print(res)
print(res.X)
print(res.F)

#visualization

import matplotlib.pyplot as plt
# Plot the design space
f1, ax1 = plt.subplots(1)
ax1.scatter(res.X[:,0], res.X[:,1], s=30, fc='none', ec='r')
ax1.set_title('design space')
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
f1.savefig('design_space.png')
# Plot the objective space
f2, ax2 = plt.subplots(1)
ax2.scatter(res.F[:,0], res.F[:,1], s=30, fc='none', ec='k')
ax2.set_title('objective space')
ax2.set_xlabel('f1')
ax2.set_ylabel('f2')
f2.savefig('objective_space.png')
