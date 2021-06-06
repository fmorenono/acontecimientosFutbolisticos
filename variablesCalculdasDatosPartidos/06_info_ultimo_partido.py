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


def anadir_a_hash(valor,has,resultado):
		has[valor]=resultado
		return has

def retornar_valor_hash(valor,has):
	ret="0;0;0;1;0;0;0;0;0;1"
	ret2=""
	if valor in has:
		ret=has[valor]
		bloques = ret.split("-")
		loc=bloques[0]
		vis=bloques[1]
		if (int(loc)==int(vis)):
			ret2="0;1;0;0"
		else:
			if (int(loc)>int(vis)):
				ret2="1;0;0;0"
			else:
				ret2="0;0;1;0"
		#ret=ret2+";"+str(int(loc)-int(vis))		
		dif=int(loc)-int(vis)
		if (dif==0):
			ret3="1;0;0;0;0;0"
		else:
			if (dif>1):
				ret3="0;1;1;0;0;0"
			else:
				if (dif>0):
					ret3="0;0;1;0;0;0"
				else:
					if (dif<-1):
						ret3="0;0;0;1;1;0"
					else:
						ret3="0;0;0;0;1;0"	
		ret=ret2+";"+ret3
		
	else:
		print("OJO: "+valor)
	return ret		
		
#revertir_fichero
def ultimo_partido(fich,fich_ant,salida):
	ultimo_resultado={}
	with open(fich_ant) as f:
		for line in f:
			#print(line)
			bloques = line.split(";")
			resultado=bloques[3]
			local=bloques[4]
			visitante=bloques[5]
			partido=local+visitante
			ultimo_resultado=anadir_a_hash(partido,ultimo_resultado,resultado)
	
	primera=True
	with open(fich) as f2:
		for line in f2:
			if(primera):
				lin="ID;jornada;horario;local;visitante;Date;FTHG;FTAG;FTR;HS;AS;HC;AC;B365H;B365D;B365A;BWH;BWD;BWA;BbAv>2.5;BbAv<2.5;porcen_home_puntos;porcen_away_puntos;porcen_total_puntos_1;porcen_total_puntos_2;porcen_home_puntos_racha3;porcen_away_puntos_racha3;porcen_total_puntos_1_racha3;porcen_total_puntos_2_racha3;porcen_home_goles_propios;porcen_home_goles_ajenos;porcen_home_goles_totales;porcen_away_goles_propios;porcen_away_goles_ajenos;porcen_away_goles_totales;porcen_goles_propios_1;porcen_goles_propios_2;porcen_goles_ajenos_1;porcen_goles_ajenos_2;porcen_goles_totales_1;porcen_goles_totales_2;ult_result_1;ult_result_2;ult_result_3;ult_result_4;ult_result_dif_goles_1;ult_result_dif_goles_2;ult_result_dif_goles_3;ult_result_dif_goles_4;ult_result_dif_goles_5;"
				lin=lin.replace("\n","")

				#guardando_a(salida,lin+"\n")
				primera=False
			else:			
				#print(line)
				bloques = line.split(";")
				local=bloques[3]
				visitante=bloques[4]
				partido=local+visitante
				dev=retornar_valor_hash(partido,ultimo_resultado)
				lin=line.replace("\n","")+""+dev
			guardando_a(salida,lin+"\n")
			
			
	
#Programaprincipal
now=time.localtime(time.time())
print('Comienza elprograma'+time.strftime("%c",now))
time.sleep(1)
fichero=sys.argv[1]
#fichero="2018_2019_spain.csv"
print(fichero)
fichero2=sys.argv[2]
#fichero="2018_2019_spain.csv"
print(fichero2)
ficheroSalida=sys.argv[3]
print(ficheroSalida)
print(".....")
opciones=sys.argv[4]
print(".....")
print(opciones)

time.sleep(1)



#Inverso
if (opciones=="1"):
	ultimo_partido(fichero,fichero2,ficheroSalida)


	
print("Acabado")
