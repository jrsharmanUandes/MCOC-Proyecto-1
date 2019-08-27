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

razon = 496.7*1000   #cantidad de gramos de cemento seco para generar un metro cubico de hormigon (496700 g/m^3)

print "razon = ",razon

#funcion Q(t) para el hormigon
def q_t(t):                                             # Define como se comporta q_t durante el tiempo (Entrega J/m3)
    tiempo = t/3600.                                    # Transforma el tiempo en segundos a horas
    if tiempo < 1.5:                                    #En la primera hora y media no existe reaccion exotermica
        return 0                               
    elif tiempo < 15:                                   # Dado que el comportamiento de la funcion es distinto en las primeras 10 horas comprueba si se encuentra en este periodo
        return ((1.0347 * 2 * tiempo - 3.1016)/60.**2)*razon  # Ecuacion de q_t dentro de las primeras 10 horas
    elif tiempo >= 15 and tiempo < 19:					# en este intervalo la curva empieza a cambiar de forma no t
    	return (-1.0762 * tiempo +26.471)*razon/3600.
    elif -0.1234*t + 7.7239 >= 0:                       # Verifica de que q(t) no sea negativo (Esto es dado que la ecuacion es lineal y en algun momento se torna negativa)
                                                        # Despues de las primeras dies horas se comporta de esta forma
        return ((-0.1234*t + 7.7239)/60.**2)*razon      # Ecuacion de q_t despues de las 10 horas
    else:
        return 0




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
	imshow(u.T[:,Ny::-1],vmin=20,vmax=80) #imshow(u.T[Nx::-1,:],vmin=20,vmax=80) # saque el .T


#Parametros del bloque (hormigon)
dt = 1.                     # s
K = 1.63                    # J/(m*s*K)
c = 0.880                   # J/(g*K)
rho = 2400000.              # g/m^3
alpha = K*dt/(c*rho*h**2)   # Adimencional

# Parametros del aire para calcular condicion de borde al exterior
K_aire = 0.02
c_aire = 1.012
rho_aire = 1225
alpha_aire = K_aire*dt/(c_aire*rho_aire*h**2)

print "dt = ",dt 
print "dx = ",dx
print "dy = ",dy
print "dz = ",dz
print "K = ",K
print "c = ",c
print "rho = ",rho
print "alpha = ",alpha
print "alpha_aire = ",alpha_aire


n_max=24*60*60*13   # Tiempo a analizar en s [13 dias]

#CB inicial
u_n[:,:,:] = 20.

#guardo para graficarffmpeg -i foto_%03d.png final.mp4
x=[]
y1=[]
y2=[]
y3=[]
y4=[]
#Contador
contador= 0

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
    if n % 60 == 0: #cada 60 segundos actualiza la temperatura ambiente
    	try:
    		u_ambiente = temp2[n/60]
    	except:
    		break

    # CB esenciales
    #u_n[-1,:] = 20.
    #u_n[0,:] = 20.
    #u_n[:,0] = 20.

    
    # Loop en el espacio i = 1  ... n - 1 u_nm1[0] = 0 u_nm1[n] =  por las condiciones de borde
    for i in range(1,Nx): 
    	for j in range(1,Ny): 
            for k in range(0,Nz):
    	        
                #algoritmo de diferencias finitas  3-D para difusion
    	        #Laplaciano
                if k == 0:      #se calcula la temperatura del borde expuesto utilizando un alfa que es la razon de conduccion de temperatura en el aire
                    nabla_u_n = (u_n[i+1,j,k] + u_n[i-1,j,k] + u_n[i,j+1,k] + u_n[i,j-1,k] +u_n[i,j,k+1] + alpha_aire/alpha*u_ambiente - 5*u_n[i,j,k] - alpha_aire/alpha*u_n[i,j,k])

                else:           #se calcula la temperaturda dentro del bloque
                    nabla_u_n = (u_n[i+1,j,k] + u_n[i-1,j,k] + u_n[i,j+1,k] + u_n[i,j-1,k] +u_n[i,j,k+1] + u_n[i,j,k-1] - 6*u_n[i,j,k])

    	        #Forward euler
    	        u_nm1[i,j,k] = u_n[i,j,k] + alpha*nabla_u_n + q_t(n)/(c*rho) #q(t) entrega J/m3 por lo que se divide en c y rho para transofrmarlo en temperatura

    

    #CB natural
    u_nm1[Nx,:,:] = u_nm1[Nx-1,:,:]
    u_nm1[0,:,:] = u_nm1[1,:,:]
    u_nm1[:,Ny,:] = u_nm1[:,Ny-1,:]
    u_nm1[:,0,:] = u_nm1[:,1,:]
    u_nm1[:,:,Nz] = u_nm1[:,:,Nz-1]
    
    u_n = u_nm1
    if n % 3600 == 0: #ingresa cada 3600 segundos para plotear el estado del hormigon
        print "temperatura A= ", u_n[Nx/2,Ny/2,Nz]
        print "temperatura M= ", u_n[Nx/2,Ny/2,Nz/2]
        print "temperatura S1= ", u_n[Nx/2,Ny/2,1]
        print "temperatura S= ", u_n[Nx/2,Ny/2,0]
        
        x.append(n/60) #Grafico en minutos
        y1.append(u_n[Nx/2,Ny/2,-1])
        y2.append(u_n[Nx/2,Ny/2,Nz/2])
        y3.append(u_n[Nx/2,Ny/2,1])
        y4.append(u_n[Nx/2,Ny/2,0])
        
        #Creo imagen
        imshowbien(u_n[Nx/2,:,:])
        title("Corte transversal\nk = {} t = {}".format(n, tiempo(n)))
        colorbar()
        savefig("movie/frame_{0:05.0f}.png".format(contador)) #guardo frame
        contador += 1
        close(1)
        
plt.plot(x,y1, label="Puntos 3, 6, 9")
plt.plot(x,y2, label="Puntos 2, 5, 8")
plt.plot(x,y3, label="Puntos 1, 4, 7")
plt.plot(x,y4, label="Punto en la superficie")

title("Temperatura",size=30)
xlabel("Tiempo en minutos")
ylabel("Temperatura Celsius")
ylim(20)
legend(loc="upper right")
savefig("movie/grafico.png")
show()
    