#-*-coding:utf-8-*-_
import requests
import json
import urllib.request,unicodedata,time,_thread
from bs4 import BeautifulSoup
from datetime import datetime,date,timedelta
import sys
import re

class Cola:
    """ Representa a una cola, con operaciones de encolar y desencolar.
        El primero en ser encolado es también el primero en ser desencolado.
    """
	
    def encolar(self, x):
        """ Agrega el elemento x como último de la cola. """
        self.items.append(x)
	
    def __init__(self):
        """ Crea una cola vacía. """
        # La cola vacía se representa por una lista vacía
        self.items=[]

    def pintar_cola(self):
        for z in range(0,len(self.items)):
            print("Pintando "+str(z))
        return "1"

    def sumar_cola(self):
        suma=0
        for z in range(0,len(self.items)):            
            suma=suma+int(self.items[z])
            print("suma"+str(z))
        return suma
		
    def desencolar(self):
        """ Elimina el primer elemento de la cola y devuelve su
        	valor. Si la cola está vacía, levanta ValueError. """
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola está vacía")
			
    def es_vacia(self):
        """ Devuelve True si la cola esta vacía, False si no."""
        return self.items == []
		



def guardando_a(fich,valor):
	try:
		#print("guardando... "+fich)
		outfile=open(fich,'a',encoding='UTF-8')
		outfile.write(valor)
		outfile.close()

	except Exception as e:
		print("Excepcionguardando")
		print("erro..."+str(e))


def anadir_a_hash(valor,has,puntos,hasPuntos):
	if valor in hasPuntos:
		has[valor]=has[valor]+1
		hasPuntos[valor]=str(int(hasPuntos[valor])+int(puntos))	
	else:
		has[valor]=1
		hasPuntos[valor]=str(puntos)
		
	return has,hasPuntos

	
def anadir_a_hash_racha3(valor,has,puntos,hasPuntos):
	if valor in has:
		
		q2=hasPuntos[valor]
		if (has[valor])>=3:
			#q2.pintar_cola()
			ant=str(q2.sumar_cola())
			des=q2.desencolar()
			print("des "+des)
			q2.encolar(str(puntos))
			print("mas de 3,,, "+str(puntos)+" ANT "+ant+" DESP"+str(q2.sumar_cola()))
		if (has[valor])<3:
			#print("menos de 3 ")
			has[valor]=has[valor]+1
			q2.encolar(str(puntos))
		hasPuntos[valor]=q2
	else:
		print("anadiendo0")
		has[valor]=1
		q = Cola()
		q.encolar(str(puntos))
		hasPuntos[valor]=q
		
	return has,hasPuntos


def retornar_valor_hash_racha3(valor,has):
	ret="NA"
	suma=0
	#print("retornar_valor_hash_racha3")
	if valor in has:
		#print(has[valor])
		q=has[valor]
		suma=q.sumar_cola()
		ret=suma
	
	return ret	

	
def retornar_valor_hash(valor,has):
	ret="NA"
	if valor in has:
		ret=has[valor]
	
	return ret	

def porcentajePuntos(valor,valor2):
	ret="NA"
	if (valor!="NA" and valor2!="NA"):
		if (valor2>=3):
			ret=round(int(valor)/(int(valor2)*3),2)
	
	return ret	

def porcentaje(valor,valor2):
	ret="NA"
	if (valor!="NA" and valor2!="NA"):
		if (valor2>=3):
			ret=round(int(valor)/(int(valor2)*1),2)
	
	return ret	
	
#Se utilizan diferentes hash para ir guardando la diferente información

