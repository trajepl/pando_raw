import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

plt.style.use('./tickstyle')
with plt.style.context(('./tickstyle')):
    x1 = np.linspace(0, 1, 11)
    y1 = [0.52, 0.55, 0.57, 0.60, 0.62, 0.63, 0.60, 0.59, 0.58, 0.54, 0.53]

    fig, (ax2) = plt.subplots(nrows=1, ncols=1, figsize=(11, 5))

    # ax1.set_xlabel(r'$\alpha$', fontsize=17)
    # ax1.set_ylabel(r'$Spearman\ correlation\  (\rho$)', fontsize=17)
    # ax1.set_ylim(0.4,0.7)
    # ax1.plot(x1, y1, 'ro-')


    y21 = [0.836, 0.843, 0.860, 0.837, 0.802, 0.778, 0.725, 0.682, 0.677, 0.654, 0.632]
    y22 = [0.812, 0.834, 0.857, 0.833, 0.794, 0.768, 0.711, 0.675, 0.650, 0.623, 0.593]
    y23 = [0.645, 0.733, 0.826, 0.814, 0.735, 0.640, 0.602, 0.595, 0.573, 0.541, 0.527]


    # ax2.set_title('Performance with various value of lambda')
    # ax2.set_ylim(0,1)

    ax2.set_xlabel(r'$\lambda$', fontsize=18)
    ax2.set_ylabel(r'$Spearman\ correlation\  (\rho$)', fontsize=18)
    ax2.plot(x1, y21, 'b*-', label='MC',)
    ax2.plot(x1, y22, 'ro-', label='RG')
    ax2.plot(x1, y23, 'g.-', label='WS353')
    ax2.legend()

plt.grid(axis='y')
# plt.show()
plt.savefig('./params_lambda.eps', format='eps')