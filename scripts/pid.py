#!/usr/bin/env python
import numpy as np
#from matplotlib import pyplot as plt
from numpy.random import *

def main():
    M = 1.00
    M1 = 0.00

    e = 0.00
    e1 = 0.00
    e2 = 0.00
    
    Kp = 0.10
    Ki = 0.10
    Kd = 0.10

    t = 100
    
    goal = 50.00

    x_list = []
    y_list = []

    x_list.append(0)
    y_list.append(0.00)

    for i in range(1,t):
        M1 = M
        e1 = e
        e2 = e1
        e = goal - y_list[i-1]

        M = M1 + Kp * (e-e1) + Ki * e + Kd * ((e-e1) - (e1-e2))
        
        y_list.append(M)
        x_list.append(i)
    print M
"""
    plt.plot(x_list, y_list)
    plt.ylim(0, goal*2)
    plt.show()
"""
#print M

if __name__ == "__main__":
    main()