def guardando_estadisticas(fich,salida):

	home_part={}#Partidos en casa del local
	home_puntos={}#Puntos Partidos en casa del local
	away_part={}#Partidos fuera del visitante
	away_puntos={} #Puntos Partidos fuera del visitante
	total_part={}#Partidos
	total_puntos={}#Total Puntos
	
	#Rachas de los 3 ultimos partidos de las variables anteriores
	home_part_racha3={}
	home_puntos_racha3={}
	away_part_racha3={}
	away_puntos_racha3={}
	total_part_racha3={}
	total_puntos_racha3={}

	#home_part={}#Partidos en casa del local
	home_goles_propios={}#Goles Partidos en casa del local (propios)
	home_goles_ajenos={}#Goles Partidos en casa del local (ajenos)
	home_goles_totales={}#Goles Partidos en casa del local (total)
	#away_part={}#Partidos fuera del visitante
	away_goles_propios={} #Goles Partidos fuera del visitante
	away_goles_ajenos={} #Goles Partidos fuera del visitante
	away_goles_totales={} #Goles Partidos fuera del visitante
	#total_part={}#Partidos
	total_goles_propios={}#Total Puntos
	total_goles_ajenos={}#Total Puntos
	total_goles_totales={}#Total Puntos
	
	
	primera=True
	lin=""
	with open(fich) as f:
		for line in f:
			if(primera):
				lin=line.replace("\n","")+"porcen_home_puntos;porcen_away_puntos;porcen_total_puntos_1;porcen_total_puntos_2;"
				lin=lin+"porcen_home_puntos_racha3;porcen_away_puntos_racha3;porcen_total_puntos_1_racha3;porcen_total_puntos_2_racha3;"
				lin=lin+"porcen_home_goles_propios;porcen_home_goles_ajenos;porcen_home_goles_totales;porcen_away_goles_propios;porcen_away_goles_ajenos;porcen_away_goles_totales;"
				lin=lin+"porcen_goles_propios_1;porcen_goles_propios_2;porcen_goles_ajenos_1;porcen_goles_ajenos_2;porcen_goles_totales_1;porcen_goles_totales_2;\n"
				
				primera=False
				guardando_a(salida,lin)	
			else:

				bloques = line.split(";")
				local=bloques[3]
				visitante=bloques[4]
				goles_local=bloques[6]
				goles_visitante=bloques[7]
				resultado=bloques[8]
				puntos_local=0
				puntos_visitante=0
				if (resultado=="H"):
					puntos_local=3
				else:
					if (resultado=="A"):
						puntos_visitante=3
					else:
						puntos_local=1
						puntos_visitante=1
				
				
				#PArtidos hasta el actual
				home_part_1=retornar_valor_hash(local,home_part)
				home_puntos_1=retornar_valor_hash(local,home_puntos)
				porcen_home_puntos=porcentajePuntos(home_puntos_1,home_part_1)
				
				
				away_part_2=retornar_valor_hash(visitante,away_part)
				away_puntos_2=retornar_valor_hash(visitante,away_puntos)
				porcen_away_puntos= porcentajePuntos(away_puntos_2,away_part_2)
				
				
				total_part_1=retornar_valor_hash(local,total_part)
				total_puntos_1=retornar_valor_hash(local,total_puntos)
				porcen_total_puntos_1= porcentajePuntos(total_puntos_1,total_part_1)
				
				total_part_2=retornar_valor_hash(visitante,total_part)
				total_puntos_2=retornar_valor_hash(visitante,total_puntos)
				porcen_total_puntos_2= porcentajePuntos(total_puntos_2,total_part_2)
				
				
				home_part_1_racha3=retornar_valor_hash(local,home_part_racha3)
				home_puntos_1_racha3=retornar_valor_hash_racha3(local,home_puntos_racha3)
				porcen_home_puntos_racha3=porcentajePuntos(home_puntos_1_racha3,home_part_1_racha3)
				#print("XXX "+str(porcen_home_puntos_racha3))
				
				away_part_2_racha3=retornar_valor_hash(visitante,away_part_racha3)
				away_puntos_2_racha3=retornar_valor_hash_racha3(visitante,away_puntos_racha3)
				porcen_away_puntos_racha3= porcentajePuntos(away_puntos_2_racha3,away_part_2_racha3)
				
				
				total_part_1_racha3=retornar_valor_hash(local,total_part_racha3)
				total_puntos_1_racha3=retornar_valor_hash_racha3(local,total_puntos_racha3)
				porcen_total_puntos_1_racha3= porcentajePuntos(total_puntos_1_racha3,total_part_1_racha3)
				
				total_part_2_racha3=retornar_valor_hash(visitante,total_part_racha3)
				total_puntos_2_racha3=retornar_valor_hash_racha3(visitante,total_puntos_racha3)
				porcen_total_puntos_2_racha3= porcentajePuntos(total_puntos_2_racha3,total_part_2_racha3)
				
				
				#Goles home
				home_part_1=retornar_valor_hash(local,home_part)
				home_goles_propios_1=retornar_valor_hash(local,home_goles_propios)
				porcen_home_goles_propios=porcentaje(home_goles_propios_1,home_part_1)
				home_goles_ajenos_1=retornar_valor_hash(local,home_goles_ajenos)
				porcen_home_goles_ajenos=porcentaje(home_goles_ajenos_1,home_part_1)
				home_goles_totales_1=retornar_valor_hash(local,home_goles_totales)
				porcen_home_goles_totales=porcentaje(home_goles_totales_1,home_part_1)

				#Goles away
				away_part_1=retornar_valor_hash(visitante,away_part)
				away_goles_propios_1=retornar_valor_hash(visitante,away_goles_propios)
				porcen_away_goles_propios=porcentaje(away_goles_propios_1,away_part_1)
				away_goles_ajenos_1=retornar_valor_hash(visitante,away_goles_ajenos)
				porcen_away_goles_ajenos=porcentaje(away_goles_ajenos_1,away_part_1)
				away_goles_totales_1=retornar_valor_hash(visitante,away_goles_totales)
				porcen_away_goles_totales=porcentaje(away_goles_totales_1,away_part_1)
				
				#Goles total
				total_part_1=retornar_valor_hash(local,total_part)
				total_goles_propios_1=retornar_valor_hash(local,total_goles_propios)
				porcen_goles_propios_1=porcentaje(total_goles_propios_1,total_part_1)
				total_part_2=retornar_valor_hash(visitante,total_part)
				total_goles_propios_2=retornar_valor_hash(visitante,total_goles_propios)
				porcen_goles_propios_2=porcentaje(total_goles_propios_2,total_part_2)				
				
				total_part_1=retornar_valor_hash(local,total_part)
				total_goles_ajenos_1=retornar_valor_hash(local,total_goles_ajenos)
				porcen_goles_ajenos_1=porcentaje(total_goles_ajenos_1,total_part_1)
				total_part_2=retornar_valor_hash(visitante,total_part)
				total_goles_ajenos_2=retornar_valor_hash(visitante,total_goles_ajenos)
				porcen_goles_ajenos_2=porcentaje(total_goles_ajenos_2,total_part_2)				
				
				total_part_1=retornar_valor_hash(local,total_part)
				total_goles_totales_1=retornar_valor_hash(local,total_goles_totales)
				porcen_goles_totales_1=porcentaje(total_goles_totales_1,total_part_1)
				total_part_2=retornar_valor_hash(visitante,total_part)
				total_goles_totales_2=retornar_valor_hash(visitante,total_goles_totales)
				porcen_goles_totales_2=porcentaje(total_goles_totales_2,total_part_2)		
				

				
				#Partidos en casa del local
				home_part,home_puntos=anadir_a_hash(local,home_part,puntos_local,home_puntos)
				home_part_racha3,home_puntos_racha3=anadir_a_hash_racha3(local,home_part_racha3,puntos_local,home_puntos_racha3)
				#Partidos fuera del visitante
				away_part,away_puntos=anadir_a_hash(visitante,away_part,puntos_visitante,away_puntos)
				away_part_racha3,away_puntos_racha3=anadir_a_hash_racha3(visitante,away_part_racha3,puntos_visitante,away_puntos_racha3)

				#Partidos total del local y del visitante
				total_part,total_puntos=anadir_a_hash(visitante,total_part,puntos_visitante,total_puntos)
				total_part,total_puntos=anadir_a_hash(local,total_part,puntos_local,total_puntos)
				
				total_part_racha3,total_puntos_racha3=anadir_a_hash_racha3(visitante,total_part_racha3,puntos_visitante,total_puntos_racha3)
				total_part_racha3,total_puntos_racha3=anadir_a_hash_racha3(local,total_part_racha3,puntos_local,total_puntos_racha3)
				
								
				#Goles
				_sin_uso=home_part.copy()
				_sin_uso,home_goles_propios=anadir_a_hash(local,_sin_uso,goles_local,home_goles_propios)
				_sin_uso,home_goles_ajenos=anadir_a_hash(local,_sin_uso,goles_visitante,home_goles_ajenos)
				_sin_uso,home_goles_totales=anadir_a_hash(local,_sin_uso,int(goles_local)+int(goles_visitante),home_goles_totales)
				
				_sin_uso=away_part.copy()
				_sin_uso,away_goles_propios=anadir_a_hash(visitante,_sin_uso,goles_visitante,away_goles_propios)
				_sin_uso,away_goles_ajenos=anadir_a_hash(visitante,_sin_uso,goles_local,away_goles_ajenos)
				_sin_uso,away_goles_totales=anadir_a_hash(visitante,_sin_uso,int(goles_local)+int(goles_visitante),away_goles_totales)
				
				_sin_uso=total_part.copy()
				_sin_uso,total_goles_propios=anadir_a_hash(local,_sin_uso,goles_local,total_goles_propios)
				_sin_uso,total_goles_propios=anadir_a_hash(visitante,_sin_uso,goles_visitante,total_goles_propios)
				
				#_sin_uso=total_part.copy()
				_sin_uso,total_goles_ajenos=anadir_a_hash(local,_sin_uso,goles_local,total_goles_ajenos)
				_sin_uso,total_goles_ajenos=anadir_a_hash(visitante,_sin_uso,goles_visitante,total_goles_ajenos)
				
				_sin_uso,total_goles_totales=anadir_a_hash(local,_sin_uso,int(goles_local)+int(goles_visitante),total_goles_totales)
				_sin_uso,total_goles_totales=anadir_a_hash(visitante,_sin_uso,int(goles_local)+int(goles_visitante),total_goles_totales)
				
				



					
				#print(home_part_1)
				_linea=str(porcen_home_puntos)+";"+str(porcen_away_puntos)+";"+str(porcen_total_puntos_1)+";"+str(porcen_total_puntos_2)+";"
				_linea2=_linea+str(porcen_home_puntos_racha3)+";"+str(porcen_away_puntos_racha3)+";"+str(porcen_total_puntos_1_racha3)+";"+str(porcen_total_puntos_2_racha3)+";"

				
			
				_linea2=_linea2+str(porcen_home_goles_propios)+";"+str(porcen_home_goles_ajenos)+";"+str(porcen_home_goles_totales)+";"+str(porcen_away_goles_propios)+";"+str(porcen_away_goles_ajenos)+";"+str(porcen_away_goles_totales)+";"
				_linea2=_linea2+str(porcen_goles_propios_1)+";"+str(porcen_goles_propios_2)+";"+str(porcen_goles_ajenos_1)+";"+str(porcen_goles_ajenos_2)+";"+str(porcen_goles_totales_1)+";"+str(porcen_goles_totales_2)+";"
			
				
				
				
				#_linea=_linea+_linea2
				print(_linea2)
				guardando_a(salida,line.replace("\n","")+_linea2+"\n")	
	

		
