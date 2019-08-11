from matplotlib.pylab import *
import numpy 

L = 1.      #largo del dominio
n = 100     #numero de intervalos



dx = L / n  #discretizacion

# Vector con todos los x  del espacio
x = linspace(0, L, n+1)
print x

#Creo el vector u_k para tiempo k con condicion inicial 1 en el tercio del medio

u_k = zeros(len(x))
for i in range(len(u_k)/3,2*len(u_k)/3):
    u_k[i] = 1.

#Temperatura en el tiempo k + 1
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

plot(x,u_k,"k--")

#Loop en el tiempo
k= 0

for k in range(4000):
    t = dt*k
    
    #condiciones de borde
    if k < 10: #durante los primeros 10 segundos
    #u_k[0] = 0.
        for i in range(len(u_k)/3,2*len(u_k)/3): # en el tercio medio de la barra
            # luego sube 1/3 la temperatura anterior
            u_km1[i]= u_k[i] + 1 + alpha*(u_k[i+1]-2*u_k[i]+u_k[i-1])   #algoritmo de diferencias finitas  1-D para difusion

    
    # Loop en el espacio i = 1  ... n - 1 por las condiciones de borde
    for i in range(0,n+1):
        # condicionales para simular barra sin perdida de calor
        if i == n :
            u_km1[i]= u_k[i] + alpha*(-u_k[i]+u_k[i-1])
        elif i == 0 :
            u_km1[i]= u_k[i] + alpha*(u_k[i+1]-u_k[i])
        else:
            u_km1[i]= u_k[i] + alpha*(u_k[i+1]-2*u_k[i]+u_k[i-1])   #algoritmo de diferencias finitas  1-D para difusion
            
            
    # avanza la solucion a k +1
    u_k = u_km1
    if  k % 250 == 0 or k <= 10:   #Plotea cierta cantidad de lineas
        plot(x,u_k)


title("k = {} t = {} s".format(k, k*dt))
show()
