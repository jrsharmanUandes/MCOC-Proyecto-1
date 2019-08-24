from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

from matplotlib.pylab import *

with open('Tempmin.csv', 'rb') as f: #abrimos el csv
	reader = csv.reader(f)
	temperatura = list(reader)

temp1 = []
minutos1 = []

for dato in temperatura:
	temp1.append(float(dato[0]))
	minutos1.append(float(dato[1])-float(temperatura[0][1]))

print temp1[0]
print minutos1[0]

#funcion interpolado para todos los minutos
f_interp = InterpolatedUnivariateSpline(minutos1,temp1,k=3)

 #listas para guardar l
temp2=[]
minutos2=[]

for i in range(int(minutos1[-1])):
	minutos2.append(i)
	temp2.append(float(f_interp(i)))


# hacemos una funcion para el tiempo
def tiempo(s):                                      # Define la funcion tiempo para graficar DDHHMMSS
    d = int(s/(24*60*60.))                          # La cantidad de dias
    h = int((s%(24*60*60.))/(60*60.))               # El resto de los dias para calcular las horas restantes
    m = int(((s%(24*60*60.))%(60*60.))/60.)         # El resto de las horas para calcular los minutos restantes
    s = int(((s%(24*60*60.))%(60*60.))%60.)         # El resto de los minutos son los segudnos
    
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

razon = 496.7*10/(Nx**3) #cantidad de gramos por cada dicretizacion(496.7 gramos/m^3)
print "asd",razon
#funcion Q(t) para el hormigon
def q_t(t):                                         # Define como se comporta q_t durante el tiempo
    tiempo = t # Transforma el tiempo en segundos a horas
    if tiempo < 1.5: 
        return 0                               
    elif tiempo < 10:                                # Dado que el comportamiento de la funcion es distinto en las primeras 10 horas comprueba si se encuentra en este periodo
        return ((1.0347 * 2 * tiempo - 3.1016)/60.)*razon  # Ecuacion de q_t dentro de las primeras 10 horas
    else: 
                                                  # Despues de las primeras dies horas se comporta de esta forma
        return ((98.845 / tiempo)/60.)*razon  # Ecuacion de q_t despues de las 10 horas




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
	imshow(u.T[:,Ny::-1],vmin=20,vmax=80)#imshow(u.T[Nx::-1,:],vmin=20,vmax=80) # saque el .T


#Parametros del bloque (hormigon)
dt = 60.  #s
K = 79.5*60 # m^2 / s
c = 450*3600. # J / kg C
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


n_max=24*60*14#*7 # intervalos 
n = 0

T = 24*3600 #perioddo

#CB inicial
u_n[:,:,:] = 20.

#guardo para graficarffmpeg -i foto_%03d.png final.mp4
x=[]
y=[]


'''
#Creo imagen
imshowbien(u_n[Nx/2,:,:])
title("Corte transversal\nk = {} t = {}".format(n, tiempo(n*dt)))
colorbar()
savefig("movie/frame_{0:05.0f}.png".format(n)) #guardo frame
close(1)
'''



#Loop en el tiempo
for n in range(n_max):
    t = dt*n
    if n % 60 == 0:
    	u_ambiente = temp2[n/60]

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
    	        u_nm1[i,j,k] = u_n[i,j,k] + alpha*nabla_u_n + q_t(n)
                
 

    #CB natural
    u_nm1[Nx,:,:] = u_nm1[Nx-1,:,:]
    u_nm1[0,:,:] = u_nm1[1,:,:]
    u_nm1[:,Ny,:] = u_nm1[:,Ny-1,:]
    u_nm1[:,0,:] = u_nm1[:,1,:]
    u_nm1[:,:,Nz] = u_nm1[:,:,Nz-1]
    
    u_n = u_nm1
    if n % 120 == 0:
        x.append(n*dt)
        y.append(u_n[Nx/2,Ny/2,Ny])
        '''
        #Creo imagen
        #imshowbien(u_n[Nx/2,:,:])
        #title("Corte transversal\nk = {} t = {}".format(n, tiempo(n*dt)))
        #colorbar()
        #savefig("movie/frame_{0:05.0f}.png".format(n)) #guardo frame
        #close(1)
        '''
plt.plot(x,y)

title("Punto 6",size=30)
xlabel("Tiempo en minutos")
ylabel("Temeperatura Celsius")
savefig("movie/Punto 6.png")
show()
    