#revertir_fichero
def revertir_fichero(fich,salida):


	d = []
	primera=True
	lin=""
	with open(fich) as f:
		for line in f:
			if(primera):
				lin=line
				primera=False
			else:
				print(1)
				bloques = line.split(";")
				aux=bloques[5]
				#print("ZZZZ"+aux)
				#bloques[5]=aux[8:10]+aux[3:5]+aux[0:2] 14/05/2017
				bloques[5]=aux[6:8]+aux[3:5]+aux[0:2] #14/05/17
				d.append(bloques)
				#print("ZZZZ2 "+bloques[5])
				
	#print ("ordenar por: ")
	ordenados=sorted(d,key=lambda x:x[5])
	
	guardando_a(salida,lin)
	print (ordenados)
	for x in ordenados:
		linea=""
		i=0
		while (i<21):
			linea=linea+x[i].replace("\n","")+";"
			i=i+1
			
		guardando_a(salida,linea+"\n")

#calculo de nuevas variables
#Programaprincipal
now=time.localtime(time.time())
print('Comienza elprograma'+time.strftime("%c",now))
time.sleep(1)
fichero=sys.argv[1]
#fichero="2018_2019_spain.csv"
print(fichero)
ficheroSalida=sys.argv[2]
print(ficheroSalida)
opciones=sys.argv[3]
print(opciones)

time.sleep(1)



#Inverso
if (opciones=="1"):
	revertir_fichero(fichero,ficheroSalida)

if (opciones=="2"):
	guardando_estadisticas(fichero,ficheroSalida)
	
print("Acabado")
