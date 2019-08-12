
from matplotlib.pylab import *

L = 1. #largo del dominio
n = 100 #numero de intervalos

dx = L / n # discretizacion

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
u_k[n] = 20.

#Temperatura en tiempo k+1
u_km1 = u_k.copy()

#Parametros de la barra (hormigon)
dt = 1.  #s
K = 1.63 # m^2 / s
c = 880. # J / kg C
rho = 2400. # kg/ m^3
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

for k in range(500000):
    t = dt*k
    #print "k = ", k, "t = ",t
    
    #condiciones de borde
    u_k[0] = 0.
    u_k[n] = 20.
    
    # Loop en el espacio i = 1  ... n - 1 por las condiciones de borde
    for i in range(1,n):
        #algoritmo de diferencias finitas  1-D para difusion
        u_km1[i]= u_k[i] + alpha*(u_k[i+1]-2*u_k[i]+u_k[i-1])
    # avanza la solucion a k +1
    #print u_km1[0]
    u_k = u_km1
    if k % 10000 == 0:
        plot(x,u_k)

show()

title("k = {} t = {} s".format(k, k*dt))
