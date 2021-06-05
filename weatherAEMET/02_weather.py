#-*-coding:utf-8-*-_
import requests
import json
import urllib.request,unicodedata,time,_thread
from bs4 import BeautifulSoup
from datetime import datetime,date,timedelta
import sys
import re


def datos_diarios(estacion,fec_ini,fec_fin,id_partido,equipo,ficheroSalida,aproximado,segundo):
	lin=""
	url=""
	try:
		url="https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2021-02-27T00:00:00UTC/fechafin/2021-02-28T23:59:59UTC/estacion/8178D"
		url="https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/"+fec_ini+"T00:00:00UTC/fechafin/"+fec_fin+"T23:59:59UTC/estacion/"+estacion
		print(url)
		querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmbW9yZW5vbm9AaG90bWFpbC5jb20iLCJqdGkiOiI4MmRlZTNhMy0wMWI0LTQxYjQtOTA3NC0zMmM3ZDk3MDY4NWEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxNjI2MzA0NiwidXNlcklkIjoiODJkZWUzYTMtMDFiNC00MWI0LTkwNzQtMzJjN2Q5NzA2ODVhIiwicm9sZSI6IiJ9.4PtMghNAKzb0iNfxKlA2fDQqKKeCrF9rBOaVMQS9oPY"}
		#querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtZWd1c3Rhc2Fsb3VAaG90bWFpbC5jb20iLCJqdGkiOiJlY2ViNzNhYS1jMzgyLTRlNDgtYWU2YS02MjU5NTk1ZjJiZjUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYyMDg5OTg1NywidXNlcklkIjoiZWNlYjczYWEtYzM4Mi00ZTQ4LWFlNmEtNjI1OTU5NWYyYmY1Iiwicm9sZSI6IiJ9.SOWWh3Xhtl5eGFTSRa1kafbS1kdaqe1AqnOSx1eYfj4"}

		
		headers = {
			'cache-control': "no-cache"
			}

		response = requests.request("GET", url, headers=headers, params=querystring)

		linea=""
		resultado=""
		for letra in response.text:
				linea=linea+str(letra)
				#print(str(letra))
				if str(letra)=='\n':
					if (linea.find('"datos"'))>0:
						resultado=linea[13:-3]
					#print (linea)
					linea=""

		print("resultado: "+resultado)
		response2 = requests.request("GET", resultado, headers=headers, params=querystring)
		
		for my_dict in json.loads(response2.text):
		#my_dict = json.loads(response2.text)[0]
			#print(my_dict)
			#my_dict = json.loads(response2.text)[1]
			print(my_dict)
			

			_fecha=my_dict['fecha']
			_nombre=my_dict['nombre']
			_provincia=my_dict['provincia']
			_tmax='NaN'
			if 'tmax' in my_dict:
				_tmax=my_dict['tmax'].replace(',','.')
			_tmin='NaN'
			if 'tmin' in my_dict:
				_tmin=my_dict['tmin'].replace(',','.')
			_sol='NaN'
			if 'sol' in my_dict:
				_sol=my_dict['sol'].replace(',','.')
			_presMax='NaN'
			if 'presMax' in my_dict:
				_presMax=my_dict['presMax'].replace(',','.')
			_presMin='NaN'
			if 'presMin' in my_dict:
				_presMin=my_dict['presMin'].replace(',','.')
			_prec='NaN'
			if 'prec' in my_dict:
				_prec=my_dict['prec'].replace(',','.')
			_racha='NaN'
			if 'racha' in my_dict:
				_racha=my_dict['racha'].replace(',','.')
			_dir='NaN'
			if 'dir' in my_dict:
				_dir=my_dict['dir'].replace(',','.')
			_velmedia='NaN'
			if 'velmedia' in my_dict:
				_velmedia=my_dict['velmedia'].replace(',','.')
			lin=_fecha+";"+_nombre+";"+_provincia+";"+_tmax+";"+_tmin+";"+_sol+";"+_presMax+";"+_presMin+";"+_prec+";"+_racha+";"+_dir+";"+_velmedia+";"
			lin2=_tmax+";"+_tmin+";"+_sol+";"+_presMax+";"+_presMin+";"+_prec+";"+_racha+";"+_dir+";"+_velmedia+";"
			print(lin)
			if (lin!=""):
				if (not segundo):
					guardando_a(ficheroSalida,id_partido+";"+equipo+";"+aproximado+";"+lin)
				else:
					guardando_a(ficheroSalida,lin2+"\n")
	
	except Exception as e:
		print("Excepcionguardando")
		print("erro..."+str(e))
		guardando_a("trazas.err",url)
	return lin

def guardando_a(fich,valor):
	try:
		print("guardando... "+fich)
		outfile=open(fich,'a')
		outfile.write(valor)
		outfile.close()

	except Exception as e:
		print("Excepcionguardando")
		print("erro..."+str(e))


#Programaprincipal
now=time.localtime(time.time())
print('Comienza elprograma'+time.strftime("%c",now))
time.sleep(1)
fichero=sys.argv[1]
#fichero="2018_2019_spain.txt"
print(fichero)
equipos=sys.argv[2]
print(equipos)
ficheroSalida=sys.argv[3]
print(ficheroSalida)
any_inicio_entrada=sys.argv[4]
print(any_inicio_entrada)
any_fin_entrada=sys.argv[5]
print(any_fin_entrada)

time.sleep(1)

#fichero de equipos
d = {}
dd = {}
with open(equipos,"r", encoding="utf-8") as f:
	for line in f:
		print(line)
		bloques = line.split(";")
		d[bloques[0]] = bloques[1]
		dd[bloques[0]] = bloques[2]

print (d)



seg=1
for line in list(open(fichero)):
	#print(line)
	bloques=line.split(sep=';')
	id_partido=bloques[0]
	bloc_hora=bloques[2]
	print (bloc_hora)
	ini=bloc_hora.split(sep=' ')
	fecha=ini[0]
	_dia=fecha[0:2]
	_mes=fecha[3:5]
	print(_dia+" "+_mes)
	equipo1=bloques[3]
	#print (equipo1)
	equipo2=bloques[4]
	#print (equipo2)
	
	equipo1_trans=''
	equipo1_exact=''
	#try:
	equipo1_trans=d[equipo1]
	equipo1_exact=dd[equipo1]
	#except Exception as e:	
	#	e=e
	
	equipo2_trans=''
	equipo2_exact=''
	#try:
	equipo2_trans=d[equipo2]
		#equipo2_trans=d[equipo2]
		#print (equipo1_exact)
	equipo2_exact=dd[equipo2]
		#print (equipo1_exact
	#except Exception as e:	
	#	e=e



	
	any=any_inicio_entrada
	if (int(_mes)<8):
		any=any_fin_entrada
	
	

	_fecha=str(any)+'-'+str(_mes)+'-'+str(_dia)
	_fecha_fin=str(any)+'-'+str(_mes)+'-'+str(_dia)
	print(equipo1_trans+" "+_fecha)
	#if (equipo1=='Villarreal') or (equipo2=='Villarreal'):
	lin=datos_diarios(equipo1_trans,_fecha,_fecha_fin,id_partido,equipo1,ficheroSalida,equipo1_exact,False)
	lin=datos_diarios(equipo2_trans,_fecha,_fecha_fin,id_partido,equipo2,ficheroSalida,equipo2_exact,True)

		
print("Acabado")
