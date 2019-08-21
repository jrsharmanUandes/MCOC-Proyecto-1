
from matplotlib.pylab import *

def tiempo(s):
    d = int(s/(24*60*60.))
    h = int((s%(24*60*60.))/(60*60.))
    m = int(((s%(24*60*60.))%(60*60.))/60.)
    s = int(((s%(24*60*60.))%(60*60.))%60.)
    
    return '{} d {} h {} m {} s '.format(d,h,m,s)

a = 25. #Ancho del dominio
b = 25. #Largo del dominio
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



def imshowbien(u):
	imshow(u.T[Nx::-1,:],vmin=10,vmax=30)


#Parametros del bloque (hormigon)
dt = 60.  #s
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
k_max=24*60*7 # intervalos 
k= 0

T = 24*3600 #perioddo

#Creo imagen
imshowbien(u_k)
title("k = {} t = {}".format(k, tiempo(k*dt)))
savefig("movie/frame_{0:05.0f}.png".format(k)) #guardo frame
colorbar()
close(1)


#CB inicial
u_k[:,:] = 20.


#Loop en el tiempo
for k in range(k_max):
    t = dt*k
    
    u_ambiente = 20. + 10.*sin((2*pi/T)*t)

    # CB esenciales
    #u_k[-1,:] = 20.
    #u_k[0,:] = 20.
    #u_k[:,0] = 20.
    u_k[:,-1] = u_ambiente 

    #if k <= k_max/4:
    
    # Loop en el espacio i = 1  ... n - 1 u_km1[0] = 0 u_km1[n] =  por las condiciones de borde
    for i in range(1,Nx): 
    	for j in range(1,Ny): 
	        
            #algoritmo de diferencias finitas  2-D para difusion
	        #Laplaciano
	        nabla_u_k = (u_k[i-1,j] + u_k[i+1,j] + u_k[i,j-1] + u_k[i,j+1] - 4*u_k[i,j])/(h**2)

	        #Forward euler
	        u_km1[i,j] = u_k[i,j] + alpha*nabla_u_k




    #CB natural
    u_km1[Nx,:] = u_km1[Nx-1,:]
    u_km1[0,:] = u_km1[1,:]
    u_km1[:,Ny] = u_km1[:,Ny-1]
    u_km1[:,0] = u_km1[:,1]
    
    u_k = u_km1

    imshowbien(u_k)
    
    title("k = {} t = {}".format(k, tiempo(k*dt)))
    colorbar()
    savefig("movie/frame_{0:05.0f}.png".format(k)) #guardo frame
    close(1)
	



