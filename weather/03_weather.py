
#-*-coding:utf-8-*-_
import urllib.request,unicodedata,time,_thread
from bs4 import BeautifulSoup
from datetime import datetime,date,timedelta
import sys
import re

					
	
def conectando(web):
	try:
		print('>>>set..')
		ur=urllib.request.urlopen(web,timeout=3)
		print('>>>set2..')
		return ur 
		#conector1=urllib.request.urlopen(url1,timeout=30)#timeoutde10segundos
	except:
		print('>>>Exceptcion en la conexión')
		time.sleep(1)
		return conectando(web)

def conectandoRead(url,cone):
	try:
		print('>>>set')
		html=cone.read()
		print('>>>set2')
		return html
		#conector1=urllib.request.urlopen(url1,timeout=30)#timeoutde10segundos
	except:
		print('>>>Exceptcion2')
		print(url)
		time.sleep(1)
		t=conectando(url)
		return conectandoRead(url,t)


def guardando_a(fich,valor):
	try:
		print("guardando... "+fich)
		outfile=open(fich,'a',encoding='UTF-8')#Indicamoselvalor'w'.
		outfile.write(valor)
		outfile.close()

	except Exception as e:
		print("Excepcionguardando")
		print("erro..."+str(e))



	
def buscar(palabra,texto):
	mensaje5a = texto.find(palabra)
	subtexto="NA"
	if (mensaje5a>-1):
		mensaje5a=mensaje5a+len(palabra)+1
		subtexto=texto[mensaje5a:]		
		mensaje5b = subtexto.find(",")
		subtexto=subtexto[:mensaje5b]
	return subtexto

	
def buscar_datos_tiempo(palabra):
	linea=""
	completa=""
	temp=""
	for letra in palabra:
		linea=linea+letra
		if letra=='\n':
			if (linea.find("Contents are strictly for use by timeandda"))>0:
				lista=re.findall(r'{(.*?)}',linea)
				for i in lista:
					if 'lunes' in i or 'martes' in i or 'miércoles' in i or 'jueves' in i or 'viernes' in i or 'sábado' in i or 'domingo' in i:
						i=i.replace(', ','; ')
						i=limpieza_dias_semana(i)
						ii=buscar('"ds"',i)
						temp=str(ii)
						ii=buscar('"icon"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"desc"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"temp"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"baro"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"wind"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"wd"',i)
						temp=temp+";"+str(ii)
						ii=buscar('"hum"',i)
						temp=temp+";"+str(ii)
						completa=completa+temp+";"+'\n'
			linea=""
			#temp=""
	print(completa)
	return completa

#depracated
def datos_mensuales(pais_ciudad,mes,any,ficher):

	url11='https://www.timeanddate.com/weather/'+pais_ciudad+'/historic?month='+mes+'&year='+any
	mes=1
	print('--------------------------------------------------------')

	try:
	
			print(url11)
			print('--------------------------------------------------------')
		
			conector1=conectando(url11)
			#html=conector1.read()
			html=conectandoRead(url11,conector1)
			soup=BeautifulSoup(html)
			te=soup.text
			#print(type(soup.text))
			mensaje5a = te.find("Contents are strictly for use by timeandda")
			#print("ahi:"+str(mensaje5a))
			datos=buscar_datos_tiempo(te)	
			guardando_a(ficher,datos)
			#print(soup.text)
			guardando_a('correctos1.txt',url11+'\n')
			
		
			mes=mes+1

	except Exception as e:
			print("erro..."+str(e))
			guardando_a('errores1.txt',url11+'\n')

