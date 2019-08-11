# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:42:50 2019

@author: johns
"""


from matplotlib.pylab import *
import scipy as sp

def findMiddle(imput_list):
    middle = float(len(imput_list))/2
    if middle % 2 != 0:
        return imput_list[int(middle - .5)]
    else:
        return (imput_list[int(middle)], imput_list[int(middle - 1)])

L = 1.      #largo del dominio
n = 100     #numero de intervalos

DT = linspace(0.1, 2, 100)
N = linspace(10, 100, 100)
U = sp.zeros((100,100))

for (u1,dt) in enumerate(DT):
    for (u2,n) in enumerate(N):
        n = int(n)
        dx = L/n
        x = linspace(0,L,n+1)
        
    

        #Condicion inicial
        
        def fun_u0(x):
            return 10*exp(-(x-0.5)**2/0.1**2)
            
        u0 = fun_u0(x)
         #Creo el vector u para tiempo k
        u_k = u0.copy()
        
        #condiciones de borde
        u_k[0] = 0.
        u_k[n] = 20.
        
        #tEMPERATURA EN EL TIEMPO K+1 
        u_km1 = u_k.copy()
        
        
        
        #Parametros de la barra (hierro)
        dt = 1.  #s
        K = 79.5 # m^2 / s
        c = 450. # J / kg C
        rho = 7800. # kg/ m^3
        alpha = K*dt/(c*rho*dx**2)
        
        #print "dt = ",dt 
        #print "dx = ",dx
        #print "K = ",K
        #print "c = ",c
        #print "rho = ",rho
        #print "alpha = ",alpha
        
        plot(x,u0,"k--")
        
        #Loop en el tiempo
        k= 0
        
        for k in range(10000):
            t = dt*k
            #print "k = ", k, "t = ",t
            
            #condiciones de borde
            if k< 100:
            #u_k[0] = 0.
                u_k[n] = 20.
            
            # Loop en el espacio i = 1  ... n - 1 por las condiciones de borde
            for i in range(0,n):
                u_km1[i]= u_k[i] + alpha*(u_k[i+1]-2*u_k[i]+u_k[i-1])   #algoritmo de diferencias finitas  1-D para difusion
                 
        try:
            U[u1][u2] = findMiddle(u_k)[0] 
        except:
            U[u1][u2] = findMiddle(u_k)        

imshow(U, cmap = 'hot', interpolation = 'nearest', origin = 'lower')
xlabel('dt')
ylabel('dx')
colorbar()
show()