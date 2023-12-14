from typing import List
import requests
from bs4 import BeautifulSoup

__baseurl = "http://crono.rallyrcmadrid.com/rally.php?idrally="

__defaultDriver = "Miranda"

def getRallyData(driver:str,RallyID:int) -> str:
    return __formatData(__auxGetRallyData(driver,RallyID))    
    pass

def __formatData(data: list) -> str: 

    if "resultados" in str(data) or "error" in str(data) :
        return str(data[0])
        
    formatedData = "-----------------\n"

    for tablapiloto in data:

        if len(tablapiloto) >1:

            tramos = len(tablapiloto) - 9

            formatedData +=str("Dorsal :" + str(tablapiloto[1]) + "\n" + 
                                "Piloto :" + str(tablapiloto[2])+"\n") 

            for i in range(tramos):
                tramo = ("Tramo " + str(i+1) + " : <b>" + str(tablapiloto[i+5] + "</b> \n"))
                formatedData+=tramo
            
            formatedData += "------------------\n"

            pass
                            
    return str(formatedData)

    pass


def __auxGetRallyData(driver:str,RallyID:int) -> list:
    
    DataUrl = __baseurl + str(RallyID)

    if driver == None or driver == '':
        DriverNick = str(__defaultDriver)
    else:
        DriverNick = driver
            
    data = []

    # Ejecutar GET-Request
    response = requests.get(DataUrl)

    if "200" in str(response):
        #print(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            div = soup.find("div",id="WRC")
            tabla = div.find("tbody")
            filas = tabla.find_all("tr")
        except:
            filas = []
        try:
            div2 = soup.find("div",id="WRC2")
            tabla2 = div2.find("tbody")
            filas2 = tabla2.find_all("tr")
        except:
            filas2 = []

        registros = filas + filas2

        for f in registros:
            datarow=[]
            cols = f.find_all('td')
            if DriverNick in str(cols[2]):
                for c in cols:
                    datarow.append(c.text)
                data.append(datarow)
    if len(data) < 1:
        data.append("no se obtuvieron resultados")
    return data
    pass

def getRallyDrivers(RallyID:int):

    drivers = []
    driversm = []
    rallyTittle = ""

    DataUrl = __baseurl + str(RallyID)
   
    # Ejecutar GET-Request
    response = requests.get(DataUrl)

    if "200" in str(response):
        #print(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            h1 = soup.find("h1")
            rallyTittle = str(h1.text)
        except:
            rallyTittle = "No Rally Tittle Found"

        try:
            div = soup.find("div",id="WRC")
            tabla = div.find("tbody")
            filas = tabla.find_all("tr")
            for r in filas:
                cols = r.find_all('td')
                drivers.append(cols[2].text)
        except:
            drivers = []
            
        try:
            div2 = soup.find("div",id="WRC2")
            tabla2 = div2.find("tbody")
            filas2 = tabla2.find_all("tr")
            for r in filas2:
                cols = r.find_all('td')
                driversm.append(cols[2].text)
        except:
            driversm = []

    return drivers,driversm,rallyTittle
    pass

def getRallyTittle(RallyID:int):

    rallyTittle = ""

    DataUrl = __baseurl + str(RallyID)
   
    # Ejecutar GET-Request
    response = requests.get(DataUrl)

    if "200" in str(response):
        #print(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            h1 = soup.find("h1")
            rallyTittle = str(h1.text)
        except:
            rallyTittle = "No Rally Tittle Found"

    return rallyTittle
    pass