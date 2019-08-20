
from matplotlib.pylab import *

a = 1. #Ancho del dominio
b = 1. #Largo del dominio
Nx = 100 #Numero de intervalos en x
Ny = 100 #Numero de intervalos en x

dx = b/Nx # discretizacion espacial en x
dy = a/Ny # discretizacion espacial en y

h = dx  # = dy

if dx != dy: # asumimos en formula
	print('ERROR!! dx != dy')
	exit(-1)

#Funcion para calcular coordenadas del punto (i,j)

coords = lambda i,j : (dx*i, dy*j)
x,y = coords(4,2)

print "x = ", x
print "y = ", y

u_k = zeros((Nx+1,Ny+1),dtype=double)
u_km1 = zeros((Nx+1,Ny+1),dtype=double)


#CB esencial
u_k[0,:] = 20.
u_k[:,0] = 20.


#Funciones para facilitar 
def printbien(u):
	print u.T[Nx::-1,:]

print u_k

def imshowbien(u):
	imshow(u.T[Nx::-1,:],vmax=30)


#Parametros de la barra (hormigon)
dt = 60.  #s
K = 79.5 # m^2 / s
c = 450. # J / kg C
rho = 7800. # kg/ m^3
alpha = 0.001#K*dt/(c*rho*dx**2)

print "dt = ",dt 
print "dx = ",dx
print "K = ",K
print "c = ",c
print "rho = ",rho
print "alpha = ",alpha
k_max=1000
k= 0

T = 24*3600 #perioddo
#figure(1)
#imshowbien(u_k)
#title("k = {} t = {} s".format(k, k*dt))
#show()
imshowbien(u_k)
title("k = {} t = {} s".format(k, k*dt))
savefig("movie/frame_{0:04.0f}.png".format(k)) #guardo frame
colorbar()
close(1)
#Loop en el tiempo

#CB inicial
u_k[:,:] = 20.

printbien(u_k)

for k in range(k_max):
    t = dt*k
    
    u_ambiente = 20. + 10*sin((2*pi/T)*t)


    # CB esenciales
    u_k[-1,:] = 20.
    u_k[0,:] = 20.
    u_k[:,0] = 20.
    u_k[:,-1] = u_ambiente = 20. + 10*sin((2*pi/T)*t)

    #if k <= k_max/4:
    
    # Loop en el espacio i = 1  ... n - 1 u_km1[0] = 0 u_km1[n] =  por las condiciones de borde
    for i in range(1,Nx): #estaba Nx-1
    	for j in range(0,Ny): #estaba Ny-1
	        #algoritmo de diferencias finitas  2-D para difusion
	        #Laplaciano
	        nabla_u_k = (u_k[i-1,j] + u_k[i+1,j] + u_k[i,j-1] + u_k[i,j+1] - 4*u_k[i,j])/(h**2)

	        #Forward euler
	        u_km1[i,j] = u_k[i,j] + alpha*nabla_u_k




    #CB natural
    u_km1[Nx,:] = u_km1[Nx-1,:]
    u_km1[:,0] = u_km1[:,1]
    u_km1[0,:] = u_km1[1,:]
    
    # avanza la solucion a k +1
    
    u_k = u_km1
#printbien(u_k)
    imshowbien(u_k)
    title("k = {} t = {} s".format(k, k*dt))
    colorbar()
#show()
    savefig("movie/frame_{0:04.0f}.png".format(k)) #guardo frame
    close(1)
	



