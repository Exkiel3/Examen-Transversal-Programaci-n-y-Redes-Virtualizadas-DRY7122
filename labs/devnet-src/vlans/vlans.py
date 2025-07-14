import os
os.system("clear")

print("Verificador de rangos de VLAN")
print("Escribe 'salir' para terminar el programa.")
print("----------------------------------------")

while True:
    entrada = input("Ingrese el número de VLAN que desee verificar(1 - 4094): ")

    if entrada.lower() == "salir":
        print("Programa terminado.")
        break

    try:
        vlan = int(entrada)
        print("Número de VLAN: {}".format(vlan))

        if 1 <= vlan <= 1005:
            print("Tipo de Vlan: es de rango NORMAL")
        elif 1006 <= vlan <= 4094:
            print("Tipo de VLAN: es de rango EXTENDIDO")
        else:
            print("VLAN fuera de un rango válido (1 - 4094)")

        print("----------------------------------------")

    except ValueError:
        print("Error: Debe ingresar un número entero válido para la VLAN o escribir 'salir'")
        print("----------------------------------------")
