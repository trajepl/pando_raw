import matplotlib.pyplot as plt
import numpy as numpy

fig_s = (8, 120)
format_f = 'pdf'
title = ''
x = [50, 100, 150, 200]

def autoline(data, ax, title, i, xlabel='', ylabel='Spearman'):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axis([25, 225, 0.3, 1])
    
    ax.plot(x,data[1],linewidth=2,label="weighted", color='r',marker='+',markerfacecolor='yellow',markersize=6)
    ax.plot(x,data[0],linewidth=2,label="cloest", color='g',marker='*',markerfacecolor='blue',markersize=6)
    ax.legend()

def point_line(data, fn):
    plt.style.use('./tickstyle')
    with plt.style.context(('./tickstyle')):
        fig, ax = plt.subplots(nrows=3, ncols=2, figsize=fig_s, sharex=True, sharey=True)
        autoline(data[0], ax[0][0], title, 0, xlabel='MC-Rel-30')
        autoline(data[1], ax[0][1], title, 0, xlabel='MC-Sim-30')
        autoline(data[2], ax[1][0], title, 0, xlabel='RG-65')
        autoline(data[3], ax[1][1], title, 0, xlabel='rel122')
        autoline(data[4], ax[2][0], title, 0, xlabel='wordrel')
        autoline(data[5], ax[2][1], title, 0, xlabel='average')
    plt.show();
    # plt.savefig(fn, format=format_f)

if __name__ == '__main__':
    data= [
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
        [[0.68, 0.68, 0.63, 0.63],[0.70, 0.78, 0.77, 0.71]],
    ]
    
    
    point_line(data, 'dim')

    # plt.plot(x1,y1,linewidth=2,label="weighted", color='r',marker='o',markerfacecolor='yellow',markersize=6)
    # plt.plot(x1,y2,linewidth=2, label="closest", color='green',marker='*',markerfacecolor='blue',markersize=6)
    # plt.xlabel('Plot Number')
    # plt.ylabel('Important var')
    # plt.title('Interesting Graph\nCheck it out')
    # plt.legend()
    # plt.show()