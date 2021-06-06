from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import urllib.request,unicodedata,time,_thread
from bs4 import BeautifulSoup
from datetime import datetime,date,timedelta
import sys
		
	
def leyendo(fich):
	try:
		infile=open(fich,'r')
		s=infile.readline()
		infile.close()
		return '0'
	except:
		print("noexiste")
		return'-1'



def guardando_a(fich,valor):
	try:
		print("guardando... "+fich)
		outfile=open(fich,'a')#Indicamoselvalor'w'.
		outfile.write(valor)
		outfile.close()

	except:
		print("Excepcion guardando")


#Programaprincipal
#Merge entre los datos estadístiicos de los partidos. Se hace uso del fichero que relaciona los nombres de los equipos de un y otro csv inicial
now=time.localtime(time.time())
print('Comienza elprograma'+time.strftime("%c",now))
time.sleep(1)
fichero=sys.argv[1]
fichero2=sys.argv[2]
#fichero="2018_2019_spain.txt"
print(fichero)
equipos=sys.argv[3]
print(equipos)
ficheroSalida=sys.argv[4]
print(ficheroSalida)

time.sleep(1)
print('--------------------------------------------------------')

#fichero de equipos  ampliado
d = {}
f1 = {}
f2 = {}
fCabeceras=""

with open(equipos,"r", encoding="utf-8") as f:
	for line in f:
		#print(line)
		bloques = line.split(";")
		d[bloques[0]] = bloques[1]
		
print (d)


with open(fichero2,"r", encoding="utf-8") as f:
	primero=True
	for line in f:
		#print(line)
		if (primero):
			fCabeceras=line
			primero=False
		else:
			bloques = line.split(",")
			partido=str(bloques[2])+str(bloques[3])
			f1[partido] = line
			
print (f1)

etiquetas=["Date","FTHG","FTAG","FTR","HS","AS","HC","AC","B365H","B365D","B365A","BWH","BWD","BWA","BbAv>2.5","BbAv<2.5"]
linea_etiquetas="ID;jornada;horario;local;visitante;Date;FTHG;FTAG;FTR;HS;AS;HC;AC;B365H;B365D;B365A;BWH;BWD;BWA;BbAv>2.5;BbAv<2.5;\n"

def buscar_partido(partido,_f1,_fCabeceras):
	print("buscar;"+ partido)
	
	lin=_f1[partido].rstrip('\n')
	lin2=_fCabeceras.rstrip('\n')
	bloques = lin.split(",")
	bloques2 = lin2.split(",")
	i=0
	l=""
	#for elem,elem2 in bloques,bloques2:
	
	for x in range(0,len(bloques)):
		elem=bloques[x]
		elem2=bloques2[x]
	
		if (i!=0) and (i!=2) and (i!=3):
			if(elem2 in etiquetas):
				l=l+str(elem)+";"
				#print(elem)
		i=i+1
	return l+'\n'

with open(fichero,"r", encoding="utf-8") as f:
	guardando_a(ficheroSalida,linea_etiquetas)	
	for line in f:
		#print(line)
		bloques = line.split(";")
		
		partido=str(d[bloques[4]])+str(d[bloques[5]])
		linea2=buscar_partido(partido,f1,fCabeceras)	
		bloques=bloques[0]+";"+bloques[1]+";"+bloques[2]+";"+bloques[4]+";"+bloques[5]+";"+str(linea2)
		
		#bloques=bloques.replace(',',';')
		guardando_a(ficheroSalida,bloques)	
#print (f1)


try:
	
		
		num_jornadas=38
		total_partidos=380
		partido=0
		while (partido<380):
		
		
			partido=partido+1
		
		
except Exception as e:
	print("error..."+str(e))
	
print("Acabado")

