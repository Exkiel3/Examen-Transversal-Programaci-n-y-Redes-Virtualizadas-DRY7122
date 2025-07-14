import requests
import urllib.parse
import os

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
#loc1 = "Santiago"
#loc2 = "Buenos Aires"
#loc1 = "Washington, D.C."
#loc2 = "Baltimore, Maryland"

key = "4a4b6066-9eb0-4b53-9b2d-58ca88dc8bd9" # Reemplazar con su clave de API de Graphhopper

def geocoding (location, key):
    while location == "":
        location = input("ingrese nuevamente la ubicacion: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    #print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat=(json_data["hits"][0]["point"]["lat"])
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)


    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
            input()

        
    return json_status,lat,lng,new_loc


while True:
    os.system("clear")
    print("\n-------------------------------------------")
    print("Tipos de vahiculos disponibles en Graphhopper:")
    print("----------------------------------------------")
    print("automovil, bicicleta, a pie")
    print("----------------------------------------------")
    profile = {"automovil": "car", "bicicleta": "bike", "a pie": "foot"}
    vehicle = input("seleccione un vehiculo de la lista o presione s para salir : ")
    if vehicle == "s" or vehicle == "s":
        break
    elif vehicle in profile:
        vehicle = profile[vehicle]
    else: 
        vehicle = "car"
        print("No se ingresó un medio de transporte válido. Usando la opcion 'automovil' por defecto.")

    loc1 = input("Ciudad de origen: ")
    if loc1 == "s" or loc1 == "s":
        break
    orig = geocoding(loc1, key)
    print(orig,"\n")

    loc2 = input("Ciudad de destino: ")
    
    if loc2 == "s" or loc2 == "s":
        break

    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de rutas: " + str(paths_status) + "\nURL de la API de rutas:\n" + paths_url)
        
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3] + " usando " + vehicle)
        input()
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)

            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))

            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            input()
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000, distance/1000/1.61))
            print("=============================================")
        else:
            print("mensaje de error: " + paths_data["message"])
            print("*************************************************")





    #print(dest)
    input()
    