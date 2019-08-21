
from matplotlib.pylab import *

def tiempo(s):
    d = int(s/(24*60*60.))
    h = int((s%(24*60*60.))/(60*60.))
    m = int(((s%(24*60*60.))%(60*60.))/60.)
    s = int(((s%(24*60*60.))%(60*60.))%60.)
    
    return '{} d {} h {} m {} s '.format(d,h,m,s)

a = 1. #Ancho del dominio
b = 1. #Largo del dominio
c = 1. #Alto del dominio
Nx = 10 #Numero de intervalos en x
Ny = 10 #Numero de intervalos en y
Nz = 10 #NUmero de intervalos en z

dx = b/Nx # discretizacion espacial en x
dy = a/Ny # discretizacion espacial en y
dz = c/Nz # discretizacion espacial en z

h = dx  # = dy = dz

if dx != dy or dx != dz or dy != dz: # asumimos en formula
	print('ERROR!!!!! dx != dy or dx != dz or dy != dz')
	exit(-1)

#Funcion para calcular coordenadas del punto (i,j,k)

coords = lambda i,j,k : (dx*i, dy*j, dz*k)
x,y,z = coords(4,2,5)

print "x = ", x
print "y = ", y
print "z = ", z

u_n = zeros((Nx+1,Ny+1,Nz+1),dtype=double)
u_nm1 = zeros((Nx+1,Ny+1,Nz+1),dtype=double)



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
alpha = K*dt/(c*rho) #sacamos h**2 y lo pusimos en el nabla

print "dt = ",dt 
print "dx = ",dx
print "dy = ",dy
print "dz = ",dz
print "K = ",K
print "c = ",c
print "rho = ",rho
print "alpha = ",alpha


n_max=24*60#*7 # intervalos 
n = 0

T = 24*3600 #perioddo

#CB inicial
u_n[:,:,:] = 20.


#Creo imagen
imshowbien(u_n[:,:,0])
title("Cara expuesta al ambiente\nk = {} t = {}".format(n, tiempo(n*dt)))
colorbar()
savefig("movie/frame_{0:05.0f}.png".format(n)) #guardo frame
close(1)





#Loop en el tiempo
for n in range(n_max):
    t = dt*n
    
    u_ambiente = 20. + 10.*sin((2*pi/T)*t)

    # CB esenciales
    #u_n[-1,:] = 20.
    #u_n[0,:] = 20.
    #u_n[:,0] = 20.
    u_n[:,:,0] = u_ambiente 

    
    # Loop en el espacio i = 1  ... n - 1 u_nm1[0] = 0 u_nm1[n] =  por las condiciones de borde
    for i in range(1,Nx): 
    	for j in range(1,Ny): 
            for k in range(1,Nz):
    	        
                #algoritmo de diferencias finitas  3-D para difusion
    	        #Laplaciano
    	        nabla_u_n = (u_n[i+1,j,k] + u_n[i-1,j,k] + u_n[i,j+1,k] + u_n[i,j-1,k] +u_n[i,j,k+1] + u_n[i,j,k-1] - 6*u_n[i,j,k])/(h**2)

    	        #Forward euler
    	        u_nm1[i,j,k] = u_n[i,j,k] + alpha*nabla_u_n




    #CB natural
    u_nm1[Nx,:,:] = u_nm1[Nx-1,:,:]
    u_nm1[0,:,:] = u_nm1[1,:,:]
    u_nm1[:,Ny,:] = u_nm1[:,Ny-1,:]
    u_nm1[:,0,:] = u_nm1[:,1,:]
    u_nm1[:,:,Nz] = u_nm1[:,:,Nz-1]
    
    u_n = u_nm1

    imshowbien(u_n[:,:,0])
    title("Cara expuesta al ambiente\nn = {} t = {}".format(n, tiempo(n*dt)))
    colorbar()
    savefig("movie/frame_{0:05.0f}.png".format(n)) #guardo frame
    close(1)
	