def datos_diarios(id_partido,ciudad,pais_ciudad,exact,mes,any,dia,ficher):

	url11='https://www.timeanddate.com/weather/'+pais_ciudad+'/historic?month='+mes+'&year='+any+'&hd='+dia
	print(url11)
	print('--------------------------------------------------------')
	datos=0
	try:
	
			print(url11)
			print('--------------------------------------------------------')
		
			conector1=conectando(url11)
			html=conectandoRead(url11,conector1)
			soup=BeautifulSoup(html)
			_tr=soup.findAll("tbody")
			
			saltar=True
			hora=""
			for _tr_ in _tr:
				if not saltar:
					texto=_tr_.text
					_tr22=_tr_.findAll("tr")
					
					for _tr22_ in _tr22:
						
						
						_tr11=_tr22_.findAll("th")
						for _tr11_ in _tr11:
							hora=_tr11_.text
							if (len(hora)>6):
								hora='0:00'
						
						
						_tr2=_tr22_.findAll("td")
						pos=1
						linea=""
						for _tr2_ in _tr2:
							texto=_tr2_.text
							#print('ahi va')
							if (pos>1 and pos!=5):
								linea=linea+texto+";"
							pos=pos+1
						linea=id_partido+";"+ciudad+";"+pais_ciudad+";"+exact+";"+dia+";"+hora+";"+linea+"\n"
						print(linea)
						datos=datos+1
						guardando_a(ficher,linea)
						#guardando_a('weather2.csv',linea)
						#time.sleep(10)
				saltar=False
			guardando_a('correctos1.txt',url11+'\n')
			return datos
		
	
	except Exception as e:
			print("erro..."+str(e))
			guardando_a('errores1.txt',url11+'\n')			
	
def limpieza_dias_semana(texto):
	texto=texto.replace("lunes, ","").replace("martes, ","").replace("miercoles, ","").replace("jueves, ","")
	texto=texto.replace("viernes, ","").replace("sabado, ","").replace("domingo, ","")
	return texto
			
#Programaprincipal
#Se extraen los datos metereologicos de la población del equipo local y visitante para cada partido (hora del partido)
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


time.sleep(1)

#fichero de equipos
d = {}
dd = {}
with open(equipos) as f:
	for line in f:
		bloques = line.split(";")
		d[bloques[0]] = bloques[1]
		dd[bloques[0]] = bloques[2]

print (d)




seg=1
for line in list(open(fichero)):
	bloques=line.split(sep=';')
	id_partido=bloques[0]
	bloc_hora=bloques[2]
	equipo1=bloques[4]
	print (equipo1)
	equipo2=bloques[5]
	print (equipo2)
	equipo1_trans=d[equipo1]
	equipo2_trans=d[equipo2]

	
	#equipo2_trans=d[equipo2]
	equipo1_exact=dd[equipo1]
	print (equipo1_exact)
	equipo2_exact=dd[equipo2]
	print (equipo1_exact)


	print(equipo1_trans)
	#time.sleep(9000)
	bloques2=bloc_hora.split(sep=' ')
	dia_mes=bloques2[0]
	
	bloques3=bloc_hora.split(sep='.')
	dia=bloques3[0]
	mes=bloques3[1]
	anio=2019
	
	mes2=mes
	mes=str(int(mes))
	if (int(mes)>7):
		anio=2018
	fecha=str(anio)+str(mes2)+str(dia)
	print(dia)
	print(mes)
	print(str(anio))
	
	j=0
	while (j<9):
		fecha=str(anio-j)+str(mes2)+str(dia)
		datos=datos_diarios(id_partido,equipo1,equipo1_trans,equipo1_exact,mes,str(anio-j),fecha,ficheroSalida)	
		guardando_a('trazas1.txt',id_partido+" "+str(anio-j)+" "+equipo1+" datos: "+str(datos)+'\n')
		datos_diarios(id_partido,equipo2,equipo2_trans,equipo2_exact,mes,str(anio-j),fecha,ficheroSalida)	
		guardando_a('trazas1.txt',id_partido+" "+str(anio-j)+" "+equipo2+" datos: "+str(datos)+'\n')
	
		j=j+1
		#datos_diarios('madrid','spain/madrid','3','2012','20120310')	
		time.sleep(seg)
		seg=seg+1
		if (seg==4):
			seg=1
		time.sleep(3)
		
print("Acabado")
