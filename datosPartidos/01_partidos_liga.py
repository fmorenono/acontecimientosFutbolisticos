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



def tratar_partidos(tr,part):
	num_jornadas=38
	jornada=38
	partido=0
	
	
	for _tr_ in _tr:
			texto=_tr_['id']+";"
			#print("....")
			texto=texto+str(jornada)+";"
			partido=partido+1
			if (partido==part):
				partido=0
				jornada=jornada-1
			_home=_tr_.find("div",{"class":"event__time"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			_home=_tr_.find("div",{"class":"event__scores fontBold"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			_home=_tr_.find("div",{"class":"event__participant event__participant--home"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			_home=_tr_.find("div",{"class":"event__participant event__participant--home fontBold"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			_home=_tr_.find("div",{"class":"event__participant event__participant--away"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			_home=_tr_.find("div",{"class":"event__participant event__participant--away fontBold"})
			if (_home)!=None:
				texto=texto+_home.text+";"
			guardando_a(archivo,texto+'\n')
		
#Programaprincipal
#Se procesan los datos de una temporada en un fichero formato web y se genera el csv de salida
now=time.localtime(time.time())
print('Comienza el programa'+time.strftime("%c",now))

time.sleep(1)

URL=sys.argv[1]
print(URL)
archivo=sys.argv[2]
print(archivo)

_driver=sys.argv[3]
print(_driver)

time.sleep(1)
print('--------------------------------------------------------')



try:
	
		driver = webdriver.Chrome(r"C:\FM\masterFM\chromedriver.exe")
		driver = webdriver.Chrome(_driver)
		
		driver.get(URL)
		soup = BeautifulSoup(driver.page_source, "html.parser")
		soup2=soup.encode('ascii', 'ignore').decode('ascii')

		
		_tr=soup.findAll("div",{"class":"event__match event__match--static event__match--oneLine "})
		
		tratar_partidos(_tr,9)
		
		#partido final
		
		_tr=soup.findAll("div",{"class":"event__match event__match--static event__match--oneLine event__match--last "})
		
		tratar_partidos(_tr,1)
			
		
		time.sleep(100000)

		driver.quit()

except Exception as e:
	print("error..."+str(e))
	
print("Acabado")

