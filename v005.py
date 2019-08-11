# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:42:50 2019

@author: johns
"""


from matplotlib.pylab import *

L = 1.      #largo del dominio
n = 100     #numero de intervalos

dx = L / n  #discretizacion

# Vector con todos los x  del espacio
x = linspace(0, L, n+1)

#Condicion inicial

def fun_u0(x):
    return 10*exp(-(x-0.5)**2/0.1**2)
    
u0 = fun_u0(x)
 #Creo el vector u para tiempo k
u_k = u0.copy()

#condiciones de borde
u_k[0] = 0.
u_k[n] = 0.

#tEMPERATURA EN EL TIEMPO K+1 
u_km1 = u_k.copy()



#Parametros de la barra (hierro)
dt = 1.  #s
K = 79.5 # m^2 / s
c = 450. # J / kg C
rho = 7800. # kg/ m^3
alpha = K*dt/(c*rho*dx**2)

print "dt = ",dt 
print "dx = ",dx
print "K = ",K
print "c = ",c
print "rho = ",rho
print "alpha = ",alpha

plot(x,u0,"k--")

#Loop en el tiempo
k= 0

for k in range(4000):
    t = dt*k
    #print "k = ", k, "t = ",t
    
    #condiciones de borde
    #u_k[n] = 20.
    
    # Loop en el espacio i = 1  ... n - 1 por las condiciones de borde
    for i in range(0,n+1):
        if i == n :
            u_km1[i]= u_k[i] + alpha*(-u_k[i]+u_k[i-1])
        elif i == 0 :
            u_km1[i]= u_k[i] + alpha*(u_k[i+1]-u_k[i])
        else:
            u_km1[i]= u_k[i] + alpha*(u_k[i+1]-2*u_k[i]+u_k[i-1])   #algoritmo de diferencias finitas  1-D para difusion
            
            
    # avanza la solucion a k +1
    u_k = u_km1
    if k % 200 == 0:    #Plotea cierta cantidad de lineas
        plot(x,u_k)


title("k = {} t = {} s".format(k, k*dt))